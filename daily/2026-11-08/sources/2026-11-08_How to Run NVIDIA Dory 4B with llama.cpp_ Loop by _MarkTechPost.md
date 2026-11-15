---
publish_time: 1794079364
link: https://www.marktechpost.com/2026/11/07/coding-guide-nvidia-dory-4b-llama-cpp/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  NVIDIA Nemotron Labs 的小型推理模型 Dory 1.0 4B，其网络中间层构成一个共享块，可对每个 token 应用一次、两次、三次或四次。每增加一次“循环”就在不增加任何参数的情况下付出更多单 token 算力，使同一检查点可在四种算力预算下运行而无需重训。本文逐层构建 NVIDIA 模型卡锁定的 llama.cpp 分支、下载 3.7GB GGUF，并从文件直接读取架构以预测各循环次数的参数与缓存开销，进而用 GSM8K 配对评测观察精度、回答长度与耗时的变化。
---

# 如何在 llama.cpp 中运行 NVIDIA Dory 4B：逐层“循环”推理指南

> 原文链接：https://www.marktechpost.com/2026/11/07/coding-guide-nvidia-dory-4b-llama-cpp/
> 来源：MarkTechPost

In this tutorial, we work with Dory 1.0 4B, a small reasoning model from NVIDIA&#8217;s Nemotron Labs whose middle layers form a shared block that can be applied once, twice, three, or four times for every token. Each extra pass, or loop, spends more computation per token without adding a single parameter, so one checkpoint can run at four different compute budgets with no retraining. We build the llama.cpp branch that NVIDIA&#8217;s model card pins, download the 3.7 GB GGUF, and read the architecture straight from the file to predict what each loop should cost in parameters and cache memory. We then check those predictions against the running server, measure decode speed at every loop count, test whether the cheaper last-loop cache changes the model&#8217;s predictions, and run a paired GSM8K evaluation to see how accuracy, answer length, and time per solved question move as the loops increase.

Copy CodeCopiedUse a different Browser

import os
import re
import sys
import json
import time
import math
import random
import signal
import shutil
import hashlib
import platform
import statistics
import traceback
import subprocess
import collections
import urllib.request
from pathlib import Path

RESULTS = {}          # step -> one-line result, for the summary table
CLAIMS = []           # (step, claim, held)
CURRENT = ["1"]

def banner(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

def section(name):
    def wrap(fn):
        def run(*a, **kw):
            CURRENT[0] = name.split(".")[0]
            banner(name)
            t0 = time.time()
            try:
                out = fn(*a, **kw)
                RESULTS[name] = out if isinstance(out, str) else "ok"
                return out
            except Exception as e:
                RESULTS[name] = f"SKIPPED / FAILED -> {type(e).__name__}: {e}"
                print(f"\n[!] {name} did not complete: {type(e).__name__}: {e}")
                traceback.print_exc(limit=3)
                return None
            finally:
                print(f"\n[{time.time() - t0:.1f} s]")
        return run
    return wrap

def claim(text, held):
    CLAIMS.append((CURRENT[0], text, bool(held)))
    return held

banner("1. Build the pinned Dory llama.cpp fork and record the environment")
FORK = "https://github.com/brianchmielNV/llama.cpp.git"
FORK_COMMIT = "98a74c97ea09ac72f6ceda1559808fc0a2f447ce"     # the commit NVIDIA's model card pins; ggml-org PR #30306 is still a draft
GGUF_REPO = "nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-GGUF"
GGUF_REV = "df53755cb8741843af8e019e088819fbef17e29b"
GGUF_FILE = "NVIDIA-Nemotron-Labs-Dory1.0-4B-Q5_K_M.gguf"      # the card's commands call it dory-q5_k_m.gguf
GGUF_SIZE = 3_673_288_864
GGUF_SHA256 = "96080be49ffd67b916018b7bdef8c484762576fb52780e10ab98ac4978a660e0"
GSM8K_REV = "740312add88f781978c0658806c59bc2815b9866"
WORK = Path(os.environ.get("DORY_WORK") or ("/content/dory" if os.path.isdir("/content") else "dory_work")).resolve()
WORK.mkdir(parents=True, exist_ok=True)
(WORK / "logs").mkdir(exist_ok=True)
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "gguf==0.19.0", "huggingface_hub", "pandas", "pyarrow"], check=True)

SYSTEM = platform.system()
GPU = ""
if shutil.which("nvidia-smi"):
    q = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,compute_cap", "--format=csv,noheader"],
                       capture_output=True, text=True)
    GPU = q.stdout.strip().splitlines()[0] if q.returncode == 0 and q.stdout.strip() else ""
BACKEND = "metal" if SYSTEM == "Darwin" else ("cuda" if GPU else "cpu")
SRC = WORK / "llama.cpp-dory"
SERVER_BIN = SRC / "build" / "bin" / "llama-server"
free_gb = shutil.disk_usage(WORK).free / 1e9
print(f"{SYSTEM} {platform.machine()}, Python {platform.python_version()}, {os.cpu_count()} CPU cores, "
      f"backend {BACKEND}{' (' + GPU + ')' if GPU else ''}, {free_gb:.1f} GB free disk")

if not SERVER_BIN.exists():
    t0 = time.time()
    if not (SRC / ".git").exists():
        subprocess.run(["git", "init", "-q", str(SRC)], check=True)
        subprocess.run(["git", "-C", str(SRC), "remote", "add", "origin", FORK], check=True)
    subprocess.run(["git", "-C", str(SRC), "fetch", "-q", "--depth", "1", "origin", FORK_COMMIT], check=True)
    subprocess.run(["git", "-C", str(SRC), "checkout", "-q", "--detach", "FETCH_HEAD"], check=True)
    flags = ["-DCMAKE_BUILD_TYPE=Release", "-DLLAMA_BUILD_SERVER=ON", "-DLLAMA_BUILD_TESTS=OFF",
             "-DLLAMA_BUILD_EXAMPLES=OFF", "-DLLAMA_BUILD_APP=OFF", "-DLLAMA_BUILD_UI=OFF",
             "-DLLAMA_USE_PREBUILT_UI=ON", "-DLLAMA_OPENSSL=OFF"]
    if BACKEND == "metal":       # the card's Apple-silicon flags
        flags += ["-DCMAKE_OSX_ARCHITECTURES=arm64", "-DGGML_METAL=ON", "-DGGML_METAL_EMBED_LIBRARY=ON",
                  "-DGGML_BLAS=ON", "-DGGML_BLAS_VENDOR=Apple"]
    elif BACKEND == "cuda":      # kernels for this GPU only (a T4 is 7.5); flash-attention kernels are unused with --flash-attn off
        cap = GPU.split(",")[-1].strip().replace(".", "")
        flags += ["-DGGML_CUDA=ON", f"-DCMAKE_CUDA_ARCHITECTURES={cap}", "-DGGML_CUDA_FA=OFF", "-DGGML_NATIVE=OFF"]
    env = dict(os.environ, HF_UI_VERSION="b11551")
    with open(WORK / "build.log", "w") as log:
        subprocess.run(["cmake", "-S", str(SRC), "-B", str(SRC / "build")] + flags, check=True, env=env, stdout=log, stderr=log)
        subprocess.run(["cmake", "--build", str(SRC / "build"), "--parallel", str(os.cpu_count()), "--target", "llama-server"],
                       check=True, env=env, stdout=log, stderr=log)
    print(f"built llama-server in {time.time() - t0:.0f} s")
head = subprocess.run(["git", "-C", str(SRC), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
assert head == FORK_COMMIT, f"checked out {head}, expected {FORK_COMMIT}"
version = subprocess.run([str(SERVER_BIN), "--version"], capture_output=True, text=True)
print(f"fork commit {head[:12]}; {(version.stdout + version.stderr).strip().splitlines()[-1]}")
RESULTS["1. Build the pinned Dory llama.cpp fork and record the environment"] = f"fork {head[:12]}, backend {BACKEND}"

We build llama-server from the exact commit of the Dory branch that NVIDIA&#8217;s model card pins, because Dory support in llama.cpp is still an open draft pull request and no released binary can load the model. The cell detects the platform and passes the card&#8217;s Metal flags on a Mac, or compiles CUDA kernels for the attached GPU alone on Colab, skipping the flash-attention kernels that the card&#8217;s &#8211;flash-attn off never uses, which keeps a T4 build manageable. It then checks that the checked-out commit is the pinned one, so every later number traces to one known version of the code.

Copy CodeCopiedUse a different Browser

@section("2. Download the Q5_K_M GGUF at a pinned revision and check its SHA-256")
def download_step():
    global GGUF
    from huggingface_hub import hf_hub_download
    t0 = time.time()
    GGUF = Path(hf_hub_download(GGUF_REPO, GGUF_FILE, revision=GGUF_REV, local_dir=str(WORK)))
    h = hashlib.sha256()
    with open(GGUF, "rb") as f:
        for block in iter(lambda: f.read(1 << 24), b""):
            h.update(block)
    size, digest = GGUF.stat().st_size, h.hexdigest()
    print(f"{GGUF.name}: {size:,} bytes, sha256 {digest[:16]}...  ({time.time() - t0:.0f} s)")
    assert size == GGUF_SIZE and digest == GGUF_SHA256, "the file does not match the card's size and checksum"
    claim("the GGUF matches the size and SHA-256 published on the card", True)
    return f"{size / 1e9:.2f} GB, checksum matches the card"

download_step()

The Q5_K_M GGUF comes from Hugging Face at a fixed repository revision, and we hash it before anything else touches it. The card&#8217;s commands refer to the file as dory-q5_k_m.gguf, but the repository names it NVIDIA-Nemotron-Labs-Dory1.0-4B-Q5_K_M.gguf, so copying the card&#8217;s command verbatim fails; pinning the real name, the size, and the SHA-256 together catches both a wrong file and a corrupted download. The 3.67 GB file matches the card&#8217;s published checksum exactly, so every measurement that follows uses the same bytes NVIDIA published.

Copy CodeCopiedUse a different Browser

@section("3. Read the architecture from the GGUF: three layer groups and a default of four loops")
def architecture_step():
    global META, GROUPS, PATTERN
    import gguf
    reader = gguf.GGUFReader(str(GGUF))
    META = {k: f.contents() for k, f in reader.fields.items() if k.startswith("dory.")}
    for k in ("dory.block_count", "dory.input_layer_count", "dory.recurrent_layer_count", "dory.output_layer_count",
              "dory.num_loops", "dory.recurrent_kv_cache_mode", "dory.attention.sliding_window", "dory.context_length"):
        print(f"{k:34s} {META[k]}")
    PATTERN = META["dory.layer_pattern"].split("-")[:-1]           # one symbol per attention layer: S sliding window, * full
    n_in, n_rec = META["dory.input_layer_count"], META["dory.recurrent_layer_count"]
    print(f"\nlayer entries alternate attention and MLP: {len(PATTERN)} attention layers "
          f"({PATTERN.count('S')} sliding-window, {PATTERN.count('*')} full attention)")
    GROUPS = collections.defaultdict(lambda: {"params": 0, "bytes": 0})
    dtypes = collections.Counter()
    for t in reader.tensors:
        m = re.match(r"blk\.(\d+)\.", t.name)
        if m:
            i = int(m.group(1))
            g = "input block" if i < n_in else "recurrent block" if i < n_in + n_rec else "output block"
        else:
            g = "embedding" if t.name.startswith("token_embd") else "LM head"
        GROUPS[g]["params"] += int(math.prod(int(x) for x in t.shape))
        GROUPS[g]["bytes"] += int(t.n_bytes)
        dtypes[t.tensor_type.name] += 1
    print(f"\n{'group':16s} {'params':>9s} {'bytes':>9s}")
    for g in ("embedding", "input block", "recurrent block", "output block", "LM head"):
        print(f"{g:16s} {GROUPS[g]['params'] / 1e9:7.3f} B {GROUPS[g]['bytes'] / 1e9:6.3f} GB")
    print(f"tensor types: {dict(dtypes)}")
    claim("the GGUF stores 16 input, 40 recurrent and 16 output layer entries (8, 20 and 8 blocks)",
          (n_in, n_rec, META["dory.output_layer_count"]) == (16, 40, 16))
    claim("the GGUF's built-in loop count is 4, not the 2 the card recommends", META["dory.num_loops"] == 4)
    total = sum(v["params"] for v in GROUPS.values())
    return (f"{total / 1e9:.2f} B parameters, {GROUPS['recurrent block']['params'] / 1e9:.2f} B of them in the shared "
            f"recurrent block; built-in num_loops = {META['dory.num_loops']}")

architecture_step()

The GGUF header tells us how the model is wired before we load it. Dory&#8217;s 72 layer entries split into an input group of 16, a shared recurrent group of 40 and an output group of 16, alternating attention and MLP, with one full-attention layer for every three sliding-window layers. Summing tensor sizes by group shows the recurrent block accounts for 1.84 of the model&#8217;s 3.98 billion parameters. The header also carries a trap: its built-in loop count is 4, while the card recommends 2, so a server started without an override silently runs the most expensive setting.

Copy CodeCopiedUse a different Browser

LOOPS = (1, 2, 3, 4)
CTX, UBATCH = 4096, 512

def predicted_kv(loops, mode, ctx=CTX, ubatch=UBATCH):
    """KV cache under the fork's allocation rule: per_loop keeps one cache per loop for every recurrent attention layer,
    last_loop keeps one in all. Full-attention layers hold ctx cells; sliding-window layers hold window + ubatch, padded to 256."""
    n_in, n_rec = META["dory.input_layer_count"] // 2, META["dory.recurrent_layer_count"] // 2
    rec, fixed = PATTERN[n_in:n_in + n_rec], PATTERN[:n_in] + PATTERN[n_in + n_rec:]
    copies = loops if mode == "per_loop" else 1
    full = fixed.count("*") + copies * rec.count("*")
    swa = fixed.count("S") + copies * rec.count("S")
    swa_cells = min(ctx, -(-(META["dory.attention.sliding_window"] + ubatch) // 256) * 256)
    per_cell = 2 * META["dory.attention.head_count_kv"] * META["dory.attention.key_length"] * 2     # K and V, 2 bytes each
    return full, swa, (full * ctx + swa * swa_cells) * per_cell / 2**20

@section("4. Predict what each extra loop costs: parameters per token and KV-cache size")
def cost_model_step():
    global PER_TOKEN
    once = ("input block", "output block", "LM head")     # the embedding is a one-row lookup, so it costs no matrix work
    PER_TOKEN = {}
    print(f"{'loops':>5s} {'params per token':>17s} {'vs 1 loop':>10s} {'weight bytes read':>18s} {'vs 1 loop':>10s}")
    for n in LOOPS:
        p = sum(GROUPS[g]["params"] for g in once) + n * GROUPS["recurrent block"]["params"]
        b = sum(GROUPS[g]["bytes"] for g in once) + n * GROUPS["recurrent block"]["bytes"]
        PER_TOKEN[n] = (p, b)
        print(f"{n:5d} {p / 1e9:15.2f} B {p / PER_TOKEN[1][0]:9.2f}x {b / 1e9:16.2f} GB {b / PER_TOKEN[1][1]:9.2f}x")
    print(f"\npredicted KV cache at --ctx-size {CTX}, f16 keys and values, micro-batch {UBATCH}:")
    print(f"{'loops':>5s}   {'per_loop: full + SWA layers':>28s} {'MiB':>7s}   {'last_loop: full + SWA layers':>29s} {'MiB':>7s}")
    for n in LOOPS:
        a, b = predicted_kv(n, "per_loop"), predicted_kv(n, "last_loop")
        print(f"{n:5d}   {a[0]:>21d} + {a[1]:<4d} {a[2]:7.1f}   {b[0]:>22d} + {b[1]:<4d} {b[2]:7.1f}")
    full_ctx = META["dory.context_length"]
    print(f"\nat the full {full_ctx:,}-token context: per_loop {predicted_kv(2, 'per_loop', full_ctx)[2] / 1024:.1f} GiB at 2 loops "
          f"and {predicted_kv(4, 'per_loop', full_ctx)[2] / 1024:.1f} GiB at 4; last_loop "
          f"{predicted_kv(4, 'last_loop', full_ctx)[2] / 1024:.1f} GiB at any loop count")
    return (f"4 loops apply {PER_TOKEN[4][0] / PER_TOKEN[1][0]:.2f}x the parameters per token of 1 loop; predicted KV at 4 loops "
            f"{predicted_kv(4, 'per_loop')[2]:.0f} MiB per_loop vs {predicted_kv(4, 'last_loop')[2]:.0f} MiB last_loop")

cost_model_step()

From those group sizes, we can predict what a loop costs before running anything. A token passes through the input block, the recurrent block once per loop, the output block, and the LM head, so 4 loops apply 2.51 times the parameters of 1 loop and read 2.28 times the weight bytes, the better guide for a memory-bound decoder. The KV cache follows the fork&#8217;s allocation rule: per_loop keeps a separate cache for every loop of every recurrent attention layer, growing from 306 MiB at 1 loop to 816 MiB at 4 for a 4,096-token context, while last_loop stays at 306 MiB.

Copy CodeCopiedUse a different Browser

PORT = 8090
KV_LINE = re.compile(r"llama_kv_cache: size =\s*([\d.]+) MiB \(\s*(\d+) cells,\s*(\d+) layers")

class DoryServer:
    """llama-server with one loop count and KV mode. Both are read when the model loads, so each setting is a fresh start."""

    def __init__(self, loops=None, mode="per_loop", ngl=999, ubatch=UBATCH):
        self.loops, self.mode, self.ngl, self.ubatch = loops, mode, ngl, ubatch
        self.name = f"{'default' if loops is None else loops}-{mode}-ngl{ngl}-ub{ubatch}"

    def __enter__(self):
        cmd = [str(SERVER_BIN), "-m", str(GGUF), "--host", "127.0.0.1", "--port", str(PORT), "-ngl", str(self.ngl),
               "--ctx-size", str(CTX), "--parallel", "1", "--batch-size", str(self.ubatch), "--ubatch-size", str(self.ubatch),
               "--cache-type-k", "f16", "--cache-type-v", "f16", "--flash-attn", "off", "--no-context-shift",
               "--jinja", "--reasoning", "on", "--temp", "1.0", "--top-p", "0.95", "--top-k", "0", "--min-p", "0",
               "--repeat-penalty", "1"]
        if self.loops is not None:
            cmd += ["--override-kv", f"dory.num_loops=int:{self.loops},dory.recurrent_kv_cache_mode=str:{self.mode}"]
        self.log = WORK / "logs" / f"server-{self.name}.log"
        with open(self.log, "w") as f:
            self.proc = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
        t0 = time.time()
        while True:
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=2) as r:
                    if r.status == 200:
                        break
            except Exception:
                pass
            if self.proc.poll() is not None or time.time() - t0 > 600:
                self.stop()
                raise RuntimeError(f"llama-server did not start; see {self.log}")
            time.sleep(0.5)
        self.load_s = time.time() - t0
        text = self.log.read_text(errors="ignore")
        sizes = KV_LINE.findall(text)                       # the full-attention cache first, then the sliding-window cache
        self.kv_mib = sum(float(s[0]) for s in sizes)
        self.kv_layers = tuple(int(s[2]) for s in sizes)
        m = re.search(r"offloaded (\d+)/(\d+) layers", text)
        self.offloaded = f"{m.group(1)}/{m.group(2)}" if m else "n/a"
        return self

    def __exit__(self, *exc):
        self.stop()

    def stop(self):
        if self.proc.poll() is None:
            os.killpg(self.proc.pid, signal.SIGTERM)
            try:
                self.proc.wait(60)
            except subprocess.TimeoutExpired:
                os.killpg(self.proc.pid, signal.SIGKILL)
                self.proc.wait()

    def post(self, path, payload, timeout=1800):
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", data=json.dumps(payload).encode(),
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())

def split_reasoning(message):
    """The server returns the thinking in reasoning_content when it can parse it; otherwise it stays inside <think> tags."""
    content, reasoning = message.get("content") or "", message.get("reasoning_content") or ""
    m = re.search(r"<think>(.*?)</think>", content, re.S)
    if m:
        reasoning, content = reasoning + m.group(1), content.replace(m.group(0), "")
    return reasoning.strip(), content.strip()

@section("5. Start the server, prove the loop override took effect, and catch the silent default")
def override_step():
    rows = []
    for loops, mode in ((2, "per_loop"), (2, "last_loop"), (None, "per_loop")):
        with DoryServer(loops, mode) as s:
            want = predicted_kv(META["dory.num_loops"] if loops is None else loops, mode)
            rows.append((s.name, s.kv_layers, s.kv_mib, want, s.offloaded, s.load_s))
            if loops == 2 and mode == "per_loop":
                r = s.post("/v1/chat/completions", {"messages": [{"role": "user", "content": "What is 17 multiplied by 23?"}],
                                                    "max_tokens": 1024, "seed": 1, "cache_prompt": False})
                reasoning, answer = split_reasoning(r["choices"][0]["message"])
                print(f"2 loops, a first request: {r['usage']['completion_tokens']} tokens, "
                      f"{len(reasoning.split())} words of reasoning, answer: {answer[:120]!r}")
                print(f"   fields in the message: {sorted(r['choices'][0]['message'])}; "
                      f"timings: {sorted(r.get('timings', {}))[:6]}...\n")
    print(f"{'server':28s} {'KV layers (full, SWA)':>22s} {'KV MiB':>8s} {'predicted':>16s} {'offloaded':>10s} {'load s':>7s}")
    for name, layers, mib, want, off, load in rows:
        print(f"{name:28s} {str(layers):>22s} {mib:8.1f} {str(want[:2]) + f' {want[2]:.1f}':>16s} {off:>10s} {load:7.1f}")
    ok = all(layers == want[:2] for _, layers, _, want, _, _ in rows)
    claim("the --override-kv loop count and cache mode are applied (KV layer counts match the prediction)", ok)
    default = rows[-1]
    claim("without an override the server runs the GGUF's 4 loops (the most expensive setting)",
          default[1] == predicted_kv(4, "per_loop")[:2])
    return f"override applied: {ok}; no override -> {default[1]} KV layers, {default[2]:.0f} MiB, i.e. 4 loops"

override_step()

Loop count and cache mode are read when the model loads, so each setting needs its own server process; the DoryServer helper starts one per configuration, waits for the health check, and parses the KV-cache lines from the server&#8217;s log. We compare the parsed layer counts with the prediction to prove an override actually took effect, rather than trusting the flag. We also start one server without any override as a negative control, and send one chat request to see how the server separates the model&#8217;s reasoning from its answer.

Copy CodeCopiedUse a different Browser

CONFIGS = [(1, "per_loop"), (2, "per_loop"), (2, "last_loop"), (3, "per_loop"), (3, "last_loop"), (4, "per_loop"), (4, "last_loop")]
SPEED_PROMPT = ("Explain, step by step, how a recurrent block that is applied several times per token changes the amount of "
                "computation a language model spends on each token, and what that means for memory and latency.")

@section("6. Measure KV memory and decode speed for every loop count and cache mode")
def sweep_step():
    global SPEED
    SPEED = {}
    print(f"{'loops':>5s} {'mode':10s} {'KV MiB':>8s} {'predicted':>9s} {'prefill tok/s':>14s} {'decode tok/s':>13s} "
          f"{'decode vs 1 loop':>17s} {'params ratio':>13s}")
    for loops, mode in CONFIGS:
        with DoryServer(loops, mode) as s:
            runs = [s.post("/completion", {"prompt": SPEED_PROMPT, "n_predict": 192, "temperature": 0, "ignore_eos": True,
                                           "cache_prompt": False, "seed": 1})["timings"] for _ in range(3)]
            dec = statistics.median(t["predicted_per_second"] for t in runs)
            pre = statistics.median(t["prompt_per_second"] for t in runs)
            SPEED[(loops, mode)] = {"kv_mib": s.kv_mib, "kv_layers": s.kv_layers, "decode": dec, "prefill": pre,
                                    "decode_runs": [round(t["predicted_per_second"], 2) for t in runs]}
        base = SPEED[(1, "per_loop")]["decode"]
        print(f"{loops:5d} {mode:10s} {s.kv_mib:8.1f} {predicted_kv(loops, mode)[2]:9.1f} {pre:14.1f} {dec:13.1f} "
              f"{base / dec:16.2f}x {PER_TOKEN[loops][0] / PER_TOKEN[1][0]:12.2f}x")
    flat = len({round(SPEED[(n, 'last_loop')]['kv_mib'], 1) for n in (2, 3, 4)} | {round(SPEED[(1, 'per_loop')]['kv_mib'], 1)}) == 1
    grows = SPEED[(1, "per_loop")]["kv_mib"] < SPEED[(2, "per_loop")]["kv_mib"] < SPEED[(3, "per_loop")]["kv_mib"] < SPEED[(4, "per_loop")]["kv_mib"]
    claim("last_loop keeps the KV cache at the one-loop size for every loop count", flat)
    claim("per_loop KV memory grows with every added loop", grows)
    slow = SPEED[(1, "per_loop")]["decode"] / SPEED[(4, "per_loop")]["decode"]
    json.dump({f"{k[0]}-{k[1]}": v for k, v in SPEED.items()}, open(WORK / "speed.json", "w"), indent=1)
    return (f"KV {SPEED[(1, 'per_loop')]['kv_mib']:.0f} MiB at 1 loop; 4 loops: {SPEED[(4, 'per_loop')]['kv_mib']:.0f} MiB per_loop, "
            f"{SPEED[(4, 'last_loop')]['kv_mib']:.0f} MiB last_loop; decode {slow:.2f}x slower at 4 loops than at 1")

sweep_step()

With the helper in place, we start a server for each of seven settings, one to four loops in both cache modes, and record the measured KV memory next to the prediction. Decode speed comes from the server&#8217;s own timings on a fixed prompt, generating 192 tokens greedily three times and keeping the median, so the only thing that changes between rows is the loop setting. Dividing the one-loop speed by each row&#8217;s speed gives the measured slowdown, which we set beside the predicted ratios to see whether decoding behaves as compute-bound or memory-bound.

Copy CodeCopiedUse a different Browser

def top_probs(response):
    """Next-token candidates as {token: logprob}, from either of the server's two probability formats."""
    first = response["completion_probabilities"][0]
    if "top_logprobs" in first:
        return {c["token"]: c["logprob"] for c in first["top_logprobs"]}
    return {c["tok_str"]: math.log(max(c["prob"], 1e-30)) for c in first["probs"]}

GATE_PROMPTS = ["The capital of France is", "def fibonacci(n):\n    ", "Water boils at a temperature of",
                "In 1969, the first humans to walk on the Moon were", "The derivative of x squared is"]

@section("7. Correctness gates: the same seed gives the same answer, and the GPU agrees with the CPU")
def gates_step():
    payload = {"messages": [{"role": "user", "content": "Name three prime numbers greater than 50."}],
               "max_tokens": 512, "seed": 7, "cache_prompt": False}
    probe = lambda s, p: top_probs(s.post("/completion", {"prompt": p, "n_predict": 1, "n_probs": 10, "temperature": 0,
                                                          "cache_prompt": False}))
    with DoryServer(2, "per_loop") as s:
        a, b = (s.post("/v1/chat/completions", payload) for _ in range(2))
        same = a["choices"][0]["message"] == b["choices"][0]["message"]
        accel = [probe(s, p) for p in GATE_PROMPTS]
    print(f"two sampled chat answers with seed 7 at temperature 1.0: identical = {same}")
    with DoryServer(2, "per_loop", ngl=0) as s:
        cpu = [probe(s, p) for p in GATE_PROMPTS]
    agree, gaps = 0, []
    for p, x, y in zip(GATE_PROMPTS, accel, cpu):
        tx, ty = max(x, key=x.get), max(y, key=y.get)
        agree += tx == ty
        gaps += [abs(x[t] - y[t]) for t in set(x) & set(y)]
        print(f"   {p[:40]!r:44s} {BACKEND}: {tx!r:12s} CPU: {ty!r:12s}")
    print(f"{BACKEND} vs CPU: top-1 token agrees on {agree} of {len(GATE_PROMPTS)} prompts; largest log-probability gap "
          f"over shared top-10 tokens {max(gaps):.3f}")
    claim("a fixed seed reproduces a sampled answer exactly", same)
    claim(f"the {BACKEND} build agrees with the CPU build on the top-1 token", agree >= len(GATE_PROMPTS) - 1)
    return f"seeded answers identical: {same}; {BACKEND} vs CPU top-1 agreement {agree}/{len(GATE_PROMPTS)}"

gates_step()

Comparisons between settings are only meaningful if the measurements repeat and the accelerated build computes the same model as the reference CPU path. Two chat requests with the same seed at the card&#8217;s sampling temperature must return identical messages, otherwise per-question comparisons would mix model behaviour with sampling noise. We then start a CPU-only server, with no layers offloaded, and compare the most likely next token on five prompts against the GPU or Metal server, because Dory support has not been reviewed upstream on every backend.

Copy CodeCopiedUse a different Browser

def load_gsm8k():
    import pandas as pd
    from huggingface_hub import hf_hub_download
    path = hf_hub_download("openai/gsm8k", "main/test-00000-of-00001.parquet", repo_type="dataset", revision=GSM8K_REV,
                           local_dir=str(WORK / "gsm8k"))
    df = pd.read_parquet(path)
    df["gold"] = df.answer.str.extract(r"####\s*([-\d,\.]+)")[0].str.replace(",", "").astype(float)
    return df

def tv_distance(p, q):
    """Total-variation distance between two top-k next-token distributions, each renormalised over its own top k."""
    zp, zq = sum(math.exp(v) for v in p.values()), sum(math.exp(v) for v in q.values())
    return 0.5 * sum(abs(math.exp(p.get(t, -1e9)) / zp - math.exp(q.get(t, -1e9)) / zq) for t in set(p) | set(q))

@section("8. What an extra loop changes: next-token distributions on 50 prompts")
def mechanism_step():
    global GSM8K
    GSM8K = load_gsm8k()
    prompts = list(GSM8K.sample(50, random_state=11).question)
    configs = [(n, m, ub) for ub in (UBATCH, 16) for n in (1, 2, 4) for m in ("per_loop", "last_loop")]
    dist, lengths = {}, []
    for n, m, ub in configs:
        with DoryServer(n, m, ubatch=ub) as s:
            got = [s.post("/completion", {"prompt": p, "n_predict": 1, "n_probs": 20, "temperature": 0, "cache_prompt": False})
                   for p in prompts]
            dist[(n, m, ub)] = [top_probs(r) for r in got]
            lengths = lengths or [r["timings"]["prompt_n"] for r in got]
    print(f"50 GSM8K questions as raw prompts, {min(lengths)} to {max(lengths)} tokens: one chunk at a {UBATCH}-token "
          f"micro-batch, {math.ceil(min(lengths) / 16)} to {math.ceil(max(lengths) / 16)} chunks at 16\n")
    print(f"{'comparison':52s} {'same top-1':>10s} {'mean TV':>8s} {'max |dlogp|':>12s}")

    def compare(label, a, b):
        x, y = dist[a], dist[b]
        same = sum(max(p, key=p.get) == max(q, key=q.get) for p, q in zip(x, y))
        tv = statistics.mean(tv_distance(p, q) for p, q in zip(x, y))
        mx = max(abs(p[t] - q[t]) for p, q in zip(x, y) for t in set(p) & set(q))
        print(f"{label:52s} {same:>7d}/50 {tv:8.4f} {mx:12.5f}")
        return same, tv, mx
    out = {}
    out["modes_1"] = compare("1 loop: per_loop vs last_loop", (1, "per_loop", UBATCH), (1, "last_loop", UBATCH))
    for n in (2, 4):
        out[f"modes_{n}"] = compare(f"{n} loops: per_loop vs last_loop, one {UBATCH}-token chunk",
                                    (n, "per_loop", UBATCH), (n, "last_loop", UBATCH))
        out[f"chunks_{n}"] = compare(f"{n} loops: per_loop vs last_loop, 16-token chunks", (n, "per_loop", 16), (n, "last_loop", 16))
    print()
    out["1v2"] = compare("1 loop vs 2 loops (per_loop)", (1, "per_loop", UBATCH), (2, "per_loop", UBATCH))
    out["2v4"] = compare("2 loops vs 4 loops (per_loop)", (2, "per_loop", UBATCH), (4, "per_loop", UBATCH))
    out["1v4"] = compare("1 loop vs 4 loops (per_loop)", (1, "per_loop", UBATCH), (4, "per_loop", UBATCH))
    claim("with the prompt in one chunk, last_loop gives the same next-token distribution as per_loop",
          all(out[f"modes_{n}"][2] == 0 for n in (1, 2, 4)))
    claim("split into small chunks, last_loop and per_loop disagree at 2 and 4 loops",
          all(out[f"chunks_{n}"][1] > 0 for n in (2, 4)))
    return (f"top-1 agreement 1 vs 4 loops {out['1v4'][0]}/50 (mean TV {out['1v4'][1]:.3f}); last_loop = per_loop in one chunk: "
            f"{all(out[f'modes_{n}'][2] == 0 for n in (1, 2, 4))}")

mechanism_step()

Next-token distributions show what a loop changes inside the model at almost no cost. For 50 GSM8K questions used as raw prompts, we request the top 20 next-token candidates under each setting and compare them by top-1 agreement and total-variation distance. The fork&#8217;s code implies a sharp prediction: last_loop overwrites a recurrent layer&#8217;s cache on every loop, so it can differ from per_loop only when earlier chunks of the prompt keep just their final-loop keys, which never happens when the whole prompt fits in one micro-batch. Repeating the probe with 16-token micro-batches tests exactly that.

Copy CodeCopiedUse a different Browser

EVAL_CONFIGS = [(1, "per_loop"), (2, "per_loop"), (2, "last_loop"), (4, "per_loop"), (4, "last_loop")]
N_QUESTIONS = 30
MAX_TOKENS = 2048
INSTRUCTION = "\n\nSolve the problem. End your reply with a last line of the form 'Final answer: <number>'."

def grade(text, gold):
    m = re.findall(r"Final answer:\s*\$?\s*(-?[\d,]*\.?\d+)", text)
    nums = m or re.findall(r"-?[\d,]*\.?\d+", text)
    if not nums:
        return False
    try:
        return abs(float(nums[-1].replace(",", "")) - gold) < 1e-6
    except ValueError:
        return False

@section("9. Paired GSM8K evaluation across loop counts and cache modes")
def eval_step():
    global EVAL, SAMPLE
    SAMPLE = GSM8K.sample(N_QUESTIONS, random_state=20261106).reset_index()
    EVAL = {}
    for loops, mode in EVAL_CONFIGS:
        path = WORK / f"gsm8k-{loops}-{mode}.jsonl"
        done = {json.loads(l)["i"]: json.loads(l) for l in open(path)} if path.exists() else {}
        todo = [i for i in range(len(SAMPLE)) if i not in done]
        if todo:
            with DoryServer(loops, mode) as s, open(path, "a") as f:
                for i in todo:
                    row = SAMPLE.iloc[i]
                    t0 = time.time()
                    r = s.post("/v1/chat/completions", {"messages": [{"role": "user", "content": row.question + INSTRUCTION}],
                                                        "max_tokens": MAX_TOKENS, "seed": 1000 + i, "cache_prompt": False})
                    reasoning, answer = split_reasoning(r["choices"][0]["message"])
                    rec = {"i": i, "correct": grade(answer, row.gold), "tokens": r["usage"]["completion_tokens"],
                           "finish": r["choices"][0]["finish_reason"], "wall_s": round(time.time() - t0, 2),
                           "decode_tps": round(r["timings"]["predicted_per_second"], 2), "answer": answer[-200:]}
                    f.write(json.dumps(rec) + "\n")
                    f.flush()
                    done[i] = rec
        EVAL[(loops, mode)] = [done[i] for i in range(len(SAMPLE))]
        rows = EVAL[(loops, mode)]
        acc = sum(r["correct"] for r in rows)
        print(f"{loops} loops {mode:9s}: {acc:2d}/{len(rows)} correct, median {statistics.median(r['tokens'] for r in rows):6.0f} "
              f"tokens, {sum(r['finish'] == 'length' for r in rows)} cut off at {MAX_TOKENS}, "
              f"median {statistics.median(r['wall_s'] for r in rows):5.1f} s per question")
    return "; ".join(f"{n}/{m[:4]} {sum(r['correct'] for r in EVAL[(n, m)])}/{N_QUESTIONS}" for n, m in EVAL_CONFIGS)

eval_step()

The paired GSM8K evaluation asks the same seeded sample of questions under five settings, with reasoning on, the card&#8217;s sampling settings and a fixed seed per question, so each question meets the same conditions at every loop count. For every reply, we record correctness against the dataset&#8217;s final answer, the number of generated tokens (including reasoning), whether the reply hit the 2,048-token limit, and the wall time. Results go to one JSONL file per setting as they arrive, so an interrupted Colab session resumes where it stopped.

Copy CodeCopiedUse a different Browser

def mcnemar(a, b):
    """Exact two-sided McNemar p-value from paired booleans."""
    only_a = sum(x and not y for x, y in zip(a, b))
    only_b = sum(y and not x for x, y in zip(a, b))
    n, k = only_a + only_b, min(only_a, only_b)
    p = 1.0 if n == 0 else min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n)
    return only_a, only_b, p

def wilson(k, n, z=1.96):
    c = (k + z * z / 2) / (n + z * z)
    h = z * math.sqrt(k * (n - k) / n + z * z / 4) / (n + z * z)
    return 100 * (c - h), 100 * (c + h)

@section("10. Statistics: accuracy, tokens and time per solved question")
def stats_step():
    global STATS
    rng = random.Random(7)
    ref = EVAL[(1, "per_loop")]
    print(f"{'setting':18s} {'accuracy':>9s} {'95% CI':>13s} {'median tokens':>14s} {'tokens vs 1 loop [95% CI]':>27s} "
          f"{'s per solved':>13s}")
    STATS = {}
    for key in EVAL_CONFIGS:
        rows = EVAL[key]
        k, n = sum(r["correct"] for r in rows), len(rows)
        ratios = [r["tokens"] / q["tokens"] for r, q in zip(rows, ref)]
        boots = sorted(statistics.median(rng.choices(ratios, k=len(ratios))) for _ in range(2000))
        per_solved = sum(r["wall_s"] for r in rows) / max(k, 1)
        STATS[key] = {"acc": k / n, "ratio": statistics.median(ratios), "ratio_ci": (boots[50], boots[1949]), "per_solved": per_solved,
                      "tokens": statistics.median(r["tokens"] for r in rows)}
        lo, hi = wilson(k, n)
        print(f"{key[0]} loops {key[1]:9s} {100 * k / n:8.1f}% {lo:5.1f}-{hi:5.1f}% {STATS[key]['tokens']:14.0f} "
              f"{STATS[key]['ratio']:12.2f} [{boots[50]:.2f}, {boots[1949]:.2f}] {per_solved:12.1f}")
    print("\npaired accuracy contrasts (McNemar exact; 'only A' = questions only the first setting solved)")
    pairs = [((2, "per_loop"), (1, "per_loop")), ((4, "per_loop"), (1, "per_loop")), ((4, "per_loop"), (2, "per_loop")),
             ((2, "last_loop"), (2, "per_loop")), ((4, "last_loop"), (4, "per_loop"))]
    for a, b in pairs:
        oa, ob, p = mcnemar([r["correct"] for r in EVAL[a]], [r["correct"] for r in EVAL[b]])
        print(f"   {a[0]} {a[1]:9s} vs {b[0]} {b[1]:9s}: only A {oa:2d}, only B {ob:2d}, p = {p:.3f}")
        STATS[(a, b)] = (oa, ob, p)
    fewer = STATS[(4, "per_loop")]["ratio_ci"][1] < 1
    claim("on GSM8K, 4 loops need fewer generated tokens than 1 loop (95% CI of the median ratio below 1)", fewer)
    return (f"accuracy {', '.join(f'{k[0]}/{k[1][:4]} {100 * STATS[k]['acc']:.0f}%' for k in EVAL_CONFIGS)}; "
            f"tokens at 4 loops {STATS[(4, 'per_loop')]['ratio']:.2f}x those at 1 loop")

stats_step()

Thirty paired questions cannot settle small accuracy differences, so the statistics cell is built to say what the sample can and cannot show. Accuracy comes with Wilson intervals, and each contrast uses an exact McNemar test on the questions that only one setting solved. Token counts are compared as the median of per-question ratios against one loop, with a bootstrap interval, which tests the card&#8217;s claim that more loops need fewer generated tokens. Time per solved question combines speed, length, and accuracy into the number a user actually pays for.

Copy CodeCopiedUse a different Browser

@section("11. The card's claims against this run")
def claims_step():
    s, sp = STATS, SPEED
    rows = [
        ("The GGUF runs 2 loops by default", f"built-in num_loops = {META['dory.num_loops']}", META["dory.num_loops"] == 2),
        ("Last-loop caching keeps the KV footprint at the one-loop size",
         f"{sp[(1, 'per_loop')]['kv_mib']:.0f} MiB at 1 loop, {sp[(4, 'last_loop')]['kv_mib']:.0f} at 4 last_loop",
         round(sp[(1, "per_loop")]["kv_mib"]) == round(sp[(4, "last_loop")]["kv_mib"])),
        ("Per-loop KV memory grows with the loop count",
         " / ".join(f"{sp[(n, 'per_loop')]['kv_mib']:.0f}" for n in LOOPS) + " MiB",
         sp[(4, "per_loop")]["kv_mib"] > sp[(1, "per_loop")]["kv_mib"]),
        ("Loop count trades compute per token without a model swap",
         f"decode {sp[(1, 'per_loop')]['decode']:.1f} -> {sp[(4, 'per_loop')]['decode']:.1f} tok/s, same file",
         sp[(4, "per_loop")]["decode"] < sp[(1, "per_loop")]["decode"]),
        ("More loops solve tasks with fewer generated tokens",
         f"GSM8K median ratio at 4 loops {s[(4, 'per_loop')]['ratio']:.2f} [{s[(4, 'per_loop')]['ratio_ci'][0]:.2f}, "
         f"{s[(4, 'per_loop')]['ratio_ci'][1]:.2f}]", s[(4, "per_loop")]["ratio_ci"][1] < 1),
        ("Last-loop accuracy stays close to per-loop",
         f"4 loops: {100 * s[(4, 'last_loop')]['acc']:.0f}% vs {100 * s[(4, 'per_loop')]['acc']:.0f}%, "
         f"McNemar p = {s[((4, 'last_loop'), (4, 'per_loop'))][2]:.2f}", s[((4, "last_loop"), (4, "per_loop"))][2] > 0.05),
    ]
    print(f"{'claim (model card)':60s} {'this run':48s} verdict")
    for text, found, ok in rows:
        print(f"{text:60s} {found:48s} {'holds' if ok else 'does not hold'}")
        claim(text, ok)
    print(f"\nnot testable here: the benchmark table (SWE-bench, Terminal-Bench, GPQA ...), the 256K context, NVFP4 pre-training;"
          f"\nwith {N_QUESTIONS} paired questions only large accuracy differences are resolvable")
    return f"{sum(bool(ok) for *_, ok in rows)} of {len(rows)} card claims hold in this run"

claims_step()

Rather than restate the model card, we check its claims against this run. Each row pairs a sentence from the card with the measurement that tests it: cache-size claims and the loop defaults to token efficiency and the accuracy of last-loop caching, and the verdict comes from the saved results rather than being typed by hand. Claims the notebook cannot reach, such as the benchmark table, the 256K context and the NVFP4 pre-training, are listed as untested rather than quietly dropped.

Copy CodeCopiedUse a different Browser

banner("SUMMARY")
for name, res in RESULTS.items():
    print(f"  {name:<100s}  {res}")
print("\nchecks decided in this run:")
for step, text, held in CLAIMS:
    print(f"   [{'held' if held else 'did not hold'}] step {step}: {text}")
failed = [k for k, v in RESULTS.items() if str(v).startswith("SKIPPED")]
print(f"\n{sum(h for *_, h in CLAIMS)} of {len(CLAIMS)} checks held; steps failed or skipped: {failed or 'none'}")
print(f"llama.cpp fork {FORK_COMMIT[:12]}, GGUF @ {GGUF_REV[:7]}, backend {BACKEND}{' ' + GPU if GPU else ''}, "
      f"Python {platform.python_version()}")

The summary prints each step&#8217;s one-line result and every check the run decided, marking which passed and which failed, along with the fork commit, the GGUF revision, and the backend, so the notebook doubles as a record of exactly what was verified and on which hardware.

In conclusion, Dory turns test-time compute into a load-time setting: one 3.7 GB file runs as four different models, from a single pass through its 20-block recurrent core to four, and the GGUF header alone predicts what each setting costs in parameters and cache memory. The notebook checks those predictions against the server, measures speed, tests the last-loop cache against a precise prediction from the code, and evaluates accuracy and answer length on a paired GSM8K sample. Two practical lessons hold whatever the measurements show: always set the loop count explicitly, because the GGUF defaults to four, and pin the fork commit, because Dory support in llama.cpp is still an open draft.

Check out the FULL CODES here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post How to Run NVIDIA Dory 4B with llama.cpp: Loop by Loop Guide appeared first on MarkTechPost.