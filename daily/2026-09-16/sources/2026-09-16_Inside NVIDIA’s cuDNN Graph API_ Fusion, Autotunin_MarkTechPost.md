---
publish_time: 1789508231
link: https://www.marktechpost.com/2026/09/15/inside-nvidias-cudnn-graph-api-fusion-autotuning-and-plan-reuse-with-cudnn-frontend/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  本文从框架之下剖析 NVIDIA cuDNN Frontend 的 graph API：将计算描述为算子图，交由 cuDNN 选择并运行引擎，开发者再自行接管引擎选择。每个 kernel 均以声明张量维度与步长、链式调用算子的统一方式表达，覆盖融合（Fusion）、自动调优（Autotuning）与计划复用（Plan Reuse），帮助开发者精细控制深度学习算子的底层执行。
---

# 深入 NVIDIA cuDNN Graph API：融合、自动调优与计划复用

> 原文链接：https://www.marktechpost.com/2026/09/15/inside-nvidias-cudnn-graph-api-fusion-autotuning-and-plan-reuse-with-cudnn-frontend/
> 来源：MarkTechPost

In this tutorial, we work through the cuDNN Frontend&#8216;s graph API from below the framework: we describe a computation as a graph of operations, let cuDNN pick an engine to run it, and then take control of that choice ourselves. Every kernel we build here is expressed the same way: we declare tensors by their dimensions and strides, chain operations onto them, run the five-step build pipeline of validate, build operation graph, create execution plans, check support, and build plans, and then execute against a variant pack of pointers. We run it all on a single Colab GPU, checking each result against a PyTorch reference so we can see both that the fusion is correct and what it costs. The topics build on each other, moving from a single fused convolution to autotuning across engine configs, FP8-style epilogues, attention, plan serialization, dynamic shapes, and CUDA graph capture.

Copy CodeCopiedUse a different Browser

import os
import sys
import glob
import math
import time
import ctypes
import traceback
import subprocess
RESULTS = {}
def banner(title):
   print("\n" + "=" * 78)
   print(title)
   print("=" * 78)
def section(name):
   def wrap(fn):
       def run(*a, **kw):
           banner(name)
           try:
               out = fn(*a, **kw)
               RESULTS[name] = out if isinstance(out, str) else "ok"
               return out
           except Exception as e:
               RESULTS[name] = f"SKIPPED / FAILED -> {type(e).__name__}: {e}"
               print(f"\n[!] {name} did not complete: {type(e).__name__}: {e}")
               traceback.print_exc(limit=3)
               return None
       return run
   return wrap
banner("0. Install nvidia-cudnn-frontend and locate libcudnn")
subprocess.run(
   [sys.executable, "-m", "pip", "install", "-q", "nvidia-cudnn-frontend"],
   check=True,
)
import torch
assert torch.cuda.is_available(), "No GPU. Runtime -> Change runtime type -> GPU."
torch.backends.cudnn.enabled = True
_ = torch.nn.functional.conv2d(
   torch.randn(1, 1, 8, 8, device="cuda"), torch.randn(1, 1, 3, 3, device="cuda")
)
torch.cuda.synchronize()
try:
   import nvidia.cudnn
   _libdir = os.path.join(os.path.dirname(nvidia.cudnn.__file__), "lib")
   os.environ["CUDNN_PATH"] = os.path.dirname(nvidia.cudnn.__file__)
   os.environ["LD_LIBRARY_PATH"] = _libdir + ":" + os.environ.get("LD_LIBRARY_PATH", "")
   for _so in sorted(glob.glob(os.path.join(_libdir, "libcudnn*.so*"))):
       try:
           ctypes.CDLL(_so, mode=ctypes.RTLD_GLOBAL)
       except OSError:
           pass
except Exception as _e:
   print(f"  (no pip cuDNN package found, relying on system cuDNN: {_e})")
import cudnn
print("  cuDNN frontend imported successfully.")
banner("1. Environment")
DEV = torch.device("cuda")
MAJOR, MINOR = torch.cuda.get_device_capability()
SM = MAJOR * 10 + MINOR
CUDNN_VER = cudnn.backend_version()
print(f"  GPU                 : {torch.cuda.get_device_name(0)}")
print(f"  Compute capability  : sm_{SM}")
print(f"  Torch / CUDA        : {torch.__version__} / {torch.version.cuda}")
print(f"  cuDNN backend       : {CUDNN_VER}")
try:
   print(f"  cuDNN version str   : {cudnn.backend_version_string()}")
except Exception:
   pass
DTYPE = torch.bfloat16 if SM >= 80 else torch.float16
HAS_SDPA = SM >= 80
print(f"  Working dtype       : {DTYPE}")
print(f"  Fused SDPA usable   : {HAS_SDPA}")
HANDLE = cudnn.create_handle()
TORCH2CUDNN = {
   torch.float16: cudnn.data_type.HALF,
   torch.bfloat16: cudnn.data_type.BFLOAT16,
   torch.float32: cudnn.data_type.FLOAT,
   torch.int32: cudnn.data_type.INT32,
   torch.int64: cudnn.data_type.INT64,
   torch.int8: cudnn.data_type.INT8,
   torch.uint8: cudnn.data_type.UINT8,
}
def tensor_of(graph, t, name):
   return graph.tensor(
       name=name,
       dim=list(t.size()),
       stride=list(t.stride()),
       data_type=TORCH2CUDNN[t.dtype],
   )
def scalar_of(graph, name):
   return graph.tensor(
       name=name,
       dim=[1, 1, 1],
       stride=[1, 1, 1],
       data_type=cudnn.data_type.FLOAT,
       is_pass_by_value=True,
   )
def build(graph, heur=None, policy=None):
   heur = heur or [cudnn.heur_mode.A, cudnn.heur_mode.FALLBACK]
   graph.validate()
   graph.build_operation_graph()
   graph.create_execution_plans(heur)
   graph.check_support()
   if policy is None:
       graph.build_plans()
   else:
       graph.build_plans(policy)
   return graph
def workspace_for(graph):
   n = graph.get_workspace_size()
   return torch.empty(max(n, 1), device=DEV, dtype=torch.uint8)
def bench(fn, warmup=10, iters=50):
   for _ in range(warmup):
       fn()
   torch.cuda.synchronize()
   s, e = torch.cuda.Event(True), torch.cuda.Event(True)
   s.record()
   for _ in range(iters):
       fn()
   e.record()
   torch.cuda.synchronize()
   return s.elapsed_time(e) / iters
def tflops(flops, ms):
   return flops / (ms * 1e-3) / 1e12
def report(tag, ms, flops=None):
   extra = f"   ({tflops(flops, ms):7.2f} TFLOP/s)" if flops else ""
   print(f"    {tag:<34s} {ms:8.3f} ms{extra}")

We start by installing nvidia-cudnn-frontend and solving the problem that trips up most first runs: making libcudnn.so visible to the frontend&#8217;s dynamic loader. We force PyTorch to load its bundled cuDNN first and then preload the shared objects explicitly, so the frontend&#8217;s own dlopen resolves against a library already resident in the process. We then report the compute capability, pick bfloat16 or float16 accordingly, create the cuDNN handle, and define the helpers for tensor description, graph building, workspace allocation, and event-based benchmarking that the rest of the notebook reuses.

Copy CodeCopiedUse a different Browser

N, C, H, W = 32, 128, 56, 56
K, R, S = 256, 3, 3
PAD, STR, DIL = 1, 1, 1
P = (H + 2 * PAD - DIL * (R - 1) - 1) // STR + 1
Q = (W + 2 * PAD - DIL * (S - 1) - 1) // STR + 1
CONV_FLOPS = 2 * N * K * P * Q * C * R * S
CONV_STATE = {}
@section("2. Fused Conv -> Bias -> ReLU")
def conv_fusion():
   x = torch.randn(N, C, H, W, device=DEV, dtype=DTYPE).to(memory_format=torch.channels_last)
   w = torch.randn(K, C, R, S, device=DEV, dtype=DTYPE).to(memory_format=torch.channels_last)
   b = torch.randn(1, K, 1, 1, device=DEV, dtype=DTYPE)
   y = torch.empty(N, K, P, Q, device=DEV, dtype=DTYPE).to(memory_format=torch.channels_last)
   g = cudnn.pygraph(
       handle=HANDLE,
       name="conv_bias_relu",
       io_data_type=TORCH2CUDNN[DTYPE],
       intermediate_data_type=cudnn.data_type.FLOAT,
       compute_data_type=cudnn.data_type.FLOAT,
   )
   X = tensor_of(g, x, "X")
   Wt = tensor_of(g, w, "W")
   Bt = tensor_of(g, b, "bias")
   conv = g.conv_fprop(
       image=X, weight=Wt,
       padding=[PAD, PAD], stride=[STR, STR], dilation=[DIL, DIL],
       compute_data_type=cudnn.data_type.FLOAT,
   )
   biased = g.bias(input=conv, bias=Bt)
   Y = g.relu(input=biased)
   Y.set_output(True).set_data_type(TORCH2CUDNN[DTYPE])
   Y.set_dim(list(y.size())).set_stride(list(y.stride()))
   t0 = time.perf_counter()
   build(g)
   build_ms = (time.perf_counter() - t0) * 1e3
   ws = workspace_for(g)
   pack = {X: x, Wt: w, Bt: b, Y: y}
   g.execute(pack, ws)
   torch.cuda.synchronize()
   ref = torch.relu(torch.nn.functional.conv2d(x, w, bias=b.flatten(), padding=PAD))
   err = (y.float() - ref.float()).abs().max().item()
   scale = ref.float().abs().max().item()
   print(f"    problem  : N{N} C{C} {H}x{W} -> K{K} {R}x{S}  ({DTYPE})")
   print(f"    build    : {build_ms:.1f} ms   workspace: {ws.numel()/1024:.1f} KiB")
   print(f"    max |err|: {err:.4f}  (ref max {scale:.2f}, rel {err/max(scale,1e-9):.2e})")
   assert err / max(scale, 1e-9) < 5e-2, "numerical mismatch vs PyTorch"
   ms_cudnn = bench(lambda: g.execute(pack, ws))
   ms_torch = bench(lambda: torch.relu(
       torch.nn.functional.conv2d(x, w, bias=b.flatten(), padding=PAD)))
   print()
   report("cuDNN FE (single fused kernel)", ms_cudnn, CONV_FLOPS)
   report("PyTorch (conv+bias, then relu)", ms_torch, CONV_FLOPS)
   print(f"    speedup: {ms_torch/ms_cudnn:.2f}x")
   CONV_STATE.update(graph=g, pack=pack, ws=ws, x=x, w=w, b=b, y=y)
   return f"{ms_cudnn:.3f} ms, {tflops(CONV_FLOPS, ms_cudnn):.1f} TFLOP/s"
conv_fusion()

We build our first graph, a convolution followed by a bias add and a ReLU, all fused into a single kernel. We keep every tensor in channels_last because that is what gives cuDNN the NHWC strides its tensor-core engines want, and we pin the output dimensions and strides explicitly so the result is written back in the same layout. We validate the output against torch.nn.functional.conv2d, then benchmark the fused graph against PyTorch running the convolution and activation as separate kernels.

Copy CodeCopiedUse a different Browser

@section("3. Autotuning: build ALL plans, time each engine config")
def autotune():
   x, w, b, y = CONV_STATE["x"], CONV_STATE["w"], CONV_STATE["b"], CONV_STATE["y"]
   g = cudnn.pygraph(
       handle=HANDLE, name="conv_autotune",
       io_data_type=TORCH2CUDNN[DTYPE],
       intermediate_data_type=cudnn.data_type.FLOAT,
       compute_data_type=cudnn.data_type.FLOAT,
   )
   X = tensor_of(g, x, "X")
   Wt = tensor_of(g, w, "W")
   Bt = tensor_of(g, b, "bias")
   Y = g.relu(input=g.bias(
       input=g.conv_fprop(image=X, weight=Wt, padding=[PAD, PAD],
                          stride=[STR, STR], dilation=[DIL, DIL],
                          compute_data_type=cudnn.data_type.FLOAT),
       bias=Bt))
   Y.set_output(True).set_data_type(TORCH2CUDNN[DTYPE])
   Y.set_dim(list(y.size())).set_stride(list(y.stride()))
   g.validate()
   g.build_operation_graph()
   g.create_execution_plans([cudnn.heur_mode.A, cudnn.heur_mode.B, cudnn.heur_mode.FALLBACK])
   g.check_support()
   g.build_plans(cudnn.build_plan_policy.ALL)
   n_plans = g.get_execution_plan_count()
   print(f"    {n_plans} candidate engine configs survived support checks\n")
   pack = {X: x, Wt: w, Bt: b, Y: y}
   timings = []
   for i in range(n_plans):
       try:
           g.build_plan_at_index(i)
           ws_sz = max(g.get_workspace_size_plan_at_index(i), 1)
           ws = torch.empty(ws_sz, device=DEV, dtype=torch.uint8)
           ms = bench(lambda: g.execute_plan_at_index(pack, ws, i), warmup=3, iters=15)
           timings.append((ms, i, ws_sz))
           print(f"      plan {i:>3d}: {ms:8.3f} ms  "
                 f"{tflops(CONV_FLOPS, ms):7.2f} TFLOP/s  ws={ws_sz/1024:8.1f} KiB")
       except Exception as e:
           print(f"      plan {i:>3d}: unusable ({type(e).__name__})")
   assert timings, "no plan executed"
   timings.sort()
   best_ms, best_i, best_ws = timings[0]
   worst_ms = timings[-1][0]
   print(f"\n    fastest = plan {best_i} @ {best_ms:.3f} ms")
   print(f"    slowest = {worst_ms:.3f} ms  -> {worst_ms/best_ms:.1f}x spread across engines")
   print("    Takeaway: heuristics are good, but for a hot shape you ship the")
   print("    autotuned index (or the serialized plan from section 6).")
   return f"best plan {best_i} @ {best_ms:.3f} ms ({worst_ms/best_ms:.1f}x spread)"
autotune()

We rebuild the same convolution but stop trusting the heuristic, asking for plans from heuristic modes A, B, and FALLBACK and compiling all of them with build_plan_policy.ALL. We then walk the plan list, build each config, allocate its specific workspace, and time it with execute_plan_at_index, printing throughput and workspace size for every candidate. The spread between the fastest and slowest engine is the point of the exercise, because it tells us how much we gain by shipping an autotuned index instead of accepting the default pick.

Copy CodeCopiedUse a different Browser

@section("4. Matmul -> scale -> bias -> activation -> AMAX")
def matmul_epilogue():
   Bsz, M, Kd, Nd = 16, 512, 1024, 512
   MM_FLOPS = 2 * Bsz * M * Nd * Kd
   a = torch.randn(Bsz, M, Kd, device=DEV, dtype=DTYPE)
   bm = torch.randn(Bsz, Kd, Nd, device=DEV, dtype=DTYPE)
   bias = torch.randn(1, 1, Nd, device=DEV, dtype=DTYPE)
   out = torch.empty(Bsz, M, Nd, device=DEV, dtype=DTYPE)
   amax = torch.empty(1, 1, 1, device=DEV, dtype=torch.float32)
   alpha_val = 0.125
   alpha = torch.full((1, 1, 1), alpha_val, dtype=torch.float32)
   g = cudnn.pygraph(
       handle=HANDLE, name="matmul_epilogue",
       io_data_type=TORCH2CUDNN[DTYPE],
       intermediate_data_type=cudnn.data_type.FLOAT,
       compute_data_type=cudnn.data_type.FLOAT,
   )
   A = tensor_of(g, a, "A")
   Bt = tensor_of(g, bm, "B")
   BIAS = tensor_of(g, bias, "bias")
   ALPHA = scalar_of(g, "alpha")
   acc = g.matmul(A=A, B=Bt, compute_data_type=cudnn.data_type.FLOAT)
   scaled = g.mul(a=acc, b=ALPHA)
   biased = g.bias(input=scaled, bias=BIAS)
   act_name = "relu"
   if hasattr(g, "gelu"):
       try:
           act = g.gelu(input=biased)
           act_name = "gelu"
       except Exception:
           act = g.relu(input=biased)
   else:
       act = g.relu(input=biased)
   print(f"    activation used: {act_name}")
   OUT = act
   OUT.set_output(True).set_data_type(TORCH2CUDNN[DTYPE])
   have_amax = True
   try:
       AMAX = g.reduction(input=act, mode=cudnn.reduction_mode.AMAX,
                          compute_data_type=cudnn.data_type.FLOAT)
       AMAX.set_output(True).set_data_type(cudnn.data_type.FLOAT)
       AMAX.set_dim([1, 1, 1]).set_stride([1, 1, 1])
   except Exception as e:
       have_amax = False
       print(f"    (AMAX reduction unavailable here: {e})")
   build(g)
   ws = workspace_for(g)
   pack = {A: a, Bt: bm, BIAS: bias, ALPHA: alpha, OUT: out}
   if have_amax:
       pack[AMAX] = amax
   g.execute(pack, ws)
   torch.cuda.synchronize()
   ref = torch.matmul(a.float(), bm.float()) * alpha_val + bias.float()
   ref = torch.nn.functional.gelu(ref) if act_name == "gelu" else torch.relu(ref)
   rel = ((out.float() - ref).abs().max() / ref.abs().max()).item()
   print(f"    shape    : ({Bsz},{M},{Kd}) x ({Bsz},{Kd},{Nd})")
   print(f"    rel err  : {rel:.2e}")
   if have_amax:
       print(f"    fused AMAX {amax.item():.4f} vs torch {ref.abs().max().item():.4f}")
   ms = bench(lambda: g.execute(pack, ws))
   def torch_ref():
       r = torch.baddbmm(bias.expand(Bsz, M, Nd), a, bm, beta=1.0, alpha=alpha_val)
       r = torch.nn.functional.gelu(r) if act_name == "gelu" else torch.relu(r)
       return r.abs().amax()
   ms_t = bench(torch_ref)
   print()
   report("cuDNN FE (one fused kernel)", ms, MM_FLOPS)
   report("PyTorch (bmm + act + amax)", ms_t, MM_FLOPS)
   print(f"    speedup: {ms_t/ms:.2f}x  -- the win is the epilogue traffic, not the GEMM")
   return f"{ms:.3f} ms, {tflops(MM_FLOPS, ms):.1f} TFLOP/s, {ms_t/ms:.2f}x vs torch"
matmul_epilogue()

We move to a batched matmul and hang a full epilogue off it: an alpha scale supplied as a pass-by-value host scalar, a bias add, an activation, and an AMAX reduction over the result. The AMAX in the same kernel is the pattern that FP8 training relies on, since it collects the scale factor for the next quantization step without a second pass over the output. We compare against a PyTorch chain of baddbmm, activation, and amax, which makes clear that the speedup comes from eliminating epilogue memory traffic rather than from a faster GEMM.

Copy CodeCopiedUse a different Browser

@section("5. SDPA (Flash Attention) with causal masking")
def sdpa_demo():
   if not HAS_SDPA:
       raise RuntimeError(f"fused SDPA needs SM80+ (Ampere), this GPU is sm_{SM}")
   b, h, s, d = 4, 16, 1024, 64
   scale = 1.0 / math.sqrt(d)
   SDPA_FLOPS = 4 * b * h * s * s * d * 0.5
   q = torch.randn(b, h, s, d, device=DEV, dtype=DTYPE)
   k = torch.randn(b, h, s, d, device=DEV, dtype=DTYPE)
   v = torch.randn(b, h, s, d, device=DEV, dtype=DTYPE)
   o = torch.empty(b, h, s, d, device=DEV, dtype=DTYPE)
   g = cudnn.pygraph(
       handle=HANDLE, name="sdpa",
       io_data_type=TORCH2CUDNN[DTYPE],
       intermediate_data_type=cudnn.data_type.FLOAT,
       compute_data_type=cudnn.data_type.FLOAT,
   )
   Q, Kt, V = tensor_of(g, q, "Q"), tensor_of(g, k, "K"), tensor_of(g, v, "V")
   causal = True
   try:
       O, _stats = g.sdpa(name="sdpa", q=Q, k=Kt, v=V,
                          is_inference=True, attn_scale=scale, use_causal_mask=True)
   except TypeError:
       try:
           O, _stats = g.sdpa(name="sdpa", q=Q, k=Kt, v=V,
                              is_inference=True, attn_scale=scale,
                              diagonal_alignment=cudnn.diagonal_alignment.TOP_LEFT,
                              right_bound=0)
       except Exception:
           causal = False
           O, _stats = g.sdpa(name="sdpa", q=Q, k=Kt, v=V,
                              is_inference=True, attn_scale=scale)
   print(f"    causal masking: {causal}")
   O.set_output(True).set_data_type(TORCH2CUDNN[DTYPE])
   O.set_dim(list(o.size())).set_stride(list(o.stride()))
   build(g)
   ws = workspace_for(g)
   pack = {Q: q, Kt: k, V: v, O: o}
   g.execute(pack, ws)
   torch.cuda.synchronize()
   ref = torch.nn.functional.scaled_dot_product_attention(q, k, v, is_causal=causal, scale=scale)
   rel = ((o.float() - ref.float()).abs().max() / ref.float().abs().max()).item()
   print(f"    shape   : b{b} h{h} s{s} d{d}   workspace {ws.numel()/1024:.1f} KiB")
   print(f"    rel err : {rel:.2e}")
   ms = bench(lambda: g.execute(pack, ws))
   ms_t = bench(lambda: torch.nn.functional.scaled_dot_product_attention(
       q, k, v, is_causal=causal, scale=scale))
   print()
   report("cuDNN FE SDPA", ms, SDPA_FLOPS)
   report("torch SDPA (backend's choice)", ms_t, SDPA_FLOPS)
   print("    Note: torch may already be dispatching to cuDNN or FlashAttention,")
   print("    so parity here is the expected, healthy outcome.")
   return f"{ms:.3f} ms, {tflops(SDPA_FLOPS, ms):.1f} TFLOP/s"
sdpa_demo()
@section("6. Serialize a built graph, reload it, execute by UID")
def serialization():
   Bsz, M, Kd, Nd = 8, 256, 512, 256
   a = torch.randn(Bsz, M, Kd, device=DEV, dtype=DTYPE)
   bm = torch.randn(Bsz, Kd, Nd, device=DEV, dtype=DTYPE)
   out = torch.empty(Bsz, M, Nd, device=DEV, dtype=DTYPE)
   UID_A, UID_B, UID_C = 1, 2, 3
   g = cudnn.pygraph(
       handle=HANDLE, name="serializable_mm",
       io_data_type=TORCH2CUDNN[DTYPE],
       intermediate_data_type=cudnn.data_type.FLOAT,
       compute_data_type=cudnn.data_type.FLOAT,
   )
   A = tensor_of(g, a, "A").set_uid(UID_A)
   Bt = tensor_of(g, bm, "B").set_uid(UID_B)
   C = g.matmul(A=A, B=Bt, compute_data_type=cudnn.data_type.FLOAT)
   C.set_output(True).set_data_type(TORCH2CUDNN[DTYPE]).set_uid(UID_C)
   t0 = time.perf_counter()
   build(g)
   cold_ms = (time.perf_counter() - t0) * 1e3
   blob = g.serialize()
   print(f"    cold build      : {cold_ms:.1f} ms")
   print(f"    serialized plan : {len(blob)} bytes (cache this to disk / ship it)")
   t0 = time.perf_counter()
   g2 = cudnn.pygraph()
   try:
       g2.deserialize(HANDLE, blob)
   except TypeError:
       g2.deserialize(blob)
   warm_ms = (time.perf_counter() - t0) * 1e3
   print(f"    deserialize     : {warm_ms:.1f} ms  -> {cold_ms/max(warm_ms,1e-6):.1f}x faster startup")
   ws = torch.empty(max(g2.get_workspace_size(), 1), device=DEV, dtype=torch.uint8)
   g2.execute({UID_A: a, UID_B: bm, UID_C: out}, ws, handle=HANDLE)
   torch.cuda.synchronize()
   ref = torch.bmm(a.float(), bm.float())
   rel = ((out.float() - ref).abs().max() / ref.abs().max()).item()
   print(f"    rel err after reload: {rel:.2e}")
   return f"{len(blob)} B blob, reload {cold_ms/max(warm_ms,1e-6):.1f}x faster than rebuild"
serialization()

We build a fused scaled dot-product attention graph with causal masking and check it against torch.nn.functional.scaled_dot_product_attention, guarding the whole section behind an SM80 check because the fused kernels need Ampere or newer. We write the causal argument with fallbacks, since the frontend has moved from use_causal_mask toward diagonal_alignment and bound arguments across its 1.x releases. We then serialize a built matmul graph to bytes, reload it into a fresh graph object, and execute it via integer UIDs, which lets us skip the compilation cost entirely at process startup.

Copy CodeCopiedUse a different Browser

@section("7. Dynamic shapes with a shared kernel cache")
def dynamic_shapes():
   kc = cudnn.create_kernel_cache()
   def make(n):
       x = torch.randn(n, 64, 32, 32, device=DEV, dtype=DTYPE).to(memory_format=torch.channels_last)
       w = torch.randn(64, 64, 3, 3, device=DEV, dtype=DTYPE).to(memory_format=torch.channels_last)
       y = torch.empty(n, 64, 32, 32, device=DEV, dtype=DTYPE).to(memory_format=torch.channels_last)
       g = cudnn.pygraph(
           handle=HANDLE, name=f"dyn_{n}",
           io_data_type=TORCH2CUDNN[DTYPE],
           intermediate_data_type=cudnn.data_type.FLOAT,
           compute_data_type=cudnn.data_type.FLOAT,
           kernel_cache=kc,
           is_dynamic_shape_enabled=True,
       )
       X, Wt = tensor_of(g, x, "X"), tensor_of(g, w, "W")
       Y = g.conv_fprop(image=X, weight=Wt, padding=[1, 1], stride=[1, 1],
                        dilation=[1, 1], compute_data_type=cudnn.data_type.FLOAT)
       Y.set_output(True).set_data_type(TORCH2CUDNN[DTYPE])
       Y.set_dim(list(y.size())).set_stride(list(y.stride()))
       t0 = time.perf_counter()
       build(g)
       ms = (time.perf_counter() - t0) * 1e3
       ws = workspace_for(g)
       g.execute({X: x, Wt: w, Y: y}, ws)
       torch.cuda.synchronize()
       return ms
   times = [(n, make(n)) for n in (8, 16, 24, 32)]
   for n, ms in times:
       print(f"      batch {n:>3d}: build {ms:7.1f} ms")
   first, rest = times[0][1], [m for _, m in times[1:]]
   print(f"\n    first shape {first:.1f} ms, later shapes avg {sum(rest)/len(rest):.1f} ms")
   print("    The cache lets shape-variant graphs reuse an already-JIT'd kernel,")
   print("    which is what keeps variable batch/seqlen serving out of rebuild hell.")
   return f"first {first:.0f} ms vs subsequent {sum(rest)/len(rest):.0f} ms"
dynamic_shapes()
@section("8. CUDA Graph capture around a cuDNN execution plan")
def cuda_graph_capture():
   if not CONV_STATE:
       raise RuntimeError("section 2 did not run, nothing to capture")
   g, pack, ws = CONV_STATE["graph"], CONV_STATE["pack"], CONV_STATE["ws"]
   eager_ms = bench(lambda: g.execute(pack, ws))
   side = torch.cuda.Stream()
   side.wait_stream(torch.cuda.current_stream())
   with torch.cuda.stream(side):
       cudnn.set_stream(handle=HANDLE, stream=side.cuda_stream)
       for _ in range(3):
           g.execute(pack, ws, handle=HANDLE)
   torch.cuda.current_stream().wait_stream(side)
   torch.cuda.synchronize()
   cg = torch.cuda.CUDAGraph()
   with torch.cuda.graph(cg):
       cudnn.set_stream(handle=HANDLE, stream=torch.cuda.current_stream().cuda_stream)
       g.execute(pack, ws, handle=HANDLE)
   cudnn.set_stream(handle=HANDLE, stream=torch.cuda.current_stream().cuda_stream)
   replay_ms = bench(lambda: cg.replay())
   report("plain execute()", eager_ms)
   report("cuda graph replay()", replay_ms)
   print(f"    launch overhead removed: {(eager_ms-replay_ms)*1e3:.1f} us/iter")
   print("    Pointers are frozen at capture time -- reuse the same buffers and")
   print("    copy new data into them, or re-capture.")
   return f"{eager_ms:.3f} -> {replay_ms:.3f} ms via replay"
cuda_graph_capture()
banner("SUMMARY")
for name, res in RESULTS.items():
   print(f"  {name:<58s} {res}")
print("""
Where to go next
 - samples/python in the repo: FP8/MXFP8 attention, paged KV cache, MoE grouped GEMM
 - python/cudnn/: the open-sourced CuTe DSL kernels (SDPA, grouped GEMM + SwiGLU,
   block-sparse and native sparse attention) you can read and modify
 - debugging: CUDNN_FRONTEND_LOG_INFO=1 and CUDNN_FRONTEND_LOG_FILE=stdout
   (use level 10 during CUDA graph capture -- level 1 dumps tensors and is not
   capture-safe)
""")

We finish with two production concerns. First, we share a kernel cache across four graphs that differ only in batch size and time each build, so we can see later shapes reuse an already compiled kernel instead of paying the JIT cost again. Then we capture the convolution plan inside a CUDA graph, setting the cuDNN handle&#8217;s stream to the capture stream. So the work lands in the graph, and we measure how much per-iteration launch overhead the replay removes.

In conclusion, what we built here was small in code but broad in scope: a convolution, a matmul, and an attention kernel, each expressed as a graph rather than a library call. Working at that level changed what we could decide. We chose which operations collapsed into a single kernel, so the bias adds, activations, and AMAX reductions we folded into the epilogues never wrote an intermediate to memory. We chose the engine ourselves instead of accepting a heuristic, and timing every candidate config told us what that choice was worth. We also chose when to pay for compilation, pushing it out of the hot path with serialized plans, a kernel cache shared across shapes, and CUDA graph capture. The checks against PyTorch mattered as much as the timings, since the places where we merely matched it were usually places where PyTorch was already calling cuDNN underneath. That marked out where this API earns its keep: fusions with no framework-level equivalent, shapes hot enough to justify autotuning, and small kernels where startup and launch costs dominate.

Check out the FULL CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Inside NVIDIA’s cuDNN Graph API: Fusion, Autotuning, and Plan Reuse with cuDNN Frontend appeared first on MarkTechPost.