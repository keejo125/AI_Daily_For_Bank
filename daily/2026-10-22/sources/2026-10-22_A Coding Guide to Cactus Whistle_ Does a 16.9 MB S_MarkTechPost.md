---
publish_time: 1792642657
link: https://www.marktechpost.com/2026/10/21/cactus-whistle-vs-whisper-base-speech-to-text-benchmark-cpu-guide/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: true
digest: |
  本文是一篇在 Apple M4 CPU 上对 Cactus Compute 的 Whistle 语音转文字模型（16.9 MB）的系统性编码测评，对比 OpenAI Whisper tiny/base。作者用固定随机种子、配对说话人聚类的 bootstrap 给出可信区间，并固定 Hugging Face 仓库版本以保证可复现。
  
  结果显示：在 test-other 样本上 Whistle 词错率（WER）约 10.47%，优于贪婪解码的 Whisper base（差 2.19 个百分点，经 Holm 校正显著），但与 beam search、test-clean 及多语种 MLS 集合无显著差异；10 秒音频上比贪婪 base 快约 5.7 倍。文章还揭示该固定引擎会静默丢弃超过 30 秒音频的中间部分，需用分窗或流式处理规避。
---

# Cactus Whistle 编码指南：一个 16.9 MB 的语音模型能否在词错率、速度、流式、时间戳、关键词以及语音转工具调用上经得起 Whisper Base 的考验？（基于 CPU）

> 原文链接：https://www.marktechpost.com/2026/10/21/cactus-whistle-vs-whisper-base-speech-to-text-benchmark-cpu-guide/
> 来源：MarkTechPost

In this tutorial, we use Whistle, Cactus Compute&#8217;s speech-to-text model, a 16.9 MB file that runs on a CPU, transcribes seven languages, and returns word timestamps and probabilities. The model card claims it beats Whisper base on LibriSpeech; we test it on seeded test-clean and test-other samples, comparing Whistle with Whisper tiny and base on identical clips, judged by paired speaker-cluster intervals with Holm correction. We find a lead over greedy Whisper base on test-other, no significant gap against beam search, and a speed advantage that narrows as clips grow. Beyond the headline, we probe a 30-second window where the pinned engine silently drops the middle of longer audio, plus streaming latency, timestamps, keyword biasing, other languages, noise, embeddings, and speech-to-tool calls. Our figures are one-run samples from an Apple M4, and published full-split numbers are quoted, not measured.

Copy CodeCopiedUse a different Browser

import os
import io
import re
import sys
import json
import math
import time
import random
import hashlib
import shutil
import zipfile
import platform
import traceback
import subprocess
import collections
import urllib.error
import urllib.request

RESULTS = {}
VERDICTS = []

def banner(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)

def section(name):
    def wrap(fn):
        def run(*a, **kw):
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
                print(f"\n[{time.time() - t0:.0f} s]")
                json.dump({"results": RESULTS, "verdicts": VERDICTS}, open("results.json", "w"), indent=1)
        return run
    return wrap

banner("1. Install Whistle, pin its weights and engine by Hub revision, transcribe one clip")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "cactus-needle==3.2.0", "openai-whisper==20250625",
                "jiwer==4.0.0", "soundfile==0.14.0", "soxr==1.1.0"], check=True)
os.environ["NEEDLE_TELEMETRY"] = "0"            # the package sends anonymous usage counts unless told not to
os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

import numpy as np
import soundfile as sf
import soxr
from huggingface_hub import hf_hub_download

# cactus-needle fetches three files on first use, from Hugging Face repos whose files are replaced in place: the 16.9 MB
# whistle.cact weights, the ~1 MB engine library (version 3.3.0 in this package; the needle3 repo received new binaries
# on 2026-10-10) and the 35 MB needle3.cact used in step 12. Pinning the Hub revision of each, and printing the hashes,
# is what makes this run reproducible. The engine version is read from the package, not typed in.
WHISTLE_REV = "ca5287601bef25af26dcf2e1b2bdc0843a7c19e5"   # Cactus-Compute/whistle, 2026-10-10
NEEDLE3_REV = "93e88ede867e4311c39151285e74df513e4b835b"   # Cactus-Compute/needle3 (engine + Needle 3 weights), 2026-10-10
from needle.agent import fetch as needle_fetch
TAG = needle_fetch._platform_tag()
ENGINE_VERSION = needle_fetch.engine_version(3)
weights = hf_hub_download("Cactus-Compute/whistle", "whistle.cact", revision=WHISTLE_REV)
wheel = hf_hub_download("Cactus-Compute/needle3", needle_fetch.engine_wheel(ENGINE_VERSION, TAG, 3), revision=NEEDLE3_REV)
with zipfile.ZipFile(wheel) as z:
    member = next(n for n in z.namelist() if n.startswith("needle/libneedle"))
    os.makedirs("engine", exist_ok=True)
    engine = os.path.abspath(os.path.join("engine", os.path.basename(member)))
    open(engine, "wb").write(z.read(member))
needle3_weights = hf_hub_download("Cactus-Compute/needle3", "needle3.cact", revision=NEEDLE3_REV)
os.makedirs(needle_fetch.cache_dir(3), exist_ok=True)           # Needle(tools=...) reads its weights from this cache path
shutil.copyfile(needle3_weights, os.path.join(needle_fetch.cache_dir(3), needle_fetch.base_weights(3)))
os.environ["NEEDLE_WHISTLE_WEIGHTS"] = weights   # both variables are honoured by the package
os.environ["NEEDLE3_LIB_PATH"] = engine

import needle
import importlib.metadata as md
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]
CPU = platform.processor() or platform.machine()
if sys.platform == "linux" and os.path.exists("/proc/cpuinfo"):
    CPU = next((l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name")), CPU)
elif sys.platform == "darwin":
    CPU = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], capture_output=True, text=True).stdout.strip() or CPU
print(f"cactus-needle {needle.__version__} (engine {ENGINE_VERSION}, wheel tag {TAG})   python {platform.python_version()}   "
      f"soundfile {md.version('soundfile')}  soxr {md.version('soxr')}  numpy {np.__version__}")
print(f"hardware: {CPU}, {os.cpu_count()} cpus visible")
print(f"whistle.cact  {os.path.getsize(weights)/1e6:.1f} MB  sha256 {sha(weights)}   @ {WHISTLE_REV[:12]}")
print(f"engine        {os.path.getsize(engine)/1e6:.1f} MB  sha256 {sha(engine)}   @ {NEEDLE3_REV[:12]}")
print(f"needle3.cact  {os.path.getsize(needle3_weights)/1e6:.1f} MB  sha256 {sha(needle3_weights)}   @ {NEEDLE3_REV[:12]}")

SR = 16000
W = needle.Whistle()      # one model per process, not thread-safe; every later step reuses this object

def fetch(url, tries=7):
    """GET with retries. The datasets-server rate-limits anonymous callers (HTTP 429): honour Retry-After when it is
    sent, otherwise back off 5, 10, 20, 40 ... seconds, and never give up on the first refusal."""
    for k in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if k == tries - 1:
                raise
            wait = int(e.headers.get("Retry-After", 0) or 0) if e.code == 429 else 0
            time.sleep(max(wait, 5 * 2 ** k) if e.code in (429, 500, 502, 503, 504) else 2)
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(3 * (k + 1))

def page(dataset, config, split, offset, length=100):
    """One page of a Hub dataset through the datasets-server rows API: metadata plus signed audio URLs."""
    url = (f"https://datasets-server.huggingface.co/rows?dataset={dataset}&config={config}"
           f"&split={split}&offset={offset}&length={length}")
    time.sleep(0.25)                                  # stay under the anonymous rate limit when paging a whole split
    return json.loads(fetch(url))

def load_audio(row):
    """Download one row's clip; return 16 kHz mono float32 samples and the sha256 of the original file."""
    data = fetch(row["audio"][0]["src"])
    audio, sr = sf.read(io.BytesIO(data), dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if sr != SR:
        audio = soxr.resample(audio, sr, SR, quality="HQ")
    return audio, hashlib.sha256(data).hexdigest()[:12]

first = page("openslr/librispeech_asr", "clean", "test", 0, 1)["rows"][0]["row"]
clip, _ = load_audio(first)
t0 = time.perf_counter()
out = W.transcribe(clip, word_timestamps=True)
wall = (time.perf_counter() - t0) * 1000
print(f"\nclip {first['id']}  {len(clip)/SR:.1f} s   reference: {first['text']}")
print(f"-> {out['text']!r}")
print(f"   language {out['language']}   engine time to first token {out['ttft_ms']:.1f} ms   decode {out['decode_tps']:.0f} tok/s"
      f"   wall {wall:.0f} ms")
print("   first words:", [(w["word"], w["start"], w["end"], w["probability"]) for w in out["words"][:3]])
RESULTS["1. Install Whistle, pin its weights and engine by Hub revision, transcribe one clip"] = \
    f"{os.path.getsize(weights)/1e6:.1f} MB weights, {len(clip)/SR:.1f} s clip in {wall:.0f} ms"

We install cactus-needle 3.2.0 with its dependencies pinned and turn off its anonymous telemetry. The package downloads Whistle&#8217;s weights, its engine and Needle 3&#8217;s weights from Hugging Face repositories whose files are replaced in place, so we pin both repositories to fixed revisions and print SHA-256 hashes. The page() helper reads the datasets-server rows API with rate-limit backoff, and load_audio() resamples clips to 16 kHz. The first test-clean clip, 3.5 s of speech, transcribes in 33 ms of wall time, each word carrying its start, end and probability.

Copy CodeCopiedUse a different Browser

import jiwer
import whisper
import torch
from whisper.normalizers import EnglishTextNormalizer, BasicTextNormalizer

NORM_EN = EnglishTextNormalizer()      # the normalisers Whistle's own benchmarks use; applied to both sides, always
NORM_BASIC = BasicTextNormalizer()
SEED = 2026
N_WHISTLE = 300                        # clips per LibriSpeech split that Whistle transcribes (it is cheap)
N_PAIRED = {"other": 100, "clean": 60}  # the first N of them also go through Whisper (it is not); test-other is primary
MAX_CLIP_S = 30.0                      # Whistle's single-pass window; longer clips are declared out of scope here
WHISPER_SECONDS = collections.Counter()

def all_rows(dataset, config, split):
    out, offset = [], 0
    while True:
        rows = page(dataset, config, split, offset)["rows"]
        out += [r["row"] for r in rows]
        offset += 100
        if len(rows) < 100:
            return out

def dataset_sha(dataset):
    return json.loads(fetch(f"https://huggingface.co/api/datasets/{dataset}"))["sha"][:12]

def wer_counts(ref, hyp):
    """Errors (S+D+I) and reference words for one normalised pair; an empty hypothesis is all deletions."""
    n = len(ref.split())
    if not hyp.strip():
        return n, n
    o = jiwer.process_words(ref, hyp)
    return o.substitutions + o.deletions + o.insertions, n

def sdi(ref, hyp):
    if not hyp.strip():
        return 0, len(ref.split()), 0
    o = jiwer.process_words(ref, hyp)
    return o.substitutions, o.deletions, o.insertions

def corpus_wer(errs, words):
    return 100.0 * sum(errs) / max(sum(words), 1)

def _by_cluster(clusters, *arrays):
    tot = collections.defaultdict(lambda: [0.0] * len(arrays))
    for i, c in enumerate(clusters):
        for j, a in enumerate(arrays):
            tot[c][j] += a[i]
    return tot

def wer_ci(clusters, errs, words, B=2000, seed=0):
    """95% percentile interval of a corpus WER, resampling clusters (speakers) with replacement."""
    tot = _by_cluster(clusters, errs, words)
    keys, rng = sorted(tot), random.Random(seed)
    boots = []
    for _ in range(B):
        d = rng.choices(keys, k=len(keys))
        boots.append(100 * sum(tot[c][0] for c in d) / max(sum(tot[c][1] for c in d), 1))
    return np.percentile(boots, [2.5, 97.5])

def paired_contrast(clusters, errs_a, words, errs_b, label_a, label_b, B=2000, seed=0):
    """WER(a) - WER(b) with a paired speaker-cluster bootstrap: the same resampled speakers for both systems."""
    tot = _by_cluster(clusters, errs_a, errs_b, words)
    keys, rng = sorted(tot), random.Random(seed)
    boots = []
    for _ in range(B):
        d = rng.choices(keys, k=len(keys))
        w = max(sum(tot[c][2] for c in d), 1)
        boots.append(100 * (sum(tot[c][0] for c in d) - sum(tot[c][1] for c in d)) / w)
    boots = np.array(boots)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    p = 2 * min((boots <= 0).mean(), (boots >= 0).mean())
    return {"a": label_a, "b": label_b, "diff": corpus_wer(errs_a, words) - corpus_wer(errs_b, words),
            "lo": lo, "hi": hi, "p": max(p, 1 / B), "clusters": len(keys)}

def holm(ps, alpha=0.05):
    order, keep = np.argsort(ps), [False] * len(ps)
    for rank, i in enumerate(order):
        if ps[i] <= alpha / (len(ps) - rank):
            keep[i] = True
        else:
            break
    return keep

def verdict(c, significant):
    """Verdict rule: diff = WER(other system) - WER(Whistle). CI entirely > 0 and Holm-significant -> Whistle ahead;
    entirely < 0 and significant -> Whistle behind; otherwise no significant difference at this sample size."""
    if c["lo"] > 0 and significant:
        return "Whistle ahead"
    if c["hi"] < 0 and significant:
        return "Whistle behind"
    return "no significant difference at this n"

def fmt_contrast(c):
    return f"{c['diff']:+.2f} pts (95% CI {c['lo']:+.2f}..{c['hi']:+.2f}, {c['clusters']} speakers)"

@section("2. Fixed, seeded samples of LibriSpeech test-clean and test-other, and the rules for the verdicts")
def sample_english():
    global EN
    print("Rules for the verdicts below, written into this notebook before its final run (exploratory probes on the")
    print("same splits came first; the prose says which):")
    print(f"  * simple random sample of {N_WHISTLE} rows per split (seed {SEED}); the first {N_PAIRED['other']} (test-other) and "
          f"{N_PAIRED['clean']} (test-clean) are the paired Whisper subsets")
    print(f"  * clips longer than {MAX_CLIP_S:.0f} s are excluded and counted (Whistle's single-pass window), as are empty references")
    print("  * the same normaliser on both sides of each comparison (Whisper's EnglishTextNormalizer for LibriSpeech, its")
    print("    BasicTextNormalizer for MLS); corpus WER = summed errors / summed reference words")
    print("  * interval: 95% speaker-cluster paired bootstrap, 2,000 draws, the same resampled speakers for every system")
    print("  * verdict per contrast: unadjusted CI of WER(other) - WER(Whistle) entirely > 0 and Holm-adjusted p < 0.05 ->")
    print("    Whistle ahead; entirely < 0 and significant -> behind; otherwise no significant difference at this n")
    print("    family A (published claims): test-other and test-clean vs base greedy and vs base beam 5, MLS pooled vs base greedy;")
    print("    family B: the keyword contrasts. Holm at alpha = 0.05 within each family. Whisper tiny rows are descriptive.\n")
    global MANIFEST
    EN, manifest = {}, {"dataset_sha": dataset_sha("openslr/librispeech_asr"), "seed": SEED, "splits": {}}
    MANIFEST = manifest
    for split in ("other", "clean"):
        t0 = time.time()
        rows = all_rows("openslr/librispeech_asr", split, "test")
        idx = random.Random(SEED).sample(range(len(rows)), N_WHISTLE)
        kept, too_long, empty = [], 0, 0
        for i in idx:
            r = rows[i]
            audio, h = load_audio(r)
            ref = NORM_EN(r["text"])
            if len(audio) / SR > MAX_CLIP_S:
                too_long += 1
                continue
            if not ref:
                empty += 1
                continue
            kept.append({"id": r["id"], "spk": str(r["speaker_id"]), "text": r["text"], "ref": ref,
                         "audio": audio, "dur": len(audio) / SR, "sha": h})
        EN[split] = kept
        manifest["splits"][split] = {"rows": len(rows), "sampled": N_WHISTLE, "too_long": too_long, "empty_ref": empty,
                                     "ids": [c["id"] for c in kept], "sha": [c["sha"] for c in kept]}
        durs = [c["dur"] for c in kept]
        pk = kept[:N_PAIRED[split]]
        print(f"test-{split}: {len(rows)} rows -> {len(kept)} clips kept ({too_long} over {MAX_CLIP_S:.0f} s, {empty} empty), "
              f"{len(set(c['spk'] for c in kept))} speakers, {sum(durs)/60:.1f} min, clip {np.mean(durs):.1f} s mean / {max(durs):.1f} s max"
              f"   [{time.time()-t0:.0f} s]")
        print(f"   paired subset: {len(pk)} clips, {len(set(c['spk'] for c in pk))} speakers, {sum(c['dur'] for c in pk):.0f} s of audio, "
              f"{sum(len(c['ref'].split()) for c in pk)} reference words")
    json.dump(manifest, open("manifest.json", "w"))
    print(f"\nmanifest.json: LibriSpeech revision {manifest['dataset_sha']}, clip ids and file hashes (the MLS and MInDS-14 clips are added to it in")
    print("steps 9 and 12), so a rerun can prove it used the same audio")
    return f"{len(EN['other'])} + {len(EN['clean'])} clips, manifest written"

sample_english()

A verdict means little if its rule is set after the final numbers arrive, so we wrote ours into the notebook before the final run, after exploratory probes that touched some of the same clips. We draw a seeded sample of 300 rows per split and drop clips longer than Whistle&#8217;s single-pass window, leaving 299 clips in each. The paired subsets, the first 100 test-other and 60 test-clean clips, go through Whisper, and few speakers make their intervals approximate. A difference counts only when its 95% paired speaker-cluster bootstrap interval excludes zero and its Holm-adjusted p is below 0.05.

Copy CodeCopiedUse a different Browser

WHISPER = {}

def whisper_model(size):
    if size not in WHISPER:
        WHISPER[size] = whisper.load_model(size, device="cpu")
    return WHISPER[size]

def run_whisper(size, audio, language="en", **kw):
    """openai-whisper with its defaults (greedy with temperature fallback) unless kw says otherwise. Seeded per call,
    because the fallback samples. Returns text, whether any segment needed the fallback, and the wall time."""
    torch.manual_seed(0)
    WHISPER_SECONDS[size] += len(audio) / SR
    t0 = time.perf_counter()
    r = whisper_model(size).transcribe(audio, language=language, fp16=False, **kw)
    fell_back = any(s.get("temperature", 0) > 0 for s in r["segments"])
    return r["text"], fell_back, time.perf_counter() - t0

SYSTEMS = {"other": [("whisper tiny, greedy", "tiny", {}), ("whisper base, greedy", "base", {}), ("whisper base, beam 5", "base", {"beam_size": 5})],
           "clean": [("whisper tiny, greedy", "tiny", {}), ("whisper base, greedy", "base", {}), ("whisper base, beam 5", "base", {"beam_size": 5})]}
FAMILY_A = {"test-clean: Whistle vs whisper base, greedy", "test-clean: Whistle vs whisper base, beam 5",
            "test-other: Whistle vs whisper base, greedy", "test-other: Whistle vs whisper base, beam 5",
            "MLS pooled: Whistle vs whisper base, greedy"}
PUBLISHED = {"other": "Whistle 10.49 / Whisper base 11.0 (paper table 9, beam) / 12.4 (table 8, greedy)",
             "clean": "Whistle 4.31 / Whisper base 4.9 (paper table 9, beam) / 5.0 (table 8, greedy)"}
CONTRASTS = []

@section("3. Word error rate against Whisper tiny and base, paired by clip, with a verdict per contrast")
def english_wer():
    global HYP
    HYP = {}
    for split in ("other", "clean"):
        clips = EN[split]
        t0 = time.perf_counter()
        hw = [W.transcribe(c["audio"], language="en")["text"] for c in clips]
        tw = time.perf_counter() - t0
        HYP[(split, "Whistle")] = hw
        e_w, n_w = zip(*[wer_counts(c["ref"], NORM_EN(h)) for c, h in zip(clips, hw)])
        lo, hi = wer_ci([c["spk"] for c in clips], e_w, n_w)
        print(f"test-{split}: Whistle on all {len(clips)} clips: WER {corpus_wer(e_w, n_w):.2f}% (95% speaker-cluster CI {lo:.2f}..{hi:.2f}) "
              f"in {tw:.1f} s ({1000*tw/len(clips):.0f} ms per clip)")
        print(f"   published full-split figures, different sample: {PUBLISHED[split]}")
        pk = clips[:N_PAIRED[split]]
        spk = [c["spk"] for c in pk]
        e_wp, n_p = list(e_w[:len(pk)]), list(n_w[:len(pk)])
        s = np.sum([sdi(c["ref"], NORM_EN(h)) for c, h in zip(pk, hw[:len(pk)])], axis=0)
        print(f"   paired subset, {len(pk)} clips / {len(set(spk))} speakers / {sum(n_p)} words:")
        print(f"   {'Whistle, 5-beam':22s} {corpus_wer(e_wp, n_p):6.2f}%  S/D/I {s[0]:3d}/{s[1]:3d}/{s[2]:3d}")
        for label, size, kw in SYSTEMS[split]:
            res = [run_whisper(size, c["audio"], **kw) for c in pk]
            hyps = [r[0] for r in res]
            HYP[(split, label)] = hyps
            e_o = [wer_counts(c["ref"], NORM_EN(h))[0] for c, h in zip(pk, hyps)]
            s = np.sum([sdi(c["ref"], NORM_EN(h)) for c, h in zip(pk, hyps)], axis=0)
            con = paired_contrast(spk, e_o, n_p, e_wp, label, "Whistle")
            con["name"] = f"test-{split}: Whistle vs {label}"
            CONTRASTS.append(con)
            better, worse = sum(a < b for a, b in zip(e_wp, e_o)), sum(a > b for a, b in zip(e_wp, e_o))
            print(f"   {label:22s} {corpus_wer(e_o, n_p):6.2f}%  S/D/I {s[0]:3d}/{s[1]:3d}/{s[2]:3d}  fallback on {sum(r[1] for r in res):2d} clips  "
                  f"{np.median([r[2] for r in res])*1000:5.0f} ms/clip  | {fmt_contrast(con)}  clips Whistle better/worse {better}/{worse}")
    fam = [c for c in CONTRASTS if c["name"] in FAMILY_A]
    print(f"\nContrasts so far (family A: {len(fam)} of 5; the Holm correction and the verdicts come once the MLS contrast is in):")
    for c in CONTRASTS:
        tag = "family A" if c["name"] in FAMILY_A else "descriptive"
        print(f"   {c['name']:48s} {fmt_contrast(c)}  p~{c['p']:.3f}  [{tag}]")
    print("\n   Whistle decodes with a 5-beam length-normalised search. openai-whisper's default is greedy with temperature")
    print("   fallback; the Whisper paper's LibriSpeech numbers come from beam search, so the beam-5 rows are the like-for-like ones.")
    print("   Every gap here is a system gap (model plus decoder), not a model-only one.")
    return " | ".join(f"test-{s}: Whistle {corpus_wer(*zip(*[wer_counts(c['ref'], NORM_EN(h)) for c, h in zip(EN[s][:N_PAIRED[s]], HYP[(s, 'Whistle')][:N_PAIRED[s]])])):.2f}% "
                      f"vs base greedy {corpus_wer(*zip(*[wer_counts(c['ref'], NORM_EN(h)) for c, h in zip(EN[s][:N_PAIRED[s]], HYP[(s, 'whisper base, greedy')])])):.2f}%" for s in ("other", "clean"))

english_wer()

Whisper&#8217;s default decoder is greedy with temperature fallback. At the same time, the paper&#8217;s LibriSpeech numbers come from beam search, and Whistle decodes with a five-beam search, so every comparison must name its baseline. Scored with one normaliser, Whistle&#8217;s WER is 10.47% on the test-other sample, near the published full-split 10.49, which we quote rather than measure. On the paired subset it scores 10.27%, against 12.46% for greedy Whisper base and 10.83% for beam search. The 2.19-point lead over greedy survives the Holm correction, but the beam gap does not, so the baseline wins.

Copy CodeCopiedUse a different Browser

def audio_seconds(clips, seconds):
    """Exactly `seconds` of speech: clips concatenated in sample order, then trimmed."""
    out, total = [], 0
    for c in clips:
        out.append(c["audio"])
        total += c["dur"]
        if total >= seconds:
            break
    return np.concatenate(out)[:int(seconds * SR)]

PROBE_SCRIPT = r"""
import sys, json, time, resource, numpy as np
kind, paths = sys.argv[1], sys.argv[2:]
scale = 1 << 20 if sys.platform == "darwin" else 1 << 10        # ru_maxrss is bytes on macOS, kilobytes on Linux
rss = lambda: resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / scale
out = {"kind": kind}
if kind.startswith("whistle"):
    import needle
    out["after_import"] = rss()
    W = needle.Whistle()
    run = lambda a: W.transcribe(a, language="en")
else:
    import whisper, torch
    out["after_import"] = rss()
    size, kw = kind.split("-")[1], ({"beam_size": 5} if kind.endswith("beam5") else {})
    m = whisper.load_model(size, device="cpu")
    def run(a):
        torch.manual_seed(0)
        return m.transcribe(a, language="en", fp16=False, **kw)
clips = {p: np.load(p) for p in paths}
run(clips[paths[0]])                                               # warm-up
reps = 5 if kind.startswith("whistle") else 3
for p, a in clips.items():
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); r = run(a); ts.append(time.perf_counter() - t0)
    out[p] = {"wall_ms": 1000 * float(np.median(ts)), "spread_ms": 1000 * float(np.ptp(ts))}
    if kind.startswith("whistle"):
        out[p].update(ttft_ms=r["ttft_ms"], tps=r["decode_tps"])
out["peak"] = rss()
print(json.dumps(out))
"""

@section("4. Speed and footprint: identical arrays, one fresh process per engine, total wall time and peak memory")
def speed():
    pool = EN["other"]
    print(f"hardware: {CPU}, {os.cpu_count()} cpus visible. Each engine runs in its own fresh process so torch's threads cannot slow")
    print("Whistle down (or the reverse); Whistle's engine picks its own thread count. Primary measure: total wall time on the same")
    print("float32 array, median of 5 (Whistle) or 3 (Whisper) after a warm-up. ttft_ms is the engine's own clock, for reference.\n")
    for secs in (5, 10, 30):
        np.save(f"clip{secs}.npy", audio_seconds(pool, secs))
    open("probe.py", "w").write(PROBE_SCRIPT)
    res = {}
    for kind in ("whistle", "whisper-tiny", "whisper-base", "whisper-base-beam5"):
        out = subprocess.run([sys.executable, "probe.py", kind, "clip5.npy", "clip10.npy", "clip30.npy"], capture_output=True, text=True, env=os.environ)
        if out.returncode != 0:
            raise RuntimeError(f"{kind} probe failed: {out.stderr[-300:]}")
        res[kind] = json.loads(out.stdout.strip().splitlines()[-1])
    print(f"{'clip':>6s} | {'Whistle wall':>12s} {'spread':>7s} {'ttft':>6s} {'tok/s':>6s} | {'tiny greedy':>11s} | {'base greedy':>11s} | {'base beam 5':>11s}")
    for secs in (5, 10, 30):
        p = f"clip{secs}.npy"
        w = res["whistle"][p]
        print(f"{secs:5d} s | {w['wall_ms']:9.0f} ms {w['spread_ms']:5.0f} ms {w['ttft_ms']:6.1f} {w['tps']:6.0f} | "
              f"{res['whisper-tiny'][p]['wall_ms']:8.0f} ms | {res['whisper-base'][p]['wall_ms']:8.0f} ms | {res['whisper-base-beam5'][p]['wall_ms']:8.0f} ms")
    w5, w10, w30 = (res["whistle"][p]["wall_ms"] for p in ("clip5.npy", "clip10.npy", "clip30.npy"))
    b5, b10, b30 = (res["whisper-base"][p]["wall_ms"] for p in ("clip5.npy", "clip10.npy", "clip30.npy"))
    bb5, bb10, bb30 = (res["whisper-base-beam5"][p]["wall_ms"] for p in ("clip5.npy", "clip10.npy", "clip30.npy"))
    print(f"\nreal-time factor on the 10 s clip: Whistle {w10/10000:.4f}, base greedy {b10/10000:.3f}, base beam 5 {bb10/10000:.3f}")
    print(f"base greedy / Whistle wall time: {b5/w5:.1f}x at 5 s, {b10/w10:.1f}x at 10 s, {b30/w30:.1f}x at 30 s; beam 5 / Whistle: "
          f"{bb5/w5:.1f}x, {bb10/w10:.1f}x, {bb30/w30:.1f}x")
    print(f"from 5 to 10 s the wall time grows {w10/w5:.2f}x for Whistle, {b10/b5:.2f}x for base greedy, {bb10/bb5:.2f}x for base beam 5;")
    print(f"from 10 to 30 s: {w30/w10:.2f}x, {b30/b10:.2f}x, {bb30/bb10:.2f}x. Whisper's encoder always sees a padded 30 s window; its decoder")
    print("still grows with the words it emits, so the padding fixes only part of its cost. The encoder is not timed separately here.")
    print("\npeak RSS of each process (model loaded, three clips transcribed) and the RSS right after its imports:")
    for kind in ("whistle", "whisper-tiny", "whisper-base"):
        r = res[kind]
        print(f"   {kind:13s} peak {r['peak']:6.0f} MB   after imports {r['after_import']:4.0f} MB   -> {r['peak']-r['after_import']:4.0f} MB for the model and the run")
    sizes = {"whistle.cact + engine": (os.path.getsize(weights) + os.path.getsize(engine)) / 1e6}
    for size in ("tiny", "base"):
        p = os.path.expanduser(f"~/.cache/whisper/{size}.pt")
        sizes[f"whisper {size}.pt"] = os.path.getsize(p) / 1e6 if os.path.exists(p) else float("nan")
    print("files on disk: " + ", ".join(f"{k} {v:.1f} MB" for k, v in sizes.items()) + "  (file sizes, not deployed footprint)")
    off = subprocess.run([sys.executable, "-c", "import needle, numpy as np; W = needle.Whistle(); print(W.transcribe(np.zeros(16000, np.float32))['text'] == '')"],
                         capture_output=True, text=True, env={**os.environ, "HF_HUB_OFFLINE": "1"})
    print(f"fresh process with HF_HUB_OFFLINE=1 and the pinned paths: {'loads and runs' if 'True' in off.stdout else 'FAILED: ' + off.stderr[-200:]}")
    return f"10 s clip: Whistle {w10:.0f} ms vs base greedy {b10:.0f} ms ({b10/w10:.1f}x, {b5/w5:.1f}x at 5 s, {b30/w30:.1f}x at 30 s); peak RSS {res['whistle']['peak']:.0f} vs {res['whisper-base']['peak']:.0f} MB"

speed()

Speed comparisons fail when engines share a process, since torch threads can slow one. Each engine therefore runs in a fresh process on identical float32 arrays, timed as a median after warm-up. The gap narrows as clips grow, from 7.7 times Whistle&#8217;s time at 5 s to 2.8 times at 30 s, partly from Whisper&#8217;s fixed padding window. Peak memory is 124 MB for Whistle and 823 MB for Whisper base. Whistle&#8217;s per-clip time differed nearly threefold between the two splits, which clip length does not explain, so treat the ratios as approximate.

Copy CodeCopiedUse a different Browser

def quiet_windows(a, limit=30.0, search=5.0, hop=0.2):
    """Cut before `limit` seconds at the quietest `hop`-second patch inside the last `search` seconds of each window."""
    out, i, n, s, h = [], 0, int(limit * SR), int(search * SR), int(hop * SR)
    while len(a) - i > n:
        seg = a[i + n - s:i + n]
        energy = [np.mean(seg[j:j + h] ** 2) for j in range(0, len(seg) - h, h // 4)]
        cut = i + n - s + int(np.argmin(energy)) * (h // 4) + h // 2
        out.append(a[i:cut])
        i = cut
    out.append(a[i:])
    return out

def speaker_sessions(min_s=40, max_s=100, k=8):
    """Same-speaker concatenations (0.4 s gaps) from the sampled clips of both splits, longest speakers first."""
    by = collections.defaultdict(list)
    for split in ("other", "clean"):
        for c in EN[split]:
            by[c["spk"]].append(c)
    out, gap = [], np.zeros(int(0.4 * SR), np.float32)
    for spk, cs in sorted(by.items(), key=lambda kv: -sum(c["dur"] for c in kv[1])):
        parts, used, total = [], [], 0
        for c in cs:
            if total + c["dur"] + 0.4 > max_s:
                break
            parts += [c["audio"], gap]
            used.append(c)
            total += c["dur"] + 0.4
        if total >= min_s:
            out.append({"spk": spk, "clips": used, "audio": np.concatenate(parts), "ref": " ".join(c["ref"] for c in used), "dur": total})
        if len(out) == k:
            break
    return out

OTHER_ENGINE_SCRIPT = r"""
import sys, os, numpy as np
os.environ["NEEDLE3_LIB_PATH"] = sys.argv[1]
import needle
W = needle.Whistle()
a = np.load(sys.argv[2])
for secs in (30.0, 30.01, 45.0):
    try:
        r = W.transcribe(a[:int(secs * 16000)], language="en", word_timestamps=True)
        print(f"   {secs:6.2f} s -> {len(r['words'])} words, last word ends at {r['words'][-1]['end']:.2f} s")
    except RuntimeError as e:
        print(f"   {secs:6.2f} s -> RuntimeError: {e}")
"""

@section("5. The 30-second window: what transcribe() does with longer audio, and two ways around it")
def long_audio():
    global SESSIONS
    SESSIONS = speaker_sessions()
    s = SESSIONS[0]
    gap = np.zeros(int(0.4 * SR), np.float32)
    print(f"speaker {s['spk']}: {len(s['clips'])} utterances joined with 0.4 s gaps, {s['dur']:.0f} s, {len(s['ref'].split())} reference words")
    print("the docs say transcribe() takes 'audio of any length, one pass up to 30 seconds and windowed beyond it'.")
    print(f"the pinned engine {ENGINE_VERSION}, on whole utterances cut from the session so the reference is exact:\n")
    print(f"{'audio':>7s} | {'ref words':>9s} {'hyp words':>9s} {'WER':>7s} | gaps longer than 3 s in the word timeline")
    for target in (20, 29, 35, 45, 60, 90):
        parts, refs, total = [], [], 0
        for c in s["clips"]:
            if total + c["dur"] + 0.4 > target:
                break
            parts += [c["audio"], gap]
            refs.append(c["ref"])
            total += c["dur"] + 0.4
        if total < min(target, s["dur"]) - 8:
            continue
        a, ref = np.concatenate(parts), " ".join(refs)
        r = W.transcribe(a, language="en", word_timestamps=True)
        hyp = NORM_EN(r["text"])
        gaps = [f"{w1['end']:.0f}-{w2['start']:.0f} s" for w1, w2 in zip(r["words"], r["words"][1:]) if w2["start"] - w1["end"] > 3]
        print(f"{total:5.0f} s | {len(ref.split()):9d} {len(hyp.split()):9d} {100*jiwer.wer(ref, hyp or '<empty>'):6.1f}% | {', '.join(gaps) or 'none'}")
    full = W.transcribe(s["audio"], language="en", word_timestamps=True)
    hyp = NORM_EN(full["text"])
    print(f"\nthe whole {s['dur']:.0f} s in one call: {len(hyp.split())} of {len(s['ref'].split())} words, WER {100*jiwer.wer(s['ref'], hyp or '<empty>'):.1f}%, "
          f"nothing raised, engine ttft {full['ttft_ms']:.0f} ms")
    # the same repo revision also holds a 3.2.0 engine wheel; a child process shows what that build does with the same audio
    other_wheel = hf_hub_download("Cactus-Compute/needle3", needle_fetch.engine_wheel("3.2.0", TAG, 3), revision=NEEDLE3_REV)
    with zipfile.ZipFile(other_wheel) as z:
        member = next(n for n in z.namelist() if n.startswith("needle/libneedle"))
        other = os.path.abspath(os.path.join("engine", "v3.2.0-" + os.path.basename(member)))
        open(other, "wb").write(z.read(member))
    np.save("session0.npy", s["audio"])
    open("other_engine.py", "w").write(OTHER_ENGINE_SCRIPT)
    out = subprocess.run([sys.executable, "other_engine.py", other, "session0.npy"], capture_output=True, text=True, env=os.environ)
    print(f"\nthe 3.2.0 engine wheel from the same repo revision (sha256 {sha(other)}), in a child process, on the same audio:")
    print(out.stdout.rstrip() or out.stderr[-300:])
    print("   two builds, two behaviours: one windows and loses the middle, the other refuses. Either way the split is yours to make.\n")
    print("workarounds on the whole clip, scored against the exact reference (one clip; the joins are 0.4 s of silence):")
    results = {}
    for name, wins in (("fixed 30 s windows", [s["audio"][i:i + 30 * SR] for i in range(0, len(s["audio"]), 30 * SR)]),
                       ("fixed 25 s windows", [s["audio"][i:i + 25 * SR] for i in range(0, len(s["audio"]), 25 * SR)]),
                       ("quiet-point cuts <= 30 s", quiet_windows(s["audio"], 30)),
                       ("quiet-point cuts <= 20 s", quiet_windows(s["audio"], 20))):
        t0 = time.perf_counter()
        hyp = NORM_EN(" ".join(W.transcribe(w, language="en")["text"] for w in wins))
        results[name] = 100 * jiwer.wer(s["ref"], hyp or "<empty>")
        print(f"   {name:26s} {len(wins):2d} calls   WER {results[name]:5.2f}%   {1000*(time.perf_counter()-t0):4.0f} ms   "
              f"windows of {', '.join(f'{len(w)/SR:.1f}' for w in wins)} s")
    t0 = time.perf_counter()
    steps = list(W.stream(iter([s["audio"][i:i + SR] for i in range(0, len(s["audio"]), SR)]), language="en"))
    hyp = NORM_EN(" ".join(x["text"] for x in steps if x["text"]))
    results["stream(), 1 s chunks"] = 100 * jiwer.wer(s["ref"], hyp or "<empty>")
    print(f"   {'stream(), 1 s chunks':26s} {len(steps):2d} passes  WER {results['stream(), 1 s chunks']:5.2f}%   {1000*(time.perf_counter()-t0):4.0f} ms")
    best = min(results, key=results.get)
    return (f"one call on {s['dur']:.0f} s keeps {len(NORM_EN(full['text']).split())}/{len(s['ref'].split())} words; {best}: {results[best]:.2f}% WER "
            f"(fixed 30 s windows {results['fixed 30 s windows']:.2f}%)")

long_audio()

Joining one speaker&#8217;s utterances gives a long clip with an exact reference, and the README promises windowing beyond the 30 s limit. A shorter cut comes back almost word for word, but the pinned 3.3.0 engine silently drops the middle of the full clip, returning fewer than half its words with no error. The 3.2.0 engine refuses such audio with a RuntimeError instead, so the two builds disagree and the split is ours to make. Splitting at quiet points scores 3.75% WER against 6.74% for fixed windows, though one clip cannot settle it.

Copy CodeCopiedUse a different Browser

@section("6. Streaming: cost per pass, how long a word waits to be committed, and what chunk size changes")
def streaming():
    durs = [s["dur"] for s in SESSIONS]
    print(f"{len(SESSIONS)} same-speaker sessions of {', '.join(f'{x:.0f}' for x in durs)} s, "
          f"{sum(len(s['ref'].split()) for s in SESSIONS)} reference words; the joins between utterances are artificial")
    off = {c["id"]: h for split in ("other", "clean") for c, h in zip(EN[split], HYP[(split, "Whistle")])}
    off_err = [sum(wer_counts(c["ref"], NORM_EN(off[c["id"]]))[0] for c in s["clips"]) for s in SESSIONS]
    words = [len(s["ref"].split()) for s in SESSIONS]
    print(f"the same utterances one at a time through transcribe() (the step 3 outputs): WER {100*sum(off_err)/sum(words):.2f}%\n")
    print(f"{'chunk':>6s} {'sessions':>8s} | {'WER':>6s} | {'pass ms mean / max':>18s} | {'passes > 1 s':>12s} | {'commit latency median / p90':>27s} | {'words only in tail':>18s} | {'pass vs time r':>14s}")
    summary, stream_err = {}, None
    for chunk_s, sessions in ((1.0, SESSIONS), (0.5, SESSIONS[:2]), (1.0, SESSIONS[:2]), (2.0, SESSIONS[:2])):
        n = int(chunk_s * SR)
        errs, tail, allw = [], 0, 0
        pass_ms, lat, rs = [], [], []
        for s in sessions:
            steps = list(W.stream(iter([s["audio"][i:i + n] for i in range(0, len(s["audio"]), n)]), language="en"))
            errs.append(wer_counts(s["ref"], NORM_EN(" ".join(x["text"] for x in steps if x["text"])))[0])
            body = steps[:-1]
            pass_ms += [x["pass_ms"] for x in body]
            lat += [x["received"] - wd["end"] for x in steps for wd in x["words"]]
            tail += len(steps[-1]["words"])
            allw += sum(len(x["words"]) for x in steps)
            if len(body) > 2:
                rs.append(np.corrcoef([x["received"] for x in body], [x["pass_ms"] for x in body])[0, 1])
        w = words[:len(sessions)]
        summary[(chunk_s, len(sessions))] = (100 * sum(errs) / sum(w), np.median(lat), np.mean(pass_ms))
        if chunk_s == 1.0 and len(sessions) == len(SESSIONS):
            stream_err = errs
        print(f"{chunk_s:5.1f} s {len(sessions):8d} | {100*sum(errs)/sum(w):5.2f}% | {np.mean(pass_ms):9.0f} / {max(pass_ms):4.0f} | {sum(p > 1000 for p in pass_ms):12d} | "
              f"{np.median(lat):12.2f} / {np.percentile(lat, 90):4.2f} s | {100*tail/allw:17.1f}% | {np.mean(rs):+.2f}")
    c = paired_contrast(list(range(len(SESSIONS))), stream_err, words, off_err, "stream, 1 s chunks", "one utterance at a time")
    print(f"\nstream (1 s chunks, 8 sessions) minus utterance-by-utterance: {c['diff']:+.2f} pts (95% session-cluster CI {c['lo']:+.2f}..{c['hi']:+.2f}, "
          f"{c['clusters']} sessions) -> {'no significant difference' if c['lo'] <= 0 <= c['hi'] else 'a real gap'} at this n")
    print("   pass_ms is the engine time per chunk; below the chunk length means real time. Commit latency is the stream time")
    print("   at which a word was committed minus the word's end: each chunk re-transcribes the recent audio and commits what two")
    print("   passes agree on, so the wait scales with the chunk. r is the correlation of pass time with stream time (buffer growth).")
    print("   The three chunk sizes are compared on the same two sessions; the eight-session row is the headline for 1 s chunks.")
    a8, a1, a05, a2 = summary[(1.0, len(SESSIONS))], summary[(1.0, 2)], summary[(0.5, 2)], summary[(2.0, 2)]
    return (f"1 s chunks on 8 sessions: WER {a8[0]:.2f}% vs {100*sum(off_err)/sum(words):.2f}% utterance by utterance, median commit {a8[1]:.2f} s; "
            f"on 2 sessions the median commit is {a05[1]:.2f} / {a1[1]:.2f} / {a2[1]:.2f} s for 0.5 / 1 / 2 s chunks")

streaming()

Streaming through stream() re-transcribes recent audio, committing a word once two consecutive passes agree, so waits grow with chunk size. Eight same-speaker sessions, made by joining utterances, stream in one-second chunks at 10.05% WER, against 10.41% when the same utterances are transcribed one at a time, a non-significant difference. A word is committed a median 1.68 s after it ends, and on two sessions the median rises from 0.78 s at half-second chunks to 3.44 s at two-second chunks. The joins are artificial, so this tests the mechanism, not conversation.

Copy CodeCopiedUse a different Browser

def auroc(scores, labels):
    """Probability that a random positive scores above a random negative (Mann-Whitney)."""
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    if not pos or not neg:
        return float("nan")
    order = sorted((s, i) for i, s in enumerate(scores))
    ranks, i = {}, 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and order[j + 1][0] == order[i][0]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k][1]] = (i + j) / 2 + 1
        i = j + 1
    pos_idx = [i for i, l in enumerate(labels) if l]
    return (sum(ranks[i] for i in pos_idx) - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))

@section("7. Word timestamps and word probabilities: consistency, a known shift, agreement with Whisper, and what p < 0.7 means")
def timestamps():
    import difflib
    pk = EN["other"][:40]
    key = lambda w: re.sub(r"[^a-z']", "", w.lower())
    diffs, same, mono, shifts = [], 0, 0, []
    probs, correct, durs = [], [], []
    replay_hits = replay_n = 0
    for i, c in enumerate(pk):
        ws = W.transcribe(c["audio"], language="en", word_timestamps=True)["words"]
        mono += all(a["start"] <= a["end"] <= b["start"] + 1e-6 for a, b in zip(ws, ws[1:]))
        if i < 20:   # a known shift: 2.000 s of zeros in front should move every word by 2.000 s
            ws2 = W.transcribe(np.concatenate([np.zeros(2 * SR, np.float32), c["audio"]]), language="en", word_timestamps=True)["words"]
            if ws2 and ws:
                shifts.append(ws2[0]["start"] - ws[0]["start"])
        if i < 20 and len(ws) >= 6:   # cut the audio where word k ends and transcribe only the cut
            k = len(ws) // 2
            got = NORM_EN(W.transcribe(c["audio"][:int(ws[k]["end"] * SR)], language="en")["text"]).split()
            exp = NORM_EN(" ".join(w["word"] for w in ws[:k + 1])).split()
            replay_n += 1
            replay_hits += got == exp
        torch.manual_seed(0)
        WHISPER_SECONDS["base"] += c["dur"]
        ww = [w for s in whisper_model("base").transcribe(c["audio"], language="en", fp16=False, word_timestamps=True)["segments"] for w in s["words"]]
        if [key(w["word"]) for w in ws] == [key(w["word"]) for w in ww]:
            same += 1
            diffs += [x["start"] - y["start"] for x, y in zip(ws, ww)] + [x["end"] - y["end"] for x, y in zip(ws, ww)]
        H, tp, td = [], [], []
        for w in ws:
            for t in NORM_EN(w["word"]).split():   # "hmm" normalises to nothing, "didn't" to two tokens, as in the reference
                H.append(t)
                tp.append(w["probability"])
                td.append(w["end"] - w["start"])
        ok = [False] * len(H)
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=c["ref"].split(), b=H).get_opcodes():
            if tag == "equal":
                for j in range(j1, j2):
                    ok[j] = True
        probs += tp
        correct += ok
        durs += td
    diffs, shifts = np.abs(diffs), np.array(shifts)
    print(f"{len(pk)} test-other clips: word times monotonic on {mono}/{len(pk)}")
    print(f"2.000 s of silence prepended on 20 clips: first word moved by {np.median(shifts):.3f} s (median), within 50 ms of 2.000 on "
          f"{100*np.mean(np.abs(shifts-2) <= 0.05):.0f}% of clips")
    print(f"cut-and-replay: cutting the audio at a word's 'end' and transcribing the cut reproduced the exact word prefix on {replay_hits}/{replay_n} clips")
    print(f"agreement with Whisper base's DTW word times, on the {same}/{len(pk)} clips where both emit the same words ({len(diffs)//2} words; a selected, easier subset):")
    print(f"   |boundary difference| median {np.median(diffs):.3f} s, within 100 ms {100*np.mean(diffs <= 0.1):.0f}%, within 200 ms "
          f"{100*np.mean(diffs <= 0.2):.0f}%   (agreement between two systems, not accuracy: there is no gold alignment)")
    probs, correct, durs = np.array(probs), np.array(correct), np.array(durs)
    print(f"\nword probability over {len(probs)} normalised tokens from {len(pk)} clips: median {np.median(probs):.3f}, 10th percentile {np.percentile(probs, 10):.3f}")
    for lo, hi in ((0, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.01)):
        m = (probs >= lo) & (probs < hi)
        if m.sum():
            print(f"   p in [{lo:.1f}, {min(hi, 1):.1f}): {m.sum():4d} words, {100*(~correct[m]).mean():5.1f}% wrong")
    print(f"   AUROC for 'this word is wrong': 1 - probability {auroc(-probs, ~correct):.3f}; word duration as a baseline (shorter = riskier) {auroc(-durs, ~correct):.3f}")
    low, high = probs < 0.7, probs >= 0.7
    return (f"shift {np.median(shifts):.2f} s; within 200 ms of Whisper on {100*np.mean(diffs <= 0.2):.0f}% of {len(diffs)//2} matched words; "
            f"p<0.7 words wrong {100*(~correct[low]).mean():.0f}% vs {100*(~correct[high]).mean():.1f}%")

timestamps()

Without gold alignments, we check timings against what they must satisfy. Word times are monotonic on every clip we check, and prepending a two-second silence to twenty clips shifts the first word by a median of 2.000 s. Cutting at a word&#8217;s end should reproduce its prefix, which holds on only a fifth of those twenty clips; this tests stability, not end-time accuracy. Probability is the stronger signal: words rated below one half were wrong 69.2% of the time, against 2.5% at 0.9 or above, and AUROC is 0.916 for wrong words, against 0.509 for duration.

Copy CodeCopiedUse a different Browser

@section("8. Keyword biasing: an oracle ceiling, a matched wrong-keyword control and a distractor list")
def keywords():
    import difflib
    clips = EN["other"]
    base = HYP[("other", "Whistle")]
    freq = collections.Counter(w for c in clips for w in c["ref"].split())

    def error_words(ref, hyp):
        out = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=ref.split(), b=NORM_EN(hyp).split()).get_opcodes():
            if tag in ("replace", "delete"):
                out += ref.split()[i1:i2]
        return sorted(set(out))
    oracle = [error_words(c["ref"], h) for c, h in zip(clips, base)]
    idx = [i for i, k in enumerate(oracle) if k]
    print(f"{len(idx)}/{len(clips)} test-other clips have at least one Whistle error ({sum(len(oracle[i]) for i in idx)} distinct wrong words)")
    print("   oracle keywords  = the reference words Whistle got wrong on that clip (a CEILING: it reads the answer)")
    print("   matched wrong    = the next error clip's oracle list, minus every word the target clip actually says")
    print("   distractor (8)   = the 8 most frequent reference words of the whole sample that the target clip does not say")
    print("   distractor (2)   = the same list cut to 2 words, so its size matches the oracle and matched arms\n")

    def matched_wrong(i):
        donor = oracle[idx[(idx.index(i) + 1) % len(idx)]]
        return [w for w in donor if w not in clips[i]["ref"].split()] or None
    arms = {}
    distractor = lambda i, k: [w for w, _ in freq.most_common(60) if w not in clips[i]["ref"].split()][:k]
    for name, keylist in (("no keywords", lambda i: None), ("oracle (ceiling)", lambda i: oracle[i]), ("matched wrong", matched_wrong),
                          ("distractor (8)", lambda i: distractor(i, 8)), ("distractor (2)", lambda i: distractor(i, 2))):
        errs, words, ins, recovered, total_kw, bad_kw, bad_kw_base, n_kw = [], [], 0, 0, 0, 0, 0, 0
        for i in idx:
            c = clips[i]
            kws = keylist(i)
            n_kw += len(kws or [])
            h = base[i] if name == "no keywords" else W.transcribe(c["audio"], language="en", keywords=kws)["text"]
            s, d, ins_i = sdi(c["ref"], NORM_EN(h))
            errs.append(s + d + ins_i)
            words.append(len(c["ref"].split()))
            ins += ins_i
            still_wrong = set(error_words(c["ref"], h))
            recovered += sum(w not in still_wrong for w in oracle[i])
            total_kw += len(oracle[i])
            if kws and name != "oracle (ceiling)":
                bad_kw += sum(w in NORM_EN(h).split() for w in kws)
                bad_kw_base += sum(w in NORM_EN(base[i]).split() for w in kws)
        arms[name] = (errs, words)
        extra = f"   wrong keywords in the output {bad_kw:3d} (already {bad_kw_base} without biasing)" if name not in ("no keywords", "oracle (ceiling)") else ""
        print(f"   {name:18s} {n_kw/len(idx):4.1f} keywords/clip   WER {corpus_wer(errs, words):6.2f}%   insertions {ins:3d}   oracle words now right {recovered:3d}/{total_kw}{extra}")
    spk = [clips[i]["spk"] for i in idx]
    w = arms["no keywords"][1]
    fam = []
    for a, b in (("no keywords", "oracle (ceiling)"), ("matched wrong", "no keywords"), ("distractor (8)", "no keywords"),
                 ("distractor (2)", "no keywords"), ("matched wrong", "oracle (ceiling)")):
        c = paired_contrast(spk, arms[a][0], w, arms[b][0], a, b)
        fam.append(c)
    sig = holm([c["p"] for c in fam])
    print(f"\n   family B, {len(fam)} contrasts, Holm at 0.05:")
    for c, s in zip(fam, sig):
        print(f"   WER({c['a']}) - WER({c['b']}) = {fmt_contrast(c)}  p~{c['p']:.3f}  {'significant' if s else 'not significant'}")
    print("   the decisive contrast is matched wrong minus oracle: how much of the gain needs the right words, not just any words")
    return (f"oracle ceiling {corpus_wer(*arms['oracle (ceiling)']):.2f}% vs {corpus_wer(*arms['no keywords']):.2f}% baseline; "
            f"wrong keywords {corpus_wer(*arms['matched wrong']):.2f}%")

keywords()

Keyword biasing needs controls, because an oracle that reads the answer looks like a win. The oracle lists the words Whistle got wrong; the matched control uses another clip&#8217;s, minus any this clip says. On the 185 clips with errors, the oracle cuts WER from 14.74% to 7.62%, while matched wrong words leave it at 14.82%, a non-significant change. Eight frequent words the clip lacks raise WER 2.05 points. Against the oracle, matched wrong words are 7.20 points worse, significant after Holm correction, so the right words matter.

Copy CodeCopiedUse a different Browser

MLS = {"de": "german", "fr": "french", "es": "spanish", "it": "italian", "nl": "dutch", "pl": "polish"}
WHISTLE_LANGS = ("en", "de", "fr", "es", "it", "nl", "pl")
N_PER_LANG = 12
PUBLISHED_MLS_BASE = {"nl": 28.4, "fr": 26.6, "de": 17.7, "it": 31.1, "pl": 22.8, "es": 12.8}   # Whisper paper, table 10 (full splits)

def clopper_pearson_lower(k, n, alpha=0.05):
    """Exact one-sided 95% lower bound for a binomial proportion, by bisection on the binomial tail."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        p = (lo + hi) / 2
        tail = sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))
        lo, hi = (p, hi) if tail < alpha else (lo, p)
    return lo

@section("9. Six more languages on Multilingual LibriSpeech, pooled, with a symmetric language-ID test")
def multilingual():
    rng = random.Random(SEED)
    print(f"sampling rule, fixed in advance: {N_PER_LANG} clips per language from 3 random pages of 100 rows of each test split (seed {SEED});")
    print("MLS pages are speaker-sorted, so the pages are the first stage of the sample. Normaliser: Whisper's BasicTextNormalizer on both sides.\n")
    pooled = {"Whistle (forced)": [], "Whistle (detected)": [], "whisper base, greedy": []}
    words, clusters, lid_w, lid_b, rows_out = [], [], 0, 0, []
    wb = whisper_model("base")
    for code, cfg in MLS.items():
        total = page("facebook/multilingual_librispeech", cfg, "test", 0, 1)["num_rows_total"]
        offsets = rng.sample(range(0, total, 100), 3)
        rows = [r["row"] for off in offsets for r in page("facebook/multilingual_librispeech", cfg, "test", off)["rows"]]
        sample = rng.sample(rows, N_PER_LANG)
        e, n_words, spk = collections.defaultdict(list), [], []
        for r in sample:
            audio, h = load_audio(r)
            MANIFEST.setdefault("mls", {}).setdefault(code, []).append([r["id"], h])
            ref = NORM_BASIC(r["transcript"])
            forced = W.transcribe(audio, language=code)["text"]
            det = W.transcribe(audio)
            lid_w += det["language"] == code
            hb, _, _ = run_whisper("base", audio, language=code)
            mel = whisper.log_mel_spectrogram(whisper.pad_or_trim(audio), n_mels=wb.dims.n_mels)
            _, probs = wb.detect_language(mel)
            lid_b += max(WHISTLE_LANGS, key=lambda l: probs.get(l, 0)) == code
            for name, h in (("Whistle (forced)", forced), ("Whistle (detected)", det["text"]), ("whisper base, greedy", hb)):
                e[name].append(wer_counts(ref, NORM_BASIC(h))[0])
            n_words.append(len(ref.split()))
            spk.append(f"{code}-{r['speaker_id']}")
        for name in pooled:
            pooled[name] += e[name]
        words += n_words
        clusters += spk
        rows_out.append((code, len(sample), len(set(spk)), sum(n_words), corpus_wer(e["Whistle (forced)"], n_words), corpus_wer(e["whisper base, greedy"], n_words)))
    print(f"{'lang':>4s} {'clips':>5s} {'spk':>3s} {'words':>5s} | {'Whistle':>8s} {'base':>8s} | Whisper base published on the full split (paper table 10)")
    for code, n, s, nw, ww, wbase in rows_out:
        print(f"{code:>4s} {n:5d} {s:3d} {nw:5d} | {ww:7.1f}% {wbase:7.1f}% | {PUBLISHED_MLS_BASE[code]}")
    print("   per-language rows are descriptive: 12 clips from a handful of speakers cannot rank the systems within a language\n")
    c = paired_contrast(clusters, pooled["whisper base, greedy"], words, pooled["Whistle (forced)"], "whisper base, greedy", "Whistle")
    c["name"] = "MLS pooled: Whistle vs whisper base, greedy"
    CONTRASTS.append(c)
    print(f"pooled over {len(words)} clips / {c['clusters']} speakers / {sum(words)} words: Whistle (forced) {corpus_wer(pooled['Whistle (forced)'], words):.2f}%, "
          f"whisper base greedy {corpus_wer(pooled['whisper base, greedy'], words):.2f}%; {fmt_contrast(c)}  [family A]")
    print(f"Whistle with the language detected instead of forced: {corpus_wer(pooled['Whistle (detected)'], words):.2f}%")
    n = len(words)
    print(f"language identification over the same seven labels: Whistle {lid_w}/{n} (one-sided 95% lower bound {100*clopper_pearson_lower(lid_w, n):.0f}%, "
          f"treating clips as independent), whisper base {lid_b}/{n} (lower bound {100*clopper_pearson_lower(lid_b, n):.0f}%)")
    json.dump(MANIFEST, open("manifest.json", "w"))
    fam = [x for x in CONTRASTS if x["name"] in FAMILY_A]
    sig = dict(zip([x["name"] for x in fam], holm([x["p"] for x in fam])))
    print(f"\nfamily A complete ({len(fam)} contrasts), Holm at 0.05 (the printed CIs are unadjusted; the verdict uses the adjusted p):")
    for x in fam:
        v = verdict(x, sig[x["name"]])
        VERDICTS.append((x["name"], fmt_contrast(x), v))
        print(f"   {x['name']:48s} {fmt_contrast(x)}  p~{x['p']:.3f}  -> {v}")
    return f"pooled WER Whistle {corpus_wer(pooled['Whistle (forced)'], words):.1f}% vs base {corpus_wer(pooled['whisper base, greedy'], words):.1f}%; language ID {lid_w}/{n} vs {lid_b}/{n}"

multilingual()

Forcing the true language would hide detection failures, so each system must also detect the language. We draw 12 clips per language from three random pages, fixed in advance, and score both sides with BasicTextNormalizer. We pin no MLS revision, so each clip is hashed instead. Pooled over 72 clips from 22 speakers, forced Whistle scores 26.40% against 24.06% for greedy Whisper base, a gap in Whisper&#8217;s favour that is not significant. Both systems detect the language on all 72 clips. Per-language rows are descriptive only.

Copy CodeCopiedUse a different Browser

@section("10. Non-speech, quiet speech and white noise at three SNRs, Whistle against Whisper base")
def noise():
    rng = np.random.default_rng(SEED)
    quiet = EN["other"][0]["audio"] * (10 ** (-30 / 20) / np.sqrt(np.mean(EN["other"][0]["audio"] ** 2)))
    probes = {"5 s digital silence": np.zeros(5 * SR, np.float32),
              "white noise, -40 dBFS": (rng.standard_normal(5 * SR) * 0.01).astype(np.float32),
              "white noise, -20 dBFS": (rng.standard_normal(5 * SR) * 0.1).astype(np.float32),
              "440 Hz tone, -20 dBFS": (0.1 * np.sqrt(2) * np.sin(2 * np.pi * 440 * np.arange(5 * SR) / SR)).astype(np.float32),
              "speech scaled to -30 dBFS": quiet.astype(np.float32)}
    print(f"{'input':>26s} | Whistle text / language           | Whisper base text")
    for name, x in probes.items():
        w = W.transcribe(x, language="en")
        b = run_whisper("base", x)[0].strip()
        print(f"{name:>26s} | {w['text']!r} {w['language']!r} | {b!r}")
    print(f"   reference for the quiet clip: {EN['other'][0]['ref']}")
    print("   an empty Whisper output is its no-speech gate, not evidence of quality; an empty Whistle output on real speech would be a miss\n")
    clips = EN["other"][:20]
    spk = [c["spk"] for c in clips]
    words = [len(c["ref"].split()) for c in clips]
    print(f"white noise on {len(clips)} test-other clips, {sum(words)} words, {len(set(spk))} speakers (directional at this n):")
    print(f"{'condition':>14s} | {'Whistle':>8s} {'base greedy':>11s} | WER(base) - WER(Whistle), 95% speaker-cluster CI")
    out = []
    for snr in (None, 20, 10, 5):
        xs = []
        for c in clips:
            if snr is None:
                xs.append(c["audio"])
            else:
                n = rng.standard_normal(len(c["audio"])).astype(np.float32)
                n *= np.sqrt((c["audio"] ** 2).mean() / ((n ** 2).mean() * 10 ** (snr / 10)))
                y = c["audio"] + n
                xs.append((y * min(1, 0.99 / np.abs(y).max())).astype(np.float32))
        e_w = [wer_counts(c["ref"], NORM_EN(W.transcribe(x, language="en")["text"]))[0] for c, x in zip(clips, xs)]
        e_b = [wer_counts(c["ref"], NORM_EN(run_whisper("base", x)[0]))[0] for c, x in zip(clips, xs)]
        c = paired_contrast(spk, e_b, words, e_w, "base", "Whistle")
        label = "clean" if snr is None else f"{snr} dB SNR"
        out.append((label, corpus_wer(e_w, words), corpus_wer(e_b, words)))
        print(f"{label:>14s} | {corpus_wer(e_w, words):7.1f}% {corpus_wer(e_b, words):10.1f}% | {c['diff']:+6.1f} ({c['lo']:+.1f}..{c['hi']:+.1f})")
    print("\n   Whistle's front end keeps roughly 250-3500 Hz while Whisper's covers 0-8 kHz, so the two systems do not see the same")
    print("   noise; this compares them as shipped, and at n = 20 none of the differences is distinguishable from zero.")
    return "; ".join(f"{l}: {w:.0f}% vs {b:.0f}%" for l, w, b in out[1:])

noise()

Digital silence, two noise levels, and a pure tone all give empty text. For Whisper that is a no-speech gate, not evidence of quality, and an empty Whistle output on speech would be a miss. A real sentence at -30 dBFS comes back word for word from Whistle, though Whisper base writes &#8216;crazed&#8217; for &#8216;traced&#8217;. At the harshest SNR we ran, white noise lifts WER on 20 test-other clips from 12.4% to 37.1% for Whistle and from 15.2% to 39.9% for Whisper base, and no gap is distinguishable from zero.

Copy CodeCopiedUse a different Browser

@section("11. Speech embeddings: the measured frame rate, and finding a spoken word inside another clip")
def embeddings():
    frames = {}
    for secs in (1, 10, 30):
        v = np.asarray(W.embed(audio_seconds(EN["other"], secs)), np.float32)
        frames[secs] = len(v) // 256
        print(f"{secs:2d} s of audio -> {len(v):7d} floats = {len(v)//256:4d} frames x 256  ({len(v)/256/secs:.1f} frames/s, {1000*secs/(len(v)/256):.1f} ms per frame)")
    fps = frames[10] / 10
    try:
        W.embed(np.zeros(31 * SR, np.float32))
    except RuntimeError as e:
        print(f"31 s -> RuntimeError: {e}")
    print("\nspoken-term search: embed clip A whole, keep the frames under one word's own timestamps as the query (the encoder is")
    print("non-causal, so those frames carry context), slide the query over clip B's frames with a cosine score. Pool: the first 120")
    print("test-other clips; words of 5+ letters and 0.25 s+, first two occurrences in different clips; a hit is a peak within 0.3 s.")
    clips = [c for c in EN["other"][:120]]
    key = lambda w: re.sub(r"[^a-z']", "", w.lower())
    occurrences = collections.defaultdict(list)
    for i, c in enumerate(clips):
        for w in W.transcribe(c["audio"], language="en", word_timestamps=True)["words"]:
            if len(key(w["word"])) >= 5 and w["end"] - w["start"] >= 0.25:
                occurrences[key(w["word"])].append((i, w["start"], w["end"]))
    pairs = [(k, o[0], o[1]) for k, o in occurrences.items() if len(o) >= 2 and o[0][0] != o[1][0]]
    cache = {}

    def frames_of(i):
        if i not in cache:
            v = np.asarray(W.embed(clips[i]["audio"]), np.float32).reshape(-1, 256)
            cache[i] = v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-8)
        return cache[i]
    hits = n = 0
    chance, tol = [], 0.3
    for k, (ia, sa, ea), (ib, sb, eb) in pairs[:60]:
        q = frames_of(ia)[int(sa * fps):max(int(sa * fps) + 2, int(ea * fps))]
        T = frames_of(ib)
        if len(T) <= len(q):
            continue
        scores = np.array([(q * T[j:j + len(q)]).sum(1).mean() for j in range(len(T) - len(q) + 1)])
        peak = (scores.argmax() + len(q) / 2) / fps
        hit = sb - tol <= peak <= eb + tol
        hits += hit
        n += 1
        chance.append((eb - sb + 2 * tol) / clips[ib]["dur"])
        if n <= 3:
            print(f"   {k!r:14s} query {ea-sa:.2f} s from clip {ia:3d} -> peak at {peak:5.2f} s in clip {ib:3d}; the word is spoken at {sb:.2f}-{eb:.2f} s: {'hit' if hit else 'miss'}")
    print(f"   {hits}/{n} peaks inside the target word (+-{tol} s); a random position would land there about {100*np.mean(chance):.0f}% of the time")
    print("   the encoder output is a content representation at frame level; it is not a speaker or sentence embedding")
    return f"{fps:.1f} frames/s x 256 floats; spoken-term search {hits}/{n} hits (chance ~{100*np.mean(chance):.0f}%)"

embeddings()

Frame rate is measured because the search maps frames to seconds. A ten-second clip yields 25 frames a second, each a 256-float vector, and clips past the embedding limit raise a RuntimeError. We embed a clip whole, since its frames see both sides, and slide one word&#8217;s frames across another clip by cosine score. The peak lands within 0.3 s of the word on 32 of 34 pairs of words with five or more letters, where chance gives about 17%. The output is frame-level content, not a sentence embedding.

Copy CodeCopiedUse a different Browser

INTENTS = {"abroad": "Using the card or account while travelling or abroad",
           "address": "Change, update or confirm the postal address on the account",
           "app_error": "The banking app or website shows an error or does not work",
           "atm_limit": "The daily ATM cash withdrawal limit",
           "balance": "Check the current account balance",
           "business_loan": "Apply for or ask about a business loan",
           "card_issues": "A card is lost, stolen, blocked, declined or not working",
           "cash_deposit": "Deposit or transfer cash into the account",
           "direct_debit": "Set up, change or cancel a direct debit or standing order",
           "freeze": "Freeze, block or unfreeze the account or card",
           "high_value_payment": "Make or authorize a large or high-value payment or transfer",
           "joint_account": "Open or ask about a joint account with another person",
           "latest_transactions": "See the latest or recent transactions and payments",
           "pay_bill": "Pay a bill or make a payment to a company"}
N_MINDS = 200

@section("12. From speech to a tool call: Whistle transcripts into Needle 3 on MInDS-14 banking requests")
def speech_to_tools():
    tools = [{"name": n, "description": d, "parameters": {"type": "object", "properties": {}}} for n, d in INTENTS.items()]
    print(f"14 tools, one per MInDS-14 intent, descriptions fixed before the first call (sha256 {hashlib.sha256(json.dumps(tools).encode()).hexdigest()[:12]})")
    first = page("PolyAI/minds14", "en-US", "train", 0, 1)
    names = next(f for f in first["features"] if f["name"] == "intent_class")["type"]["names"]
    assert names == list(INTENTS), names
    rows = all_rows("PolyAI/minds14", "en-US", "train")
    sample = random.Random(SEED).sample(rows, N_MINDS)
    clips, too_long = [], 0
    for r in sample:
        audio, h = load_audio(r)        # 8 kHz telephone wav, resampled to 16 kHz by load_audio
        MANIFEST.setdefault("minds14", []).append([r["path"], h])
        if len(audio) / SR > MAX_CLIP_S:   # the same pre-declared filter as step 2: the engine refuses longer clips
            too_long += 1
            continue
        clips.append({"audio": audio, "ref": r["transcription"], "intent": names[r["intent_class"]], "dur": len(audio) / SR})
    t0 = time.perf_counter()
    hyps = [W.transcribe(c["audio"], language="en")["text"] for c in clips]
    tw = time.perf_counter() - t0
    e, n = zip(*[wer_counts(NORM_EN(c["ref"]), NORM_EN(h)) for c, h in zip(clips, hyps)])
    json.dump(MANIFEST, open("manifest.json", "w"))
    print(f"{len(clips)} of the {N_MINDS} sampled clips ({len(rows)} rows in the split; {too_long} dropped for exceeding {MAX_CLIP_S:.0f} s; "
          f"{sum(c['dur'] for c in clips)/60:.1f} min of 8 kHz telephone speech): Whistle WER {corpus_wer(e, n):.1f}% "
          f"against the casual MInDS-14 transcriptions, {1000*tw/len(clips):.0f} ms per clip")
    for c, h in list(zip(clips, hyps))[:2]:
        print(f"   [{c['intent']}] ref: {c['ref'][:72]}\n   {' ' * (len(c['intent']) + 2)} hyp: {h[:72]}")
    t0 = time.perf_counter()
    agent = needle.Needle(tools=tools, auto_date=False)   # no date fact in the prompt, so the result does not depend on the clock
    print(f"\nNeedle 3 loaded in {time.perf_counter()-t0:.1f} s into the same engine; Whistle stays loaded beside it")

    def route(texts):
        out = []
        for t in texts:
            r = agent.complete(t)
            agent.reset()
            calls = [c["name"] for c in r.get("function_calls", [])]
            out.append((calls[0] if calls else None, r.get("confidence") or 0.0, r.get("peak_ram_mb")))
        return out
    truth = [c["intent"] for c in clips]
    res = {}
    for label, texts in (("reference transcripts", [c["ref"] for c in clips]), ("Whistle transcripts", hyps)):
        t0 = time.perf_counter()
        res[label] = route(texts)
        right = np.array([p == y for (p, _, _), y in zip(res[label], truth)])
        conf = np.array([c for _, c, _ in res[label]])
        print(f"   routing from {label:21s}: {100*right.mean():.1f}% correct, {sum(p is None for p, _, _ in res[label])} refusals, "
              f"{1000*(time.perf_counter()-t0)/len(texts):.0f} ms/call, confidence when right {conf[right].mean():.2f} vs wrong {conf[~right].mean():.2f}")
    a = [p == y for (p, _, _), y in zip(res["reference transcripts"], truth)]
    b = [p == y for (p, _, _), y in zip(res["Whistle transcripts"], truth)]
    only_ref, only_wh = sum(x and not y for x, y in zip(a, b)), sum(y and not x for x, y in zip(a, b))
    m = only_ref + only_wh
    p_mc = min(1.0, 2 * sum(math.comb(m, j) for j in range(min(only_ref, only_wh) + 1)) / 2 ** m) if m else 1.0
    print(f"   discordant clips: right only from the reference text {only_ref}, right only from Whistle's text {only_wh} (exact McNemar p = {p_mc:.2f})")
    conf = collections.Counter((y, p) for (p, _, _), y in zip(res["Whistle transcripts"], truth) if p != y)
    print("   most common confusions (truth -> call): " + ", ".join(f"{y} -> {p} x{k}" for (y, p), k in conf.most_common(3)))
    off = route([NORM_EN(h) for h in HYP[("other", "Whistle")][:40]])
    print(f"   40 LibriSpeech sentences (off-topic): {sum(p is None for p, _, _ in off)} refused, {sum(p is not None for p, _, _ in off)} given a banking tool call")
    print(f"   peak_ram_mb reported by Needle: {res['Whistle transcripts'][-1][2]} MB (this whole process, Whisper models included). MInDS-14 is public,")
    print("   so training-set overlap cannot be ruled out for either model, and the tool descriptions are ours: the number moves with them.")
    return f"routing {100*np.mean(b):.0f}% right from Whistle's text vs {100*np.mean(a):.0f}% from the reference text; WER {corpus_wer(e, n):.0f}%"

speech_to_tools()

Whistle transcribes the sampled MInDS-14 banking requests at 31.9% WER against casual reference transcripts. Needle 3 routes each transcript among fourteen tools, one per banking intent, whose descriptions we wrote. The returned function call becomes the route, and a reply with no call counts as a refusal. Routing is right 50.3% of the time from Whistle&#8217;s text and 51.8% from reference text, a non-significant gap, so with these descriptions, routing, not transcription, is the limit. Of the off-topic LibriSpeech sentences, 17 are refused, and the rest get a banking tool call.

Copy CodeCopiedUse a different Browser

banner("SUMMARY")
for name, res in RESULTS.items():
    print(f"  {name:<104s}  {res}")
print("\nVerdicts on the published-claim contrasts (family A, 95% speaker-cluster paired bootstrap, unadjusted CIs, Holm over 5):")
for claim, measured, v in VERDICTS:
    print(f"  {claim:<48s} {measured:<58s} {v}")
print(f"\nWhisper audio transcribed in this run: " + ", ".join(f"{k} {v/60:.1f} min" for k, v in WHISPER_SECONDS.items())
      + f"; hardware {CPU}")
print("""
What to carry over
 - Pin the Hub revisions of whistle.cact, the engine wheel and needle3.cact and print their hashes; both repos replace files in
   place, and the engine version the package wants is in needle.agent.fetch.ENGINE_VERSIONS, not in the package version.
 - Score with the same normalizer on both sides of each comparison, sample with a fixed seed, cluster the bootstrap by speaker.
 - Say which Whisper you compared against: greedy (the package default) and beam search (the paper's numbers) differ.
 - Keep a single transcribe() call under 30 s; cut longer audio yourself (quiet points worked best on this clip) or use stream().
 - Word probability is a usable error signal, keyword biasing has a ceiling, embeddings are content frames.
Where to go next
 - pip install "cactus-needle[mic,compare]" then needle whistle compare clip.wav runs one clip through Whistle, Whisper and Moonshine.
 - needle download <platform> fetches the engine for macOS, Linux, Android, iOS, RISC-V, MIPS, the browser or WASI; the native
   runner takes --model needle3.cact --model whistle.cact --tools tools.json --audio clip.wav for audio-to-tool-calls in one call.
 - The weights also ship as safetensors, and fine-tuning for new languages is being discussed in the repository's issues.
 - Docs: cactuscompute.com/whistle    Code: github.com/cactus-compute/needle    Weights: huggingface.co/Cactus-Compute/whistle
""")

The summary prints each section&#8217;s one-line result, then the five published-claim verdicts, where only test-other against greedy Whisper base favors Whistle. It also reports the audio Whisper transcribed, 18.4 minutes for tiny and 68.7 for base, and all 13 cells ran without failure. The habits to carry over are pinning Hub revisions, fixing the seed, scoring both sides with one normalizer, and naming the Whisper decoder.

In conclusion, on an Apple M4 CPU, Whistle scored 10.47% on the test-other sample, near the published full-split 10.49, quoted, not measured. It beat greedy Whisper base by 2.19 points on the paired subset, while beam search, test-clean, and pooled MLS showed no significant gap. It ran 5.7 times faster than greedy base on a ten-second clip. Streaming with one-second chunks committed words a median 1.68 s after they end, with no significant loss. The 30 s limit matters most: the pinned engine silently drops the middle of longer audio, so split it or stream. These are one-run samples, and no single clip or small set can settle a claim.

Check out the FULL CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post A Coding Guide to Cactus Whistle: Does a 16.9 MB Speech Model Hold Up Against Whisper Base? Word Error Rate, Speed, Streaming, Timestamps, Keywords, and Speech-to-Tool Calls on a CPU appeared first on MarkTechPost.