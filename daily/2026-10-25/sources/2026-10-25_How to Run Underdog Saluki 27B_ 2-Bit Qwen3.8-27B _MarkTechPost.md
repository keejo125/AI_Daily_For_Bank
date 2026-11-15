---
publish_time: 1792895418
link: https://www.marktechpost.com/2026/10/24/underdog-saluki-27b-coding-guide-llama-cpp/
source: MarkTechPost
status: confirmed
category: 国内
is_model_related: true
digest: |
  本文实战演示如何运行 Underdog Saluki 27B——一个 7.9GB、基于 ISTA-DASLab GSQ-RCO 量化的 Qwen3.8-27B 构建，声称在约 2 bit/权重下保留工具调用能力，并在其自有 120 任务基准上小幅超越 54GB 完整模型。作者将 Saluki 与原始 GGUF 在原生 llama.cpp 中并置对比：逐张量比对文件头、字节级比较辨明是否只是 ISTA 权重“混音”，再在单卡上实测显存与速度，并用 Berkeley Function Calling Leaderboard（BFCL）严格的与宽松的解析对两者在同源 120 任务上打分。文章附带完整复现脚本，是一份面向本地部署的量化模型评测教程。
---

# Underdog Saluki 27B 上手指南：2-bit 量化 Qwen3.8-27B 工具调用

> 原文链接：https://www.marktechpost.com/2026/10/24/underdog-saluki-27b-coding-guide-llama-cpp/
> 来源：MarkTechPost

In this tutorial, we work with Underdog Saluki 27B, a 7.9 GB build of Qwen3.8-27B that its makers say keeps tool calling intact at about two bits per weight and even edges out the full 54 GB model on their own 120-task benchmark. Saluki is built on ISTA-DASLab&#8217;s GSQ-RCO quantization of the same model, so we put both files side by side in stock llama.cpp. We start with the files themselves: a tensor-by-tensor diff of the two GGUF headers, then a byte-level comparison that shows whether Saluki is a remix of ISTA&#8217;s bits or a changed model. We then serve each file on one GPU, read its memory and speed, and score both on the same seeded 120 tasks from the Berkeley Function Calling Leaderboard, using BFCL&#8217;s own checker with strict and lenient parsing.

Copy CodeCopiedUse a different Browser

import os
import re
import ast
import sys
import json
import math
import copy
import enum
import glob
import time
import types
import random
import shutil
import struct
import hashlib
import tarfile
import platform
import traceback
import subprocess
import collections
import urllib.request
import urllib.error

RESULTS = {}          # step -> one-line result, for the summary table
CLAIMS = []           # (step, claim, held) rows; held is True, False or None (not decided in this run)
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
                json.dump({"results": RESULTS, "claims": CLAIMS}, open(os.path.join(WORK, "results.json"), "w"), indent=1)
        return run
    return wrap

def claim(text, held):
    CLAIMS.append((CURRENT[0], text, held))
    return held

banner("1. Platform, pins and helpers")
SYSTEM, MACHINE = platform.system(), platform.machine()
ON_CUDA = SYSTEM == "Linux" and shutil.which("nvidia-smi") is not None
assert ON_CUDA or (SYSTEM == "Darwin" and MACHINE == "arm64"), "needs an NVIDIA GPU on Linux (Colab T4) or an Apple-silicon Mac"
WORK = os.environ.get("SALUKI_WORK") or ("/content/saluki" if os.path.isdir("/content") else os.path.abspath("saluki_work"))
for d in ("models", "llama", "bfcl", "runs"):
    os.makedirs(os.path.join(WORK, d), exist_ok=True)

# Everything the notebook downloads is pinned by size and SHA-256.
LLAMA_TAG = "b11565"   # llama.cpp release of 2026-10-12, commit f9a95aeb2
LLAMA_ASSET = {"Linux": ("llama-b11565-bin-ubuntu-cuda-12.8-x64.tar.gz", 171559844,
                         "61b8cf4e49739afe4008b06a92390dff999e706e9e7e9749c015544a9f241627"),
               "Darwin": ("llama-b11565-bin-macos-arm64.tar.gz", 12105509,
                          "19289548468babcd5131cecccf3a9bc7c67030cc7f0a978dafc0db1ba7891068")}[SYSTEM]
MODELS = {
    "Saluki": dict(repo="ConwayResearch/Underdog-Saluki-27B-1.0", rev="4f60eba09f4b6db63c72915d328d97e1d93edb8c",
                   file="Underdog-Saluki-27B-1.0-IQ2-mix.gguf", size=7898369152,
                   sha256="4a673518b11b1c4445f9b9a9d3c40356f5ba39f6a6260dcb25f3fbfd475d9efb"),
    "ISTA": dict(repo="ISTA-DASLab/Qwen3.8-27B-GSQ-RCO-GGUF", rev="d562806dbafae37109975e970aae91b43e73b440",
                 file="Qwen3.8-27B-GSQ-RCO-IQ2_XS.gguf", size=8422841472,
                 sha256="f0ae5006da0ce6225935339e4e989369f94de95d2263cf969519f8420c9ae02c"),
}
# BFCL v4 data and BFCL's own checker code, at one gorilla commit.
GORILLA = ("https://raw.githubusercontent.com/ShishirPatil/gorilla/6ea57973c7a6097fd7c5915698c54c17c5b1b6c8/"
           "berkeley-function-call-leaderboard/bfcl_eval/")
BFCL_FILES = {
    "data/BFCL_v4_simple_python.json": "82dd63ba502eb2520c6b5d1d9a5c4b590e03ff261565175561f6228a367d1991",
    "data/BFCL_v4_multiple.json": "aef168155ebd74b7ac2401198b201343bc7d16d7a3d7e0d4e6d8ee82c6969b2a",
    "data/BFCL_v4_irrelevance.json": "2b6ed4c2e992cdcf5f1678a701851f944bef7550ee026ed1ddb89efed5be01a6",
    "data/BFCL_v4_parallel.json": "19f51a82eff42e5d62541aa500115a056eb78f437c2ba1f10415fd7c8e5dda84",
    "data/BFCL_v4_parallel_multiple.json": "8863ea8433239f55c5f016154cf0830853c89f693c6ea270396a2fa121960579",
    "data/possible_answer/BFCL_v4_simple_python.json": "90cd5bc653690ee8e459b5b3f3fc9458606f7f3fcbf795bb51b7dc581f8c86dc",
    "data/possible_answer/BFCL_v4_multiple.json": "244e00ce9395df948bcafc7bee64e8f9c87ef70887587d83cae45b13699f3047",
    "data/possible_answer/BFCL_v4_parallel.json": "8a6aa19c1adddc6a5a2f7e40f9dbf30cc7e95815e7b830c90589ab318229e0f0",
    "data/possible_answer/BFCL_v4_parallel_multiple.json": "5ebf24f458c1f16300c05505d83d6f0a1b68b79be273a033febd0d4f840507e3",
    "eval_checker/ast_eval/ast_checker.py": "2aae7a68461a8f76c0be3894c8901b66b56967a1989d3ab066051e3fb97f1538",
    "constants/enums.py": "2182becfa2a1d071ee1db30db593b4758c6bf866aa12d2d4b8daf09175ea518a",
    "constants/type_mappings.py": "1702fb67afbe2c492608e58e2b7d02e46381f50166b47f3c952f76e34c7cd3bd",
    "utils.py": "3703b9bb63f83581c60b8e0b82aac74c360c9ca781e99e7d4eb28b0cce2285dd",
    "model_handler/utils.py": "f78fd3edce603b333dc9a88ee2c041dc547d51f71aa449ffebc044c4b1e353f3",
}
# Underdog Bench's five kinds of tasks, 24 each; we draw our own seeded sample because its task list is not published.
KINDS = [("simple_python", "Call the one right function"), ("multiple", "Pick the right function from several"),
         ("irrelevance", "Know when no tool fits"), ("parallel", "Same function, several calls"),
         ("parallel_multiple", "Several different functions")]
N_PER_KIND, SEED, CTX, PORT = 24, 2026, 16384, 8080
# llama-server's own defaults are temperature 0.8 and top_k 40, so every request states its sampler.
GREEDY = dict(temperature=0, top_k=0, top_p=1.0, min_p=0)

def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)

def sha256_file(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()

def fetch(url, dest, size=None, sha=None, quiet=False):
    """Resumable download with curl, then a size and SHA-256 check. Returns seconds spent downloading."""
    t0 = time.time()
    if not (os.path.exists(dest) and (size is None or os.path.getsize(dest) == size)):
        for attempt in range(5):
            r = sh(["curl", "-fsSL", "-C", "-", "--retry", "5", "-o", dest, url])
            if r.returncode == 0 and (size is None or os.path.getsize(dest) == size):
                break
            time.sleep(5 * (attempt + 1))
    got = os.path.getsize(dest)
    assert size is None or got == size, f"{os.path.basename(dest)}: {got} bytes, expected {size}"
    if sha:
        assert sha256_file(dest) == sha, f"{os.path.basename(dest)}: SHA-256 mismatch"
    return time.time() - t0

print(f"platform : {SYSTEM} {MACHINE}, Python {platform.python_version()}, glibc {platform.libc_ver()[1] or 'n/a'}")
if SYSTEM == "Linux":
    print("os       :", open("/etc/os-release").read().split('PRETTY_NAME="')[1].split('"')[0])
    gpu = sh(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"]).stdout.strip()
    print("gpu      :", gpu)
    # The CUDA 12.8 build of llama.cpp ships without the CUDA runtime; Colab's image has it as pip wheels.
    import importlib.util
    if importlib.util.find_spec("nvidia.cuda_runtime") is None or importlib.util.find_spec("nvidia.cublas") is None:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "nvidia-cuda-runtime-cu12==12.9.79",
                        "nvidia-cublas-cu12==12.9.2.10"], check=True)
    import nvidia.cuda_runtime, nvidia.cublas
    CUDA_LIBS = [os.path.join(list(m.__path__)[0], "lib") for m in (nvidia.cuda_runtime, nvidia.cublas)]
else:
    chip = sh(["sysctl", "-n", "machdep.cpu.brand_string"]).stdout.strip()
    mem = int(sh(["sysctl", "-n", "hw.memsize"]).stdout) / 2**30
    print(f"gpu      : {chip}, {mem:.0f} GB unified memory (Metal)")
    CUDA_LIBS = []
HW = gpu.split(",")[0] if SYSTEM == "Linux" else chip
print(f"work dir : {WORK}  ({shutil.disk_usage(WORK).free / 1e9:.0f} GB free)")

Everything the notebook touches is pinned before anything runs. The setup cell records the llama.cpp release, both model files and fourteen BFCL files by size and SHA-256, and it fixes the sampler for every request, because llama-server otherwise falls back to defaults we did not choose. It detects the platform, an NVIDIA GPU on Linux or an Apple-silicon Mac, and on Colab it ensures the CUDA 12 runtime libraries the prebuilt llama. cpp needs are importable.cpp needs are importable.

Copy CodeCopiedUse a different Browser

@section("2. Download llama.cpp b11565 and both 2-bit files, and check every byte against its pin")
def download_step():
    global LLAMA_DIR, SERVER_BIN, SERVER_ENV
    name, size, sha = LLAMA_ASSET
    tar = os.path.join(WORK, "llama", name)
    fetch(f"https://github.com/ggml-org/llama.cpp/releases/download/{LLAMA_TAG}/{name}", tar, size, sha)
    with tarfile.open(tar) as t:
        t.extractall(os.path.join(WORK, "llama"), filter="data")
    SERVER_BIN = glob.glob(os.path.join(WORK, "llama", "**", "llama-server"), recursive=True)[0]
    LLAMA_DIR = os.path.dirname(SERVER_BIN)
    for b in glob.glob(os.path.join(LLAMA_DIR, "llama-*")):
        os.chmod(b, 0o755)
    SERVER_ENV = dict(os.environ)
    if CUDA_LIBS:
        SERVER_ENV["LD_LIBRARY_PATH"] = ":".join(CUDA_LIBS + [LLAMA_DIR, SERVER_ENV.get("LD_LIBRARY_PATH", "")])
        missing = [l for l in sh(["ldd", SERVER_BIN], env=SERVER_ENV).stdout.splitlines() if "not found" in l]
        assert not missing, f"unresolved libraries: {missing}"
    r = sh([SERVER_BIN, "--version"], env=SERVER_ENV)
    ver = re.search(r"version: .*", r.stdout + r.stderr).group(0)
    print(f"llama.cpp: {name} (SHA-256 checked) -> {ver}")

    for rel, digest in BFCL_FILES.items():
        dest = os.path.join(WORK, "bfcl", rel.replace("/", "__"))
        fetch(GORILLA + rel, dest, sha=digest)
    print(f"BFCL v4: {len(BFCL_FILES)} files from gorilla@6ea5797 (5 task files, 4 answer files, 5 checker sources), all SHA-256 checked")

    for tag, m in MODELS.items():
        path = os.path.join(WORK, "models", m["file"])
        had = os.path.exists(path) and os.path.getsize(path) == m["size"]
        url = f"https://huggingface.co/{m['repo']}/resolve/{m['rev']}/{m['file']}"
        dl = fetch(url, path, m["size"])          # size check now, hash below
        t0 = time.time()
        ok = sha256_file(path) == m["sha256"]
        how = "already on disk" if had else f"downloaded in {dl:.0f} s ({m['size'] / dl / 1e6:.0f} MB/s)"
        print(f"{tag:7s}: {m['file']}  {m['size']:,} bytes, {how}; SHA-256 {'matches' if ok else 'DOES NOT MATCH'} "
              f"the Hub's LFS pin ({time.time() - t0:.0f} s to hash)")
        claim(f"{m['file']} is byte-identical to the file pinned at {m['repo']}@{m['rev'][:7]}", ok)
        assert ok
    return f"llama.cpp {LLAMA_TAG}; Saluki 7.90 GB and ISTA IQ2_XS 8.42 GB verified by SHA-256"

download_step()

We download the CUDA build of llama.cpp b11565, both 2-bit files and the BFCL data, and check every byte against its pin. The Hugging Face downloads are resumable, and the hashes are the Hub&#8217;s own LFS digests at a fixed revision, so a silently replaced file would stop the notebook rather than change its results. BFCL&#8217;s task files, answer files, and checker code all come from one gorilla commit. The cell prints how long the downloads took, which is the slowest part of the run on Colab.

Copy CodeCopiedUse a different Browser

GGML_TYPES = {0: ("F32", 1, 4), 1: ("F16", 1, 2), 8: ("Q8_0", 32, 34), 10: ("Q2_K", 256, 84), 12: ("Q4_K", 256, 144),
              16: ("IQ2_XXS", 256, 66), 17: ("IQ2_XS", 256, 74), 18: ("IQ3_XXS", 256, 98), 19: ("IQ1_S", 256, 50),
              21: ("IQ3_S", 256, 110), 22: ("IQ2_S", 256, 82), 23: ("IQ4_XS", 256, 136), 29: ("IQ1_M", 256, 56),
              30: ("BF16", 1, 2)}   # name, values per block, bytes per block (ggml-common.h)

def read_gguf(path):
    """GGUF v3 header: metadata, tensor table (name, dims, type, offset) and where the tensor data starts."""
    f = open(path, "rb")
    u = lambda fmt: struct.unpack("<" + fmt, f.read(struct.calcsize(fmt)))[0]
    s = lambda: f.read(u("Q")).decode("utf-8", "replace")
    scalar = {0: "B", 1: "b", 2: "H", 3: "h", 4: "I", 5: "i", 6: "f", 7: "?", 10: "Q", 11: "q", 12: "d"}

    def val(t):
        if t == 8:
            return s()
        if t == 9:
            et, n = u("I"), u("Q")
            return [val(et) for _ in range(n)]
        return u(scalar[t])
    assert f.read(4) == b"GGUF"
    version, n_tensors, n_kv = u("I"), u("Q"), u("Q")
    kv = {}
    for _ in range(n_kv):
        k = s()
        kv[k] = val(u("I"))
    tensors = []
    for _ in range(n_tensors):
        name = s()
        dims = [u("Q") for _ in range(u("I"))]
        ttype, off = u("I"), u("Q")
        n = math.prod(dims)
        _, per, nbytes = GGML_TYPES[ttype]
        tensors.append(dict(name=name, dims=dims, type=GGML_TYPES[ttype][0], n=n, bytes=n // per * nbytes, off=off))
    align = kv.get("general.alignment", 32)
    data_start = (f.tell() + align - 1) // align * align
    return kv, tensors, data_start

def tensor_class(name):
    if not name.startswith("blk."):
        return name.split(".")[0]                       # token_embd, output, output_norm
    kind = name.split(".")[2]
    if kind in ("attn_q", "attn_k", "attn_v", "attn_output"):
        return "full-attention " + kind[5:]
    if kind in ("attn_qkv", "attn_gate", "ssm_out", "ssm_conv1d"):
        return "linear-attention " + kind
    if kind in ("ssm_alpha", "ssm_beta"):
        return "linear-attention gates (alpha, beta)"
    if kind in ("ffn_gate", "ffn_up", "ffn_down"):
        return kind
    return "norms and small vectors"

@section("3. What Saluki changes: a tensor-by-tensor diff of the two GGUF headers")
def header_diff():
    global HDR
    HDR = {tag: read_gguf(os.path.join(WORK, "models", m["file"])) for tag, m in MODELS.items()}
    (kv_s, t_s, start_s), (kv_i, t_i, start_i) = HDR["Saluki"], HDR["ISTA"]
    assert [t["name"] for t in t_s] == [t["name"] for t in t_i] and [t["dims"] for t in t_s] == [t["dims"] for t in t_i]
    n_params = sum(t["n"] for t in t_s)
    print(f"both files: {len(t_s)} tensors with the same names and shapes, {n_params:,} weights, "
          f"architecture '{kv_s['general.architecture']}', {kv_s['qwen35.block_count']} blocks")
    for tag, (kv, ts, start) in HDR.items():
        data = sum(t["bytes"] for t in ts)
        size = MODELS[tag]["size"]
        print(f"   {tag:7s}: header {start:,} B + tensor data {data:,} B = {start + data:,} B "
              f"({'equals' if start + data == size else 'DIFFERS FROM'} the file size); {8 * data / n_params:.3f} bits per weight")
        claim(f"{tag}: header plus tensor bytes computed from the type table equals the file size exactly", start + data == size)

    rows = collections.OrderedDict()
    moves = collections.Counter()
    up = down = 0
    for a, b in zip(t_i, t_s):
        r = rows.setdefault(tensor_class(a["name"]), dict(k=0, n=0, bi=0, bs=0))
        r["k"] += 1; r["n"] += a["n"]; r["bi"] += a["bytes"]; r["bs"] += b["bytes"]
        if a["type"] != b["type"]:
            moves[(a["type"], b["type"])] += 1
            up += b["bytes"] > a["bytes"]; down += b["bytes"] < a["bytes"]
    print(f"\n{'tensor class':34s} {'count':>5s} {'weights':>9s} {'ISTA bpw':>9s} {'Saluki bpw':>10s} {'change MB':>10s}")
    for c, r in sorted(rows.items(), key=lambda kv: -kv[1]["n"]):
        if r["n"] < 1e6:
            continue
        print(f"{c:34s} {r['k']:5d} {r['n'] / 1e9:8.3f}B {8 * r['bi'] / r['n']:9.3f} {8 * r['bs'] / r['n']:10.3f} {(r['bs'] - r['bi']) / 1e6:+10.1f}")
    changed = sum(moves.values())
    print(f"\n{changed} of {len(t_s)} tensors change type: " + ", ".join(f"{n} {a}->{b}" for (a, b), n in moves.most_common()))
    print(f"   {down} get fewer bytes, {up} get more")
    claim("every tensor whose type changes gets fewer bits; none gets more", up == 0 and down == changed)
    untouched = [c for c, r in rows.items() if r["bi"] == r["bs"] and r["n"] >= 1e6]
    print(f"   classes with no change at all: {', '.join(sorted(untouched))}")
    proj = lambda c: c.startswith(("full-attention", "linear-attention")) and "gates" not in c
    claim("every attention and DeltaNet projection matrix keeps its type (only the small alpha/beta gates change)",
          all(a["type"] == b["type"] for a, b in zip(t_i, t_s) if proj(tensor_class(a["name"]))))
    keys = sorted(k for k in set(kv_s) | set(kv_i) if kv_s.get(k) != kv_i.get(k) and not k.startswith("tokenizer.ggml.t"))
    print(f"\nmetadata keys that differ: {keys}")
    print(f"Saluki's header still reads: general.name = {kv_s['general.name']!r}, quantized_by = {kv_s['general.quantized_by']!r}")
    print(f"sampling stored in both headers: temp {kv_s['general.sampling.temp']}, top_k {kv_s['general.sampling.top_k']}, "
          f"top_p {kv_s['general.sampling.top_p']:.2f} (these are Qwen's thinking-mode settings; step 5 shows what the server does with them)")
    saved = (MODELS["ISTA"]["size"] - MODELS["Saluki"]["size"]) / 1e6
    return f"{changed} of {len(t_s)} tensor types changed, all downgrades; {saved:.0f} MB smaller"

header_diff()

Reading the two GGUF headers in plain Python shows exactly what Saluki changed. Both files have the same 851 tensors with the same shapes, and the type table predicts each file&#8217;s size in bytes. Saluki changes the type of 146 tensors and every change cuts bits: most fall on the feed-forward down projections and the output layer, and the small DeltaNet gate vectors drop from BF16 to Q8_0. No attention or DeltaNet projection matrix changes, and the header still names ISTA DASLab as the quantiser.

Copy CodeCopiedUse a different Browser

@section("4. Byte-level provenance: are the unchanged tensors ISTA's own bytes?")
def provenance():
    import numpy as np
    (_, t_s, start_s), (_, t_i, start_i) = HDR["Saluki"], HDR["ISTA"]
    ms = np.memmap(os.path.join(WORK, "models", MODELS["Saluki"]["file"]), dtype=np.uint8, mode="r")
    mi = np.memmap(os.path.join(WORK, "models", MODELS["ISTA"]["file"]), dtype=np.uint8, mode="r")
    q = dict(k=0, same=0, eq_bytes=0, bytes=0)
    f32 = collections.defaultdict(lambda: [0, 0, []])            # kind -> [identical, differ, relative L2 changes]
    for a, b in zip(t_i, t_s):
        if a["type"] != b["type"]:
            continue
        x = mi[start_i + a["off"]: start_i + a["off"] + a["bytes"]]
        y = ms[start_s + b["off"]: start_s + b["off"] + b["bytes"]]
        if a["type"] == "F32":
            kind = re.sub(r"blk\.\d+\.", "", a["name"])
            u, v = x.view(np.float32).astype(np.float64), y.view(np.float32).astype(np.float64)
            same = bool(np.array_equal(u, v))
            f32[kind][0 if same else 1] += 1
            if not same:
                f32[kind][2].append(np.linalg.norm(u - v) / np.linalg.norm(u))
        else:
            eq = int(np.count_nonzero(x == y))
            q["k"] += 1; q["same"] += eq == a["bytes"]; q["eq_bytes"] += eq; q["bytes"] += a["bytes"]
    print(f"quantised matrices that keep their type: {q['same']} of {q['k']} byte-identical, but "
          f"{100 * q['eq_bytes'] / q['bytes']:.1f}% of their {q['bytes'] / 1e9:.2f} GB of bytes are equal")
    print(f"\nunquantised F32 vectors (never re-encoded, so any change means the weights changed):")
    print(f"   {'kind':28s} {'identical':>9s} {'changed':>8s}   median relative change")
    for kind, (same, diff, rel) in sorted(f32.items(), key=lambda kv: -kv[1][1]):
        med = f"{sorted(rel)[len(rel) // 2]:.1e}" if rel else "-"
        print(f"   {kind:28s} {same:9d} {diff:8d}   {med}")
    changed = sum(v[1] for v in f32.values())
    total = sum(v[0] + v[1] for v in f32.values())
    claim("Saluki's unchanged-type tensors are byte-for-byte ISTA's (a pure type re-mix)", q["same"] == q["k"] and changed == 0)
    claim("Saluki's F32 norm and gate vectors differ from ISTA's, so its weights were changed, not only re-encoded", changed > 0)
    return (f"{q['same']}/{q['k']} same-type matrices byte-identical, {100 * q['eq_bytes'] / q['bytes']:.1f}% of their bytes equal; "
            f"{changed}/{total} F32 vectors changed")

provenance()

Same types don&#8217;t mean the same weights, so we compare the bytes of the 705 tensors that keep their type. Only one of 352 quantized matrices is byte-identical, yet 98.4% of their bytes match, consistent with small edits to the underlying weights followed by re-quantizing on the same grids. The unquantized norm and gate vectors settle it: most changed by a median of a few parts in ten thousand. Saluki is a lightly changed model, not a re-encoding of ISTA&#8217;s file.

Copy CodeCopiedUse a different Browser

SERVER = {}

def start_server(tag):
    """One llama-server per model, one slot, all layers on the GPU, debug log kept for unparsed replies."""
    stop_server()
    log_path = os.path.join(WORK, "runs", f"server_{tag}.log")
    cmd = [SERVER_BIN, "-m", os.path.join(WORK, "models", MODELS[tag]["file"]), "--host", "127.0.0.1", "--port", str(PORT),
           "-c", str(CTX), "-np", "1", "-ngl", "99", "-fa", "on", "--jinja", "--reasoning-format", "deepseek", "-lv", "5"]
    t0 = time.time()
    proc = subprocess.Popen(cmd, stdout=open(log_path, "w"), stderr=subprocess.STDOUT, env=SERVER_ENV)
    while True:
        try:
            if urllib.request.urlopen(f"http://127.0.0.1:{PORT}/health", timeout=5).status == 200:
                break
        except urllib.error.HTTPError as e:
            assert e.code == 503, e
        except urllib.error.URLError:
            pass
        assert proc.poll() is None, f"llama-server exited; see {log_path}"
        assert time.time() - t0 < 900, "server did not become healthy in 15 minutes"
        time.sleep(2)
    SERVER.update(tag=tag, proc=proc, log=log_path, load_s=time.time() - t0)
    return SERVER["load_s"]

def stop_server():
    if SERVER.get("proc") and SERVER["proc"].poll() is None:
        SERVER["proc"].terminate()
        SERVER["proc"].wait(timeout=60)
    SERVER.clear()

def api(path, body=None, timeout=1800):
    req = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", None if body is None else json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def memory_report():
    """Buffer sizes from the server's load log, plus what the GPU reports."""
    text = open(SERVER["log"]).read()
    out = {}
    for label, what in (("weights", "model"), ("KV cache", "KV"), ("recurrent state", "RS"), ("compute", "compute")):
        last = {}                                  # llama.cpp sizes every buffer in a dry run first; keep the final value per device
        for dev, mib in re.findall(rf"(\S+) +{what} buffer size = +([\d.]+) MiB", text):
            last[dev] = float(mib)
        out[label] = sum(last.values())
    if ON_CUDA:
        out["GPU in use (nvidia-smi)"] = float(sh(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"]).stdout.split()[0])
    return out

@section("5. A hybrid model on one GPU: start the server, read its memory, and look at the prompt it builds")
def architecture_and_server():
    kv = HDR["Saluki"][0]
    L, every = kv["qwen35.block_count"], kv["qwen35.full_attention_interval"]
    full = [i for i in range(L) if (i + 1) % every == 0]
    heads_kv, dk = kv["qwen35.attention.head_count_kv"], kv["qwen35.attention.key_length"]
    kv_tok = len(full) * heads_kv * dk * 2 * 2                    # K and V, f16
    conv = (kv["qwen35.ssm.conv_kernel"] - 1) * (kv["qwen35.ssm.inner_size"] + 2 * kv["qwen35.ssm.group_count"] * kv["qwen35.ssm.state_size"])
    state = kv["qwen35.ssm.state_size"] * kv["qwen35.ssm.inner_size"]
    rs = (L - len(full)) * (conv + state) * 4
    print(f"{L} blocks: {L - len(full)} Gated DeltaNet (linear attention) and {len(full)} full-attention layers (3, 7, ..., {full[-1]})")
    print(f"KV cache: {kv_tok // 1024} KiB per token for the {len(full)} attention layers; a model with attention in all "
          f"{L} layers would need {L * heads_kv * dk * 4 // 1024} KiB")
    print(f"recurrent state: {rs / 2**20:.1f} MiB per sequence, fixed, whatever the context length")
    print(f"expected at -c {CTX}: KV {kv_tok * CTX / 2**20:.0f} MiB + state {rs / 2**20:.0f} MiB")

    load_s = start_server("Saluki")
    mem = memory_report()
    print(f"\nllama-server up in {load_s:.0f} s (-c {CTX}, -np 1, -ngl 99, -fa on); buffers from its log:")
    for k, v in mem.items():
        print(f"   {k:24s} {v:8.0f} MiB")
    claim(f"the server's KV buffer at -c {CTX} matches 64 KiB per token within 2%",
          abs(mem["KV cache"] - kv_tok * CTX / 2**20) <= 0.02 * kv_tok * CTX / 2**20)
    SERVER_MEM["Saluki"] = mem

    props = api("/props")
    p = props["default_generation_settings"]["params"]
    g = {k: kv[f"general.sampling.{k}"] for k in ("temp", "top_k", "top_p", "min_p")}
    from_file = abs(p["temperature"] - g["temp"]) < 1e-6 and p["top_k"] == g["top_k"] and abs(p["top_p"] - g["top_p"]) < 1e-6
    print(f"\nserver defaults: temperature {p['temperature']:.2f}, top_k {p['top_k']}, top_p {p['top_p']:.2f}, min_p {p['min_p']:.2f}"
          f" -> {'taken from the GGUF header' if from_file else 'llama.cpp built-ins, not the header'}; the card suggests 0.6 for thinking,"
          f" so every request below states its own sampler")
    claim("llama-server takes its default sampler from the GGUF's general.sampling keys", from_file)
    caps = props.get("chat_template_caps", {})
    print("template supports: " + ", ".join(k.replace("supports_", "") for k, v in caps.items() if v))
    msgs = [{"role": "user", "content": "What is the weather in Oslo?"}]
    tool = [{"type": "function", "function": {"name": "get_weather", "description": "Current weather for a city",
             "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}]
    for label, kw in (("thinking off", {"enable_thinking": False}), ("thinking on, effort low", {"reasoning_effort": "low"}),
                      ("thinking on, default", {})):
        prompt = api("/apply-template", {"messages": msgs, "tools": tool, "chat_template_kwargs": kw})["prompt"]
        n = len(api("/tokenize", {"content": prompt, "add_special": False})["tokens"])
        print(f"   {label:24s}: {n:3d} prompt tokens, ends {prompt[-28:]!r}")
    return f"KV {kv_tok // 1024} KiB/token, state {rs / 2**20:.0f} MiB; server buffers {sum(mem[k] for k in ('weights', 'KV cache', 'recurrent state', 'compute')) / 1024:.1f} GiB"

SERVER_MEM = {}
architecture_and_server()

Qwen3.8-27B is a hybrid: 48 of its 64 blocks are Gated DeltaNet linear-attention layers with a fixed recurrent state, and only every fourth block keeps full attention. The KV cache therefore costs 64 KiB per token instead of 256 KiB, plus about 150 MiB of state per sequence. We start llama-server with one slot, read its buffers from the log, check where its default sampler comes from, and look at the prompts the chat template builds with thinking off, on, and at low effort.

Copy CodeCopiedUse a different Browser

SPEED = {}

def speed_probe(tag):
    """Prefill and decode rates from the server's own timings: two prompt lengths, 128 forced output tokens."""
    rng = random.Random(SEED)
    words = "def class return import yield lambda tensor gradient matrix kernel cache token buffer layer".split()
    rows = []
    for target in (256, 1024):
        text = " ".join(rng.choice(words) for _ in range(target))
        ids = api("/tokenize", {"content": text, "add_special": False})["tokens"][:target]
        r = api("/completion", {"prompt": ids, "n_predict": 128, "ignore_eos": True, "cache_prompt": False, **GREEDY})
        t = r["timings"]
        rows.append((t["prompt_n"], t["prompt_per_second"], t["predicted_n"], t["predicted_per_second"]))
        print(f"   {tag:7s} prompt {t['prompt_n']:5d} tok at {t['prompt_per_second']:7.1f} tok/s | "
              f"decode {t['predicted_n']} tok at {t['predicted_per_second']:5.2f} tok/s")
    SPEED[tag] = rows
    return rows

@section("6. Prefill and decode speed, measured by the server")
def speed_step():
    print(f"hardware: {HW}")
    rows = speed_probe("Saluki")
    return f"Saluki on {HW}: prefill {rows[1][1]:.0f} tok/s at {rows[1][0]} tokens, decode {rows[1][3]:.1f} tok/s"

speed_step()

Speed comes from the server&#8217;s own timings rather than a stopwatch around the request. We send a 256-token and a 1,024-token prompt with the prompt cache off and force 128 output tokens, which gives a prefill rate and a decode rate at each length. A dense 27B model reads its full weight file for every generated token, so decode speed mostly depends on memory bandwidth, and the same probe runs again on ISTA&#8217;s file later for a like-for-like comparison.

Copy CodeCopiedUse a different Browser

def load_bfcl_checker():
    """BFCL's own checker functions, executed from the pinned source with their package imports replaced."""
    src = lambda rel: open(os.path.join(WORK, "bfcl", rel.replace("/", "__"))).read()

    def run(rel, ns, only=None):
        tree = ast.parse(src(rel))
        body = [n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom))]
        if only:
            body = [n for n in body if getattr(n, "name", None) in only]
        exec(compile(ast.Module(body=body, type_ignores=[]), rel, "exec"), ns)
        return ns
    enums = run("constants/enums.py", {"Enum": enum.Enum})
    tmap = run("constants/type_mappings.py", {})
    model_cfg = collections.defaultdict(lambda: types.SimpleNamespace(underscore_to_dot=True))   # OpenAI-style FC model
    chk = run("eval_checker/ast_eval/ast_checker.py", {"re": re, "Language": enums["Language"], "MODEL_CONFIG_MAPPING": model_cfg,
              "JAVA_TYPE_CONVERSION": tmap["JAVA_TYPE_CONVERSION"], "JS_TYPE_CONVERSION": tmap["JS_TYPE_CONVERSION"],
              "java_type_converter": None, "js_type_converter": None})
    utl = run("utils.py", {}, {"is_function_calling_format_output", "is_empty_output"})
    conv = run("model_handler/utils.py", {"copy": copy, "re": re, "json": json, "ModelStyle": enums["ModelStyle"],
               "GORILLA_TO_OPENAPI": tmap["GORILLA_TO_OPENAPI"]}, {"_cast_to_openai_type", "convert_to_tool"})
    return types.SimpleNamespace(
        ast_checker=lambda funcs, out, gt, cat: chk["ast_checker"](funcs, out, gt, enums["Language"].PYTHON, cat, "fc-model"),
        is_empty=utl["is_empty_output"],
        to_tools=lambda funcs: conv["convert_to_tool"](funcs, tmap["GORILLA_TO_OPENAPI"], enums["ModelStyle"].OPENAI_COMPLETIONS))

def load_tasks():
    tasks = []
    for kind, label in KINDS:
        rows = [json.loads(l) for l in open(os.path.join(WORK, "bfcl", f"data__BFCL_v4_{kind}.json")) if l.strip()]
        gt = {}
        if kind != "irrelevance":
            for l in open(os.path.join(WORK, "bfcl", f"data__possible_answer__BFCL_v4_{kind}.json")):
                if l.strip():
                    d = json.loads(l); gt[d["id"]] = d["ground_truth"]
        for r in sorted(random.Random(f"{SEED}-{kind}").sample(rows, N_PER_KIND), key=lambda r: int(r["id"].rsplit("_", 1)[1])):
            tasks.append(dict(id=r["id"], kind=kind, messages=r["question"][0], functions=r["function"], gt=gt.get(r["id"])))
    return tasks

TOOL_BLOCK = re.compile(r"<tool_call>(.*?)(?:</tool_call>|$)", re.S)
FUNC_XML = re.compile(r"<function=([^>\s]+)\s*>(.*?)(?:</function>|$)", re.S)
PARAM_XML = re.compile(r"<parameter=([^>\s]+)\s*>\n?(.*?)\n?</parameter>", re.S)

def lenient_calls(raw, functions):
    """Forgiving reading of the model's raw text: any <function=...> block, closed or not, inside or outside <tool_call>.
    Values are typed with the function's own schema (BFCL types). Not part of BFCL; used only for the 'lenient' column."""
    raw = raw.split("</think>")[-1]                    # with thinking on, the reasoning precedes </think>
    types_ = {re.sub(r"\.", "_", f["name"]): {k: v.get("type", "string") for k, v in f["parameters"]["properties"].items()}
              for f in functions}                       # tool names were sent with dots turned into underscores
    calls = []
    for fname, body in FUNC_XML.findall(raw):
        fname = fname.strip().strip('"')
        args = {}
        for p, v in PARAM_XML.findall(body):
            t = types_.get(re.sub(r"\.", "_", fname), {}).get(p, "string")
            v = v.strip() if t != "string" else v
            try:
                args[p] = (int(v) if t == "integer" else float(v) if t in ("float", "number") else
                           v.lower() == "true" if t == "boolean" and v.lower() in ("true", "false") else
                           json.loads(v) if t in ("array", "tuple", "dict", "object") else v)
            except ValueError:
                try:
                    args[p] = ast.literal_eval(v)
                except Exception:
                    args[p] = v
        calls.append({fname: args})
    return calls

def score(task, calls):
    """BFCL's rule: irrelevance passes with no call; the other kinds go through BFCL's ast_checker."""
    if task["kind"] == "irrelevance":
        return CHECK.is_empty(calls), "made a call" if calls else None
    if not calls:
        return False, "no call"
    try:
        r = CHECK.ast_checker(task["functions"], calls, task["gt"], task["kind"])
    except Exception as e:                       # malformed arguments the checker cannot walk
        return False, f"checker_error:{type(e).__name__}"
    return bool(r["valid"]), r.get("error_type")

def run_task(task, think=False, max_tokens=512):
    body = {"messages": task["messages"], "tools": CHECK.to_tools(task["functions"]), "max_tokens": max_tokens,
            "cache_prompt": False, "verbose": True, **GREEDY,
            "chat_template_kwargs": {"reasoning_effort": "low"} if think else {"enable_thinking": False}}
    log_pos = os.path.getsize(SERVER["log"])
    t0 = time.time()
    rec = dict(id=task["id"], kind=task["kind"], think=think)
    try:
        r = api("/v1/chat/completions", body)
        msg = r["choices"][0]["message"]
        rec.update(status=200, finish=r["choices"][0]["finish_reason"], raw=r["__verbose"]["content"],
                   prompt_n=r["timings"]["prompt_n"], out_n=r["timings"]["predicted_n"],
                   reasoning_chars=len(msg.get("reasoning_content") or ""))
        rec["calls"] = [{tc["function"]["name"]: json.loads(tc["function"]["arguments"])} for tc in msg.get("tool_calls") or []]
    except urllib.error.HTTPError as e:            # stock llama.cpp answers 500 when its parser cannot read the reply
        time.sleep(0.5)
        with open(SERVER["log"], errors="replace") as f:
            f.seek(log_pos)
            new = f.read()
        m = re.findall(r"=== BEGIN ===\n(.*?)\n=== END ===", new, re.S)
        rec.update(status=e.code, finish="parse error", raw=m[-1] if m else "", calls=None, prompt_n=None, out_n=None)
    rec["seconds"] = time.time() - t0
    rec["strict"], rec["strict_why"] = score(task, rec["calls"]) if rec["calls"] is not None else (False, "unparsed (HTTP 500)")
    if rec["strict"]:
        rec["lenient"] = True
    else:
        rec["lenient"], _ = score(task, lenient_calls(rec["raw"], task["functions"]))
    return rec

def bench(tag, tasks):
    out, t0 = [], time.time()
    for i, task in enumerate(tasks):
        out.append(run_task(task))
        if (i + 1) % 30 == 0:
            print(f"   {tag}: {i + 1}/{len(tasks)} done, {time.time() - t0:.0f} s")
    json.dump(out, open(os.path.join(WORK, "runs", f"bfcl_{tag}.json"), "w"), indent=1)
    return out

def ci(k, n, alpha=0.05):
    """Clopper-Pearson interval by bisection on the binomial tail."""
    def cdf(x, p):
        return sum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(x + 1))

    def solve(f, target, rising):
        lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if (f(mid) < target) == rising else (lo, mid)
        return (lo + hi) / 2
    lo = 0.0 if k == 0 else solve(lambda p: 1 - cdf(k - 1, p), alpha / 2, True)
    hi = 1.0 if k == n else solve(lambda p: cdf(k, p), alpha / 2, False)
    return lo, hi

def kind_table(tag, recs):
    print(f"\n{tag}: {'kind':38s} {'strict':>8s} {'lenient':>8s}  replies: structured / plain text / unparsed (500) / cut off")
    for kind, label in KINDS:
        rs = [r for r in recs if r["kind"] == kind]
        st = collections.Counter("unparsed" if r["status"] != 200 else "cut off" if r["finish"] == "length"
                                 else "structured" if r["calls"] else "plain text" for r in rs)
        print(f"   {label:44s} {sum(r['strict'] for r in rs):3d}/{len(rs):<4d} {sum(r['lenient'] for r in rs):3d}/{len(rs):<4d}"
              f"  {st['structured']:3d} / {st['plain text']:3d} / {st['unparsed']:3d} / {st['cut off']:3d}")
    k, n = sum(r["strict"] for r in recs), len(recs)
    lo, hi = ci(k, n)
    print(f"   {'total':44s} {k:3d}/{n:<4d} {sum(r['lenient'] for r in recs):3d}/{n:<4d}  strict 95% CI {100 * lo:.0f}-{100 * hi:.0f}%")

@section("7. Tool calling on 120 BFCL v4 tasks, thinking off: Saluki")
def bench_saluki():
    global CHECK, TASKS, RUNS
    CHECK = load_bfcl_checker()
    TASKS = load_tasks()
    print(f"sample: {N_PER_KIND} tasks per kind, drawn with seed {SEED}, {len(TASKS)} in all; scored with BFCL's ast_checker "
          f"(gorilla@6ea5797); greedy, thinking off, max_tokens 512")
    print(f"first ids per kind: " + ", ".join(t["id"] for t in TASKS[::N_PER_KIND]))
    RUNS = {"Saluki": bench("Saluki", TASKS)}
    kind_table("Saluki", RUNS["Saluki"])
    sec = [r["seconds"] for r in RUNS["Saluki"]]
    print(f"\nmedian {sorted(sec)[len(sec) // 2]:.1f} s per task on {HW}; median output {sorted(r['out_n'] or 0 for r in RUNS['Saluki'])[len(sec) // 2]} tokens")
    again = [run_task(t) for t in TASKS[:: len(TASKS) // 5][:5]]
    same = sum(a["calls"] == b["calls"] and a["raw"] == b["raw"] for a, b in zip(again, RUNS["Saluki"][:: len(TASKS) // 5][:5]))
    print(f"greedy re-run of 5 tasks: {same} of 5 identical raw replies")
    claim("greedy decoding with the prompt cache off gives the same reply on a re-run (5 tasks)", same == 5)
    s = sum(r["strict"] for r in RUNS["Saluki"])
    return f"Saluki {s}/{len(TASKS)} strict, {sum(r['lenient'] for r in RUNS['Saluki'])}/{len(TASKS)} lenient"

bench_saluki()

Underdog Bench&#8217;s 120 tasks are not published, so we draw our own: 24 per kind from the same five BFCL v4 categories, with a fixed seed. We send each task to the server as an OpenAI tool request, converted with BFCL&#8217;s own function, with thinking off and greedy decoding. Strict scoring uses only the calls llama.cpp parses and BFCL&#8217;s ast_checker, while lenient scoring re-reads the raw reply with a forgiving parser, which is how we test the vendor&#8217;s strict-versus-forgiving gap.

Copy CodeCopiedUse a different Browser

@section("8. Does thinking help? Six multi-call tasks with reasoning on, effort low")
def thinking_step():
    pick = [t for t in TASKS if t["kind"] in ("parallel", "parallel_multiple")]
    pick = random.Random(SEED).sample(pick, min(6, len(pick)))
    off = {r["id"]: r for r in RUNS["Saluki"]}
    rows = []
    for t in pick:
        r = run_task(t, think=True, max_tokens=2048)
        o = off[t["id"]]
        rows.append((t["id"], o, r))
        print(f"   {t['id']:22s} off: {'pass' if o['strict'] else 'fail'} {o['out_n'] or 0:4d} tok {o['seconds']:5.1f} s | "
              f"on: {'pass' if r['strict'] else 'fail'} {r['out_n'] or 0:4d} tok {r['seconds']:6.1f} s  ({r['finish']})")
    p_off, p_on = sum(o["strict"] for _, o, _ in rows), sum(r["strict"] for _, _, r in rows)
    tok = sum(r["out_n"] or 0 for *_, r in rows) / max(1, sum(o["out_n"] or 0 for _, o, _ in rows))
    sec = sum(r["seconds"] for *_, r in rows) / sum(o["seconds"] for _, o, _ in rows)
    print(f"\nthinking off {p_off}/{len(rows)}, thinking on {p_on}/{len(rows)}; thinking used {tok:.1f}x the output tokens and {sec:.1f}x the time")
    return f"thinking on (effort low): {p_on}/{len(rows)} vs {p_off}/{len(rows)} off, {tok:.1f}x tokens, {sec:.1f}x time"

thinking_step()

Turning thinking on is the card&#8217;s advice for general use, but at 27B every reasoning token costs time. We re-run six seeded multi-call tasks with reasoning on at the lowest effort and compare them with the same tasks run with thinking off: pass or fail, output tokens and seconds. Six tasks cannot settle whether thinking improves tool calls, so the cell focuses on cost and shows how many extra tokens a single tool call buys when the model thinks first.

Copy CodeCopiedUse a different Browser

@section("9. The parent file: ISTA's IQ2_XS through the same server, the same sample and the same checker")
def bench_ista():
    load_s = start_server("ISTA")
    mem = memory_report()
    SERVER_MEM["ISTA"] = mem
    print(f"llama-server up in {load_s:.0f} s; " + ", ".join(f"{k} {v:.0f} MiB" for k, v in mem.items()))
    print(f"weights: ISTA {mem['weights']:.0f} MiB vs Saluki {SERVER_MEM['Saluki']['weights']:.0f} MiB")
    speed_probe("ISTA")
    s, i = SPEED["Saluki"][1], SPEED["ISTA"][1]
    print(f"decode at {s[0]} prompt tokens: Saluki {s[3]:.2f} vs ISTA {i[3]:.2f} tok/s; prefill {s[1]:.0f} vs {i[1]:.0f} tok/s")
    RUNS["ISTA"] = bench("ISTA", TASKS)
    kind_table("ISTA", RUNS["ISTA"])
    stop_server()
    k = sum(r["strict"] for r in RUNS["ISTA"])
    return f"ISTA IQ2_XS {k}/{len(TASKS)} strict, {sum(r['lenient'] for r in RUNS['ISTA'])}/{len(TASKS)} lenient"

bench_ista()

The parent file follows the same path. We stop Saluki&#8217;s server, start one on ISTA&#8217;s IQ2_XS file with the same flags, read its memory, repeat the speed probe and score it on the same 120 tasks with the same checker and parsing rules. Running one model at a time keeps each well within the GPU&#8217;s memory, and using one harness for both removes differences in prompts, sampling, or parsing from the comparison.

Copy CodeCopiedUse a different Browser

def mcnemar(a, b):
    """Exact two-sided McNemar test on paired pass/fail lists."""
    b10 = sum(x and not y for x, y in zip(a, b))
    b01 = sum(y and not x for x, y in zip(a, b))
    n, k = b10 + b01, min(b10, b01)
    p = min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n) if n else 1.0
    return b10, b01, p

@section("10. Head to head: the same 120 tasks, paired, next to the vendor's numbers")
def head_to_head():
    S, I = RUNS["Saluki"], RUNS["ISTA"]
    assert [r["id"] for r in S] == [r["id"] for r in I]
    vendor = {"simple_python": 24, "multiple": 23, "irrelevance": 18, "parallel": 12, "parallel_multiple": 11}
    print(f"{'kind':38s} {'Saluki':>7s} {'ISTA':>6s} | {'lenient':>7s} {'':>5s} | vendor's Saluki (of 24)")
    for kind, label in KINDS:
        s = [r for r in S if r["kind"] == kind]; i = [r for r in I if r["kind"] == kind]
        print(f"{label:38s} {sum(r['strict'] for r in s):7d} {sum(r['strict'] for r in i):6d} | "
              f"{sum(r['lenient'] for r in s):7d} {sum(r['lenient'] for r in i):5d} | {vendor[kind]:3d}")
    out = {}
    for mode in ("strict", "lenient"):
        a, b = [r[mode] for r in S], [r[mode] for r in I]
        b10, b01, p = mcnemar(a, b)
        out[mode] = (sum(a), sum(b), b10, b01, p)
        print(f"{mode:8s}: Saluki {sum(a)}/120, ISTA {sum(b)}/120; Saluki-only passes {b10}, ISTA-only {b01}, exact McNemar p = {p:.3f}")
    print("vendor's Underdog Bench (different 120 tasks, unpublished): Saluki 88, ISTA IQ2_XS 76, full Qwen3.8-27B 84")
    sa, ia, b10, b01, p = out["strict"]
    claim("Saluki passes more of our 120 tasks than its parent (strict scoring)", sa > ia)
    claim("the difference is significant at 5% (exact McNemar)", p < 0.05)
    pick_s = sum(r["strict"] for r in S if r["kind"] in ("simple_python", "multiple"))
    pick_i = sum(r["strict"] for r in I if r["kind"] in ("simple_python", "multiple"))
    claim("Saluki is at least as good as its parent at picking the right single function (first two kinds)", pick_s >= pick_i)
    return f"strict: Saluki {sa}/120 vs ISTA {ia}/120 (McNemar p = {p:.2f}); lenient: {out['lenient'][0]} vs {out['lenient'][1]}"

head_to_head()

Because both models answered the same tasks, the comparison is paired. The cell prints the per-kind scores next to the vendor&#8217;s per-kind numbers for Saluki and runs an exact McNemar test on the tasks where the two files disagree, for strict and lenient scoring. A gap of a few tasks in 120 sits inside run-to-run noise, as the vendor&#8217;s page itself concedes, so the test tells us whether our sample shows a real difference.

Copy CodeCopiedUse a different Browser

@section("11. Where the failures come from")
def failures():
    for tag in ("Saluki", "ISTA"):
        recs = RUNS[tag]
        why = collections.Counter((r["strict_why"] or "?").split(":")[-1] for r in recs if not r["strict"])
        print(f"{tag}: {sum(not r['strict'] for r in recs)} failures -> " + ", ".join(f"{k} {v}" for k, v in why.most_common()))
        rescued = [r for r in recs if r["lenient"] and not r["strict"]]
        print(f"   lenient reading rescues {len(rescued)}: " + ", ".join(r["id"] for r in rescued[:8]))
    ex = next((r for r in RUNS["Saluki"] if not r["strict"] and r["kind"] != "irrelevance"), None)
    if ex:
        task = next(t for t in TASKS if t["id"] == ex["id"])
        print(f"\nexample, {ex['id']} ({ex['strict_why']}):")
        print("   expected:", json.dumps(task["gt"])[:300])
        print("   model   :", (json.dumps(ex["calls"]) if ex["calls"] is not None else ex["raw"])[:300])
    irr = [r for r in RUNS["Saluki"] if r["kind"] == "irrelevance" and not r["strict"]]
    if irr:
        print(f"\nirrelevance: Saluki made a call on {len(irr)} of {N_PER_KIND} prompts that no tool fits, e.g. {irr[0]['id']}: "
              f"{json.dumps(irr[0]['calls'])[:160]}")
    un = sum(r["status"] != 200 for tag in RUNS for r in RUNS[tag])
    return f"{un} replies across both models were unparseable by the stock server"

failures()

Scores hide where calls go wrong, so this cell breaks the failures down by BFCL&#8217;s own error types: wrong number of calls, wrong or missing arguments, a call made when no tool fits, and replies the stock server could not parse. It also lists the tasks the lenient reading rescues and prints one failed task beside its expected answer, the quickest way to tell a model error from a scoring artifact.

Copy CodeCopiedUse a different Browser

banner("SUMMARY")
for name, res in RESULTS.items():
    print(f"  {name:<100s}  {res}")
print("\nClaims decided in this run:")
for step, text, held in CLAIMS:
    print(f"   [{'held' if held else 'DID NOT HOLD' if held is False else 'undecided'}] step {step}: {text}")
failed = [k for k, v in RESULTS.items() if str(v).startswith("SKIPPED")]
print(f"\n{sum(h is True for *_, h in CLAIMS)} of {len(CLAIMS)} claims held; steps failed or skipped: {failed or 'none'}")
print(f"run on: {HW}; llama.cpp {LLAMA_TAG}; Python {platform.python_version()}")
print("not tested here: the full-size Qwen3.8-27B; Underdog Bench's own 120 tasks and the 100-task parallel set (unpublished); "
      "SWE-bench, WebWalkerQA, IFEval and AIME; the vision add-on; Mia and Ternary Bonsai 2; thinking at the default effort.")

The summary prints each step&#8217;s one-line result and the claims ledger (held, did not hold, or undecided), along with the hardware and the llama. cpp version.cpp version. It closes with what the notebook does not test: the full-size Qwen3.8-27B, the vendor&#8217;s own task lists, the agentic and math benchmarks, and the vision add-on.

In conclusion, Saluki is not quite what its file suggests. Its header keeps ISTA&#8217;s 851-tensor layout and saves bits only where ISTA spent more, yet its bytes and unquantized vectors show a model whose weights were changed, consistent with Underdog calling it a preview checkpoint. That turns the tool-calling comparison with its parent into a test of that training rather than of quantization alone. Both files run in stock llama.cpp, one at a time, and BFCL&#8217;s own checker gives a paired comparison on identical tasks. Small samples, greedy decoding, and a single run limit what any one notebook can claim, so the intervals matter as much as the scores.

Check out the FULL CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post How to Run Underdog Saluki 27B: 2-Bit Qwen3.8-27B Tool-Calling Guide appeared first on MarkTechPost.