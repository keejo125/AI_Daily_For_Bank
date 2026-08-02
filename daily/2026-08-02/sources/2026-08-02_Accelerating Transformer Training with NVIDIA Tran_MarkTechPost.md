---
publish_time: 1785609075
status: confirmed
category: 国际
is_model_related: false
digest: |
  NVIDIA发布技术教程，详解Transformer Engine如何通过融合GPU内核、BF16和FP8混合精度加速Transformer模型训练。核心原理是在训练前向和反向传播中动态缩放张量到FP8精度，利用H100/H200 GPU的FP8 Tensor Core实现更高吞吐量，同时通过自动混合精度管理防止精度损失。融合内核将多个连续操作（如矩阵乘法+偏置+激活函数）合并为单个GPU内核调用，大幅减少显存读写和kernel启动开销，是当前大模型训练效率优化的关键技术路径。
---


# Accelerating Transformer Training with NVIDIA Transformer Engine, Fused Kernels, BF16, FP8, and GPU Benchmarking

> 原文链接：https://www.marktechpost.com/2026/08/01/accelerating-transformer-training-with-nvidia-transformer-engine-fused-kernels-bf16-fp8-and-gpu-benchmarking/
> 来源：MarkTechPost

In this tutorial, we explore how NVIDIA Transformer Engine accelerates transformer workloads by combining fused GPU kernels, BF16 computation, and hardware-aware FP8 execution. We begin by installing Transformer Engine and detecting the active GPU architecture so that we can determine whether the runtime supports TE kernels, FP8 tensor cores, or only the pure-PyTorch fallback path. We then examine core fused components such as te.Linear, te.LayerNorm, te.LayerNormLinear, te.LayerNormMLP, and te.TransformerLayer, while also configuring a delayed-scaling FP8 recipe that manages tensor scaling, amax history, and hybrid E4M3/E5M2 formats. Using these components, we construct a compact GPT-style causal language model, train it on deterministic synthetic sequences, compare higher-precision and FP8 execution, measure runtime and peak GPU memory, inspect FP8 metadata, and validate the trained model through autoregressive generation.

Copy CodeCopiedUse a different Browser

import subprocess, sys, os
def pip_install(*pkgs):
   subprocess.run([sys.executable, "-m", "pip", "install", "-q",
                   "--no-build-isolation", *pkgs], check=False)
print(">> Installing transformer_engine[pytorch] (this can take a few minutes)...")
pip_install("transformer_engine[pytorch]")
import time, math, gc
import torch
import torch.nn as nn
import torch.nn.functional as F
assert torch.cuda.is_available(), "Enable a GPU runtime in Colab first!"
DEVICE = "cuda"
props = torch.cuda.get_device_properties(0)
CC = (props.major, props.minor)
GPU_NAME = props.name
print(f">> GPU: {GPU_NAME} | compute capability {CC[0]}.{CC[1]} | "
     f"{props.total_memory/1e9:.1f} GB")
TE_CAPABLE  = CC >= (8, 0)
FP8_CAPABLE = CC >= (8, 9)
te = None
if TE_CAPABLE:
   try:
       import transformer_engine.pytorch as te
       from transformer_engine.common import recipe
       print(">> Transformer Engine imported OK:",
             getattr(te, "__version__", "unknown version"))
   except Exception as e:
       print(f">> TE import failed ({e}); using pure-PyTorch fallback.")
       TE_CAPABLE = FP8_CAPABLE = False
else:
   print(">> GPU is pre-Ampere (e.g. T4): TE kernels unsupported -> fallback mode.")
if TE_CAPABLE and FP8_CAPABLE and te is not None:
   try:
       ok, reason = te.fp8.check_fp8_support()
       FP8_CAPABLE = bool(ok)
       if not ok:
           print(">> TE reports FP8 unsupported:", reason)
   except Exception:
       pass
print(f">> Mode: TE={'ON' if TE_CAPABLE else 'OFF'} | "
     f"FP8={'ON' if FP8_CAPABLE else 'OFF (will use BF16)'}")
torch.manual_seed(1234)
if TE_CAPABLE:
   H = 768
   x_demo = torch.randn(8, 32, H, device=DEVICE, dtype=torch.bfloat16)
   lin      = te.Linear(H, H, bias=True, params_dtype=torch.bfloat16).to(DEVICE)
   ln       = te.LayerNorm(H, params_dtype=torch.bfloat16).to(DEVICE)
   ln_lin   = te.LayerNormLinear(H, 3 * H, params_dtype=torch.bfloat16).to(DEVICE)
   ln_mlp   = te.LayerNormMLP(H, 4 * H, params_dtype=torch.bfloat16).to(DEVICE)
   with torch.no_grad():
       print("\n>> Module tour (shapes):")
       print("   te.Linear         ", tuple(lin(x_demo).shape))
       print("   te.LayerNorm      ", tuple(ln(x_demo).shape))
       print("   te.LayerNormLinear", tuple(ln_lin(x_demo).shape))
       print("   te.LayerNormMLP   ", tuple(ln_mlp(x_demo).shape))
   del lin, ln, ln_lin, ln_mlp, x_demo
   gc.collect(); torch.cuda.empty_cache()
fp8_recipe = None
if FP8_CAPABLE:
   fp8_recipe = recipe.DelayedScaling(
       fp8_format=recipe.Format.HYBRID,
       amax_history_len=16,
       amax_compute_algo="max",
   )
   print("\n>> FP8 recipe:", fp8_recipe)

We install NVIDIA Transformer Engine and initialize the PyTorch environment required for GPU-accelerated execution. We inspect the active GPU, compute capability, and memory capacity to determine whether fused TE kernels and FP8 tensor cores are available. We also validate the core fused modules and configure a delayed-scaling FP8 recipe while preserving an automatic PyTorch fallback for unsupported hardware.

Copy CodeCopiedUse a different Browser

VOCAB, D_MODEL, N_HEADS, N_LAYERS, FFN, SEQ = 96, 768, 12, 4, 3072, 256
class MiniGPT_TE(nn.Module):
   """Causal LM where every block is a single fused te.TransformerLayer."""
   def __init__(self):
       super().__init__()
       self.emb = nn.Embedding(VOCAB, D_MODEL)
       self.pos = nn.Embedding(SEQ, D_MODEL)
       self.blocks = nn.ModuleList([
           te.TransformerLayer(
               hidden_size=D_MODEL,
               ffn_hidden_size=FFN,
               num_attention_heads=N_HEADS,
               self_attn_mask_type="causal",
               layer_number=i + 1,
               params_dtype=torch.bfloat16,
               hidden_dropout=0.0,
               attention_dropout=0.0,
           )
           for i in range(N_LAYERS)
       ])
       self.ln_f = nn.LayerNorm(D_MODEL)
       self.head = nn.Linear(D_MODEL, VOCAB, bias=False)
   def forward(self, idx):
       B, T = idx.shape
       h = self.emb(idx) + self.pos(torch.arange(T, device=idx.device))
       h = h.to(torch.bfloat16)
       for blk in self.blocks:
           h = blk(h)
       h = self.ln_f(h.float())
       return self.head(h)
class Block_PT(nn.Module):
   """Plain-PyTorch transformer block, mirrors te.TransformerLayer."""
   def __init__(self):
       super().__init__()
       self.ln1 = nn.LayerNorm(D_MODEL)
       self.attn = nn.MultiheadAttention(D_MODEL, N_HEADS, batch_first=True)
       self.ln2 = nn.LayerNorm(D_MODEL)
       self.mlp = nn.Sequential(nn.Linear(D_MODEL, FFN), nn.GELU(),
                                nn.Linear(FFN, D_MODEL))
   def forward(self, x, mask):
       a, _ = self.attn(self.ln1(x), self.ln1(x), self.ln1(x),
                        attn_mask=mask, need_weights=False)
       x = x + a
       return x + self.mlp(self.ln2(x))
class MiniGPT_PT(nn.Module):
   def __init__(self):
       super().__init__()
       self.emb = nn.Embedding(VOCAB, D_MODEL)
       self.pos = nn.Embedding(SEQ, D_MODEL)
       self.blocks = nn.ModuleList([Block_PT() for _ in range(N_LAYERS)])
       self.ln_f = nn.LayerNorm(D_MODEL)
       self.head = nn.Linear(D_MODEL, VOCAB, bias=False)
   def forward(self, idx):
       B, T = idx.shape
       mask = torch.triu(torch.full((T, T), float("-inf"),
                                    device=idx.device), diagonal=1)
       h = self.emb(idx) + self.pos(torch.arange(T, device=idx.device))
       for blk in self.blocks:
           h = blk(h, mask)
       return self.head(self.ln_f(h))
model = (MiniGPT_TE() if TE_CAPABLE else MiniGPT_PT()).to(DEVICE)
n_params = sum(p.numel() for p in model.parameters())
print(f"\n>> Model: {'TE fused' if TE_CAPABLE else 'pure PyTorch'} | "
     f"{n_params/1e6:.1f}M params | {N_LAYERS} layers x {D_MODEL}d")

We define a compact causal language model using fused te.TransformerLayer blocks for Transformer Engine execution. We also implement an equivalent pure-PyTorch transformer architecture with multi-head attention, layer normalization, residual connections, and feed-forward networks. We select the appropriate model dynamically according to GPU support and report the final parameter count and architectural dimensions.

Copy CodeCopiedUse a different Browser

def make_batch(bsz=16):
   phase  = torch.randint(0, VOCAB, (bsz, 1))
   stride = torch.randint(1, 7, (bsz, 1))
   steps  = torch.arange(SEQ + 1).unsqueeze(0)
   seq = (phase + stride * steps) % VOCAB
   return seq[:, :-1].to(DEVICE), seq[:, 1:].to(DEVICE)
opt = torch.optim.AdamW(model.parameters(), lr=3e-4)
def run_step(x, y, use_fp8):
   if TE_CAPABLE and use_fp8:
       with te.fp8_autocast(enabled=True, fp8_recipe=fp8_recipe):
           logits = model(x)
   else:
       logits = model(x)
   loss = F.cross_entropy(logits.float().reshape(-1, VOCAB), y.reshape(-1))
   opt.zero_grad(set_to_none=True)
   loss.backward()
   opt.step()
   return loss.item()
print(f"\n>> Training 60 steps ({'FP8' if FP8_CAPABLE else 'BF16/FP32'})...")
t0 = time.time()
for step in range(1, 61):
   x, y = make_batch()
   loss = run_step(x, y, use_fp8=FP8_CAPABLE)
   if step % 10 == 0:
       print(f"   step {step:3d} | loss {loss:.4f} | "
             f"{(time.time()-t0)/step*1000:.0f} ms/step")
print(f">> Final loss: {loss:.4f} (random guess would be ~{math.log(VOCAB):.2f})")

We create deterministic arithmetic-pattern sequences that allow the model to learn predictable token transitions across the vocabulary. We configure the AdamW optimizer and implement a training step that conditionally wraps the forward pass in te.fp8_autocast when FP8 execution is supported. We train the model for multiple iterations, monitor the loss and step latency, and compare the final loss against the random-guess baseline.

Copy CodeCopiedUse a different Browser

def bench(use_fp8, iters=30, warmup=10):
   x, y = make_batch(bsz=32)
   for _ in range(warmup):
       run_step(x, y, use_fp8)
   torch.cuda.synchronize()
   torch.cuda.reset_peak_memory_stats()
   t = time.time()
   for _ in range(iters):
       run_step(x, y, use_fp8)
   torch.cuda.synchronize()
   ms = (time.time() - t) / iters * 1000
   mem = torch.cuda.max_memory_allocated() / 1e9
   return ms, mem
print("\n>> Benchmark (batch 32, seq 256, fwd+bwd+optim):")
ms_hi, mem_hi = bench(use_fp8=False)
print(f"   {'BF16' if TE_CAPABLE else 'FP32'}: {ms_hi:7.1f} ms/step | "
     f"peak mem {mem_hi:.2f} GB")
if FP8_CAPABLE:
   ms_f8, mem_f8 = bench(use_fp8=True)
   print(f"   FP8 : {ms_f8:7.1f} ms/step | peak mem {mem_f8:.2f} GB")
   print(f"   Speedup: {ms_hi/ms_f8:.2f}x  "
         f"(gains grow with model size — try D_MODEL=2048, N_LAYERS=12)")
else:
   print("   FP8 benchmark skipped — needs an sm_89+ GPU (L4/H100/Ada/Blackwell).")
if FP8_CAPABLE:
   blk = model.blocks[0]
   for name, m in blk.named_modules():
       meta = getattr(m, "fp8_meta", None)
       if meta and "scaling_fwd" in meta:
           s = meta["scaling_fwd"]
           print(f"\n>> FP8 state of block-0 submodule '{name}':")
           print("   scale       :", s.scale.flatten()[:4].tolist())
           print("   amax_history:", s.amax_history[0, :4].tolist())
           break

We benchmark forward propagation, backpropagation, and optimizer updates using higher-precision and FP8 execution modes. We measure average training-step latency and peak allocated GPU memory to quantify the performance and memory impact of reduced-precision computation. We also inspect the scaling factors and amax history maintained by Transformer Engine to understand how delayed scaling stabilizes FP8 tensors.

Copy CodeCopiedUse a different Browser

@torch.no_grad()
def generate(prompt_len=8, gen_len=24):
   x, _ = make_batch(bsz=1)
   ctx = x[:, :prompt_len]
   for _ in range(gen_len):
       inp = ctx[:, -SEQ:]
       if TE_CAPABLE and FP8_CAPABLE:
           with te.fp8_autocast(enabled=True, fp8_recipe=fp8_recipe):
               logits = model(inp)
       else:
           logits = model(inp)
       nxt = logits[:, -1].argmax(-1, keepdim=True)
       ctx = torch.cat([ctx, nxt], dim=1)
   return ctx[0].tolist()
seq = generate()
print("\n>> Greedy generation (should continue the arithmetic pattern):")
print("   prompt+gen:", seq)
diffs = [(b - a) % VOCAB for a, b in zip(seq, seq[1:])]
print("   step diffs:", diffs, "<- constant stride = model learned the rule")
print("\n>> Done! Things to try next:")
print("   * Scale up: D_MODEL=2048, N_LAYERS=12 -> FP8 speedup becomes dramatic")
print("   * recipe.Format.E4M3 vs HYBRID; amax_history_len=1024")
print("   * te.LayerNormMLP / te.LayerNormLinear in your own architectures")
print("   * fp8_model_init() to store weights themselves in FP8 for inference")

We implement greedy autoregressive generation by repeatedly feeding the latest context into the trained causal language model. We compare consecutive generated tokens to verify whether the model preserves the constant arithmetic stride present in the synthetic training data. We conclude by identifying practical extensions, including larger model dimensions, alternative FP8 formats, longer amax histories, fused modules, and FP8 weight initialization.

In conclusion, we demonstrated how we integrate NVIDIA Transformer Engine into an end-to-end transformer training workflow while preserving compatibility across different Colab GPU environments. We used fused transformer modules to reduce kernel-launch overhead and memory traffic, applied FP8 autocasting with delayed scaling when supported, and retained BF16 or FP32 execution through an automatic PyTorch fallback. By training and benchmarking the same mini causal language model, we observed how hardware capability, numerical format, fused execution, and model scale influence training speed and memory consumption. We also inspected the internal scaling factors and amax history that support stable FP8 computation, which gives us a clearer understanding of how Transformer Engine manages reduced-precision arithmetic.

Check out the Full Codes. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Accelerating Transformer Training with NVIDIA Transformer Engine, Fused Kernels, BF16, FP8, and GPU Benchmarking appeared first on MarkTechPost.