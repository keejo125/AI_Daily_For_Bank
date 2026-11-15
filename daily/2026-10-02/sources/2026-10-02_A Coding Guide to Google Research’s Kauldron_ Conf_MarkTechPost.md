---
publish_time: 1790901170
link: https://www.marktechpost.com/2026/10/01/a-coding-guide-to-google-researchs-kauldron-configs-that-are-plain-data-components-wired-by-string-and-a-jax-trainer-you-can-read-end-to-end/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Google Research 开源的 JAX 训练库 Kauldron，主打研究速度与模块化。教程围绕其三大机制展开：konfig 将实验配置转化为可经 JSON 往返的纯字典树；kontext 用字符串键路径连接组件，使损失函数无需导入模型即可评分；运行时形状检查器以具名轴跨参数绑定，不匹配时报告绑定对象。文中还演示了自定义损失与指标、在合成数据上训练真实 Trainer、五变体单配置行扫描，以及训练断点自动续训。
---

# Google Kauldron：面向研究速度的 JAX 训练库编码指南

> 原文链接：https://www.marktechpost.com/2026/10/01/a-coding-guide-to-google-researchs-kauldron-configs-that-are-plain-data-components-wired-by-string-and-a-jax-trainer-you-can-read-end-to-end/
> 来源：MarkTechPost

In this tutorial, we implement Kauldron, the JAX training library from Google Research that describes itself as optimized for research velocity and modularity, and we take those two words literally by testing what they actually buy us. We install it, then spend the first half of the notebook on the three mechanisms that make Kauldron different from a stack of Flax and Optax: konfig, which turns an experiment into a tree of plain dictionaries that round-trip through JSON; kontext, which wires components together with string key paths so a loss never imports the model it scores; and the runtime shape checker, whose named axes bind across arguments and report what they were bound to when something does not match. We then write a custom loss and a custom metric in the shape the framework expects, train a real Trainer on synthetic in-memory data with no download and no accelerator, and monitor an inner layer of the model without editing the model. We finish by running a five-variant sweep in which every experiment differs by one config line, and by letting a training run checkpoint itself and resume where it stopped.

Copy CodeCopiedUse a different Browser

import os
import sys
import json
import textwrap
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

banner("0. Install Kauldron, and the one compatibility patch you need today")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "kauldron==1.4.2"], check=True)

import jax
from etils.enp import array_spec as _array_spec

# jax >= 0.10.1 moved `jax._src.prng`, but etils <= 1.14.0 still reaches for it whenever it
# inspects an array's dtype. Kauldron calls that code on every batch, so without this two-line
# patch a Trainer raises AttributeError before it finishes a single step. The replacement uses
# jax's own public dtype API and is a no-op on older jax.
if not hasattr(jax._src, "prng"):
    _array_spec._is_jax_random_dtype = lambda dt: jax.dtypes.issubdtype(dt, jax.dtypes.prng_key)

import numpy as np
import optax
import flax
from flax import linen as nn
import kauldron
from kauldron import kd, konfig, kontext
from kauldron.typing import Float, typechecked

print(f"  kauldron {kauldron.__version__}  |  jax {jax.__version__}  |  flax {flax.__version__}"
      f"  |  optax {optax.__version__}")
print(f"  devices: {jax.devices()}")
print("\n  Kauldron's pitch is modularity: it is the glue, not the framework. Four pieces do the work:")
print("    konfig    -> your experiment IS a Python call tree, and that tree is a plain dict")
print("    kontext   -> parts are wired by string key paths, so they never import each other")
print("    ktyping   -> Float['*b h w c'] checked at runtime, with named axes bound across args")
print("    kd.train  -> Trainer: model + data + losses + metrics + optimizer, and nothing else")
print("\n  Everything below runs on a CPU runtime with no dataset download: the data is synthetic.")

We install Kauldron and apply the one compatibility patch the current release combination needs. jax 0.10.1 moved the private module jax._src.prng, and etils up to 1.14.0 still reaches for it whenever it inspects an array&#8217;s dtype, which is a code path Kauldron runs on every batch. Without the two-line replacement below, which uses jax&#8217;s own public dtype API and is a no-op on older versions, a Trainer raises AttributeError before it completes a single step. With it in place we import the four pieces that do the work: konfig for the config system, kontext for the wiring, the typing module for runtime shape checks, and kd.train for the Trainer itself. Everything afterwards runs on a CPU runtime, because the only dataset in this notebook is one we generate.

Copy CodeCopiedUse a different Browser

@section("1. A config is a call tree, and a call tree is a dict")
def config_is_a_dict():
    with konfig.imports():
        import optax as coptax                      # looks like optax, builds ConfigDict instead

    cfg = coptax.adam(learning_rate=0.003)
    print(f"  cfg          = {cfg}")
    print(f"  type         = {type(cfg).__name__}")
    print(f"  __qualname__ = {cfg.__qualname__!r}   <- the call, stored as data")

    cfg.learning_rate = 1e-4                        # configs are mutable
    optimizer = konfig.resolve(cfg)                 # ...until you resolve them
    print(f"  after cfg.learning_rate = 1e-4 -> resolve() gives {type(optimizer).__name__}")

    print("\n  An arbitrarily complex optimizer is still just nested dicts:")
    chain = coptax.chain(
        coptax.clip_by_global_norm(1.0),
        coptax.scale_by_adam(b2=0.99),
        coptax.scale_by_learning_rate(0.003),
    )
    as_json = json.dumps(json.loads(chain.to_json()), indent=2)
    print(textwrap.indent(as_json, "    "))

    rebuilt = konfig.resolve(konfig.ConfigDict(json.loads(chain.to_json())))
    print(f"  JSON -> ConfigDict -> resolve() -> {type(rebuilt).__name__}")
    print("  optax has no idea konfig exists. No base class, no registry, no decorator.")
    return f"optax.chain -> JSON -> {type(rebuilt).__name__}"

config_is_a_dict()

We start with konfig, because it is the piece the rest of the library is built on. Inside a konfig.imports() block, importing optax gives us something that looks and autocompletes like optax but builds configuration instead of objects, so optax.adam(learning_rate=0.003) returns a ConfigDict holding the qualified name of the call and its arguments rather than an optimizer. That config is mutable until konfig.resolve turns it into the real thing, and because it is only nested dictionaries, an arbitrarily complex optax.chain serialises to JSON and comes back as a working optimizer. The important part is what optax had to do to support this: nothing. There is no base class, no registry, and no decorator anywhere in optax, and the same applies to any library we configure this way.

Copy CodeCopiedUse a different Browser

@section("2. cfg.ref: change one number, everything downstream follows")
def config_references():
    with konfig.imports():
        import optax as coptax
        from kauldron import kd as ckd

    cfg = ckd.train.Trainer()
    cfg.num_train_steps = 1000
    cfg.schedules = {
        "lr": coptax.warmup_cosine_decay_schedule(
            init_value=0.0, peak_value=1e-3, warmup_steps=100,
            decay_steps=cfg.ref.num_train_steps,    # <- a reference, not the value 1000
        )
    }
    at_1000 = konfig.resolve(cfg.schedules["lr"])
    cfg.num_train_steps = 200                       # one edit...
    at_200 = konfig.resolve(cfg.schedules["lr"])    # ...and the schedule already knows

    print(f"  {'progress':>10s}  {'lr @ 1000 steps':>18s}  {'lr @ 200 steps':>16s}")
    for frac in (0.1, 0.5, 0.9):
        print(f"  {frac:>9.0%}  {float(at_1000(int(1000*frac))):>18.6f}"
              f"  {float(at_200(int(200*frac))):>16.6f}")
    print("\n  Without .ref the schedule would have frozen 1000 into itself, and a sweep over")
    print("  num_train_steps would have silently trained on the wrong decay curve.")
    return (f"lr at 90% of training: {float(at_1000(900)):.6f} (1000 steps)"
            f" vs {float(at_200(180)):.6f} (200 steps)")

config_references()

Configuration systems usually go wrong when one value is needed in several places, and Kauldron&#8217;s answer is cfg.ref. We point a warmup-cosine schedule&#8217;s decay_steps at cfg.ref.num_train_steps rather than 1000, then change num_train_steps to 200 and resolve the schedule again. The learning rate curve reshapes itself, because the config stored a reference rather than a copy of the value. Without that indirection the schedule would have frozen 1000 into itself, and a sweep over the number of training steps would have quietly trained every variant on the wrong decay curve, which is the kind of bug that produces a plausible number and no error.

Copy CodeCopiedUse a different Browser

@section("3. kontext: parts are wired by string, so they never import each other")
def kontext_keys():
    import dataclasses

    ctx = {
        "batch": {"image": np.zeros((4, 8, 8, 3)), "label": np.arange(4)},
        "preds": {"logits": np.ones((4, 10)), "aux": [{"pos": np.zeros(3)}]},
    }
    print("  a context is just nested data; a key path reaches into it:")
    for path in ["batch.image", "preds.logits", "preds.aux[0].pos"]:
        print(f"    {path:22s} -> {kontext.get_by_path(ctx, path).shape}")

    try:
        kontext.get_by_path(ctx, "batch.nope")
    except KeyError as e:
        print(f"    {'batch.nope':22s} -> KeyError: {str(e)[:96]}...")

    @dataclasses.dataclass(eq=True, frozen=True, kw_only=True)
    class MeanGap:
        preds: kontext.Key = kontext.REQUIRED       # these ARE the wiring
        targets: kontext.Key = kontext.REQUIRED

        def __call__(self, *, preds, targets):
            return float(abs(np.asarray(preds).mean() - np.asarray(targets).mean()))

    metric = MeanGap(preds="preds.logits", targets="batch.label")
    kwargs = kontext.resolve_from_keyed_obj(ctx, metric)
    print(f"\n  MeanGap declared preds={metric.preds!r}, targets={metric.targets!r}")
    print(f"  resolved to kwargs: {{{', '.join(f'{k}: {v.shape}' for k, v in kwargs.items())}}}")
    print(f"  value = {metric(**kwargs)}")
    print("\n  MeanGap never imported the model and the model never heard of MeanGap. Point the")
    print("  same metric at 'preds.aux[0].pos' and nothing but that string changes.")
    return f"MeanGap(preds='preds.logits', targets='batch.label') = {metric(**kwargs)}"

kontext_keys()

kontext is how Kauldron connects components that know nothing about each other. A context is ordinary nested data, and a key path such as batch.image or preds.aux[0].pos reaches into it, resolving dictionary keys, attributes and list indices alike, and raising a KeyError that lists what was actually available when it cannot. Any object can declare its inputs by annotating fields as kontext.Key, and resolve_from_keyed_obj then pulls exactly those paths out of the context and hands them over as keyword arguments. We build a small metric this way and point it at a model&#8217;s outputs: the metric never imports the model, the model never hears of the metric, and redirecting the metric at a different tensor is a change to one string.

Copy CodeCopiedUse a different Browser

@section("4. ktyping: named axes, checked at runtime, bound across arguments")
def shape_checking():
    @typechecked
    def project(features: Float["*b n c"], weights: Float["c d"]) -> Float["*b n d"]:
        return jax.numpy.einsum("...c,cd->...d", features, weights)

    out = project(jax.numpy.zeros((2, 16, 8)), jax.numpy.zeros((8, 32)))
    print(f"  project(f32[2 16 8], f32[8 32]) -> {out.shape}   c bound to 8, d bound to 32")

    print("\n  now break it: c is bound to 8 by the first argument, so 5 cannot also be c")
    try:
        project(jax.numpy.zeros((2, 16, 8)), jax.numpy.zeros((5, 32)))
    except Exception as e:
        print(textwrap.indent(str(e), "    "))
    print("\n  'Inferred Dims' is the part worth having: it reports what each axis name was already")
    print("  bound to, so a mismatch names the axis instead of printing two anonymous shapes.")
    return "mismatch named the axis: c already bound to 8, got 5"

shape_checking()

Kauldron&#8217;s typing module checks array shapes at runtime using named axes. We annotate a function with Float[&#8216;*b n c&#8217;] and Float[&#8216;c d&#8217;], and the decorator binds each axis name the first time it sees it, then enforces that binding everywhere else in the signature, including the return value. When we deliberately pass an incompatible second argument, the error does the thing that matters: alongside the actual shapes it prints an Inferred Dims block showing that c had already been bound to 8, so the failure names the axis that disagreed instead of leaving us to compare two anonymous tuples. On a model with several tensors in flight this is the difference between a one-line fix and a debugging session.

Copy CodeCopiedUse a different Browser

import dataclasses

@dataclasses.dataclass(eq=True, frozen=True, kw_only=True)
class LogCosh(kd.losses.Loss):
    """log(cosh(err)): quadratic near zero, linear in the tails. ~30 lines less than raw Flax."""

    preds: kontext.Key = kontext.REQUIRED
    targets: kontext.Key = kontext.REQUIRED

    @typechecked
    def get_values(self, preds: Float["*a"], targets: Float["*a"]) -> Float["*a"]:
        return jax.numpy.log(jax.numpy.cosh(preds - targets))

@dataclasses.dataclass(eq=True, frozen=True, kw_only=True)
class WithinTol(kd.metrics.Metric):
    """Fraction of predictions landing within `tol` of the target, over every batch seen."""

    preds: kontext.Key = kontext.REQUIRED
    targets: kontext.Key = kontext.REQUIRED
    tol: float = 0.25

    @flax.struct.dataclass
    class State(kd.metrics.AutoState):
        # sum_field() marks a value that is ADDED when two states merge. Keeping the numerator
        # and the denominator apart is what makes the pooled result exact.
        n_hit: Float[""] = kd.metrics.sum_field(default=0.0)
        n_total: Float[""] = kd.metrics.sum_field(default=0.0)

        def compute(self) -> Float[""]:
            # Return a jax scalar, like the built-in states do: the metric writer that
            # `trainer.train()` logs through does not accept a bare numpy scalar.
            total = jax.numpy.maximum(jax.numpy.asarray(self.n_total), 1.0)
            return jax.numpy.asarray(self.n_hit) / total

    @typechecked
    def get_state(self, preds: Float["*a"], targets: Float["*a"]) -> "WithinTol.State":
        hit = (jax.numpy.abs(preds - targets) < self.tol).astype("float32")
        return self.State(n_hit=hit.sum(), n_total=jax.numpy.asarray(hit.size, "float32"))

@section("5. A custom loss and a custom metric, in the shape Kauldron expects")
def custom_loss_and_metric():
    rng = np.random.default_rng(0)
    p = jax.numpy.asarray(rng.normal(size=(8, 4)).astype("float32"))
    t = jax.numpy.asarray(rng.normal(size=(8, 4)).astype("float32"))

    loss = LogCosh(preds="preds.y", targets="batch.y")
    print(f"  {'LogCosh(preds, targets)':34s} {float(loss(preds=p, targets=t)):.6f}")
    print(f"  {'same loss, weight=0.5':34s} "
          f"{float(LogCosh(preds='a', targets='b', weight=0.5)(preds=p, targets=t)):.6f}   <- exactly half")
    print(f"  {'builtin kd.losses.L2':34s} {float(kd.losses.L2(preds='a', targets='b')(preds=p, targets=t)):.6f}")

    print("\n  A metric is not a number, it is a State that merges. Watch why that matters when")
    print("  the last batch of an epoch is smaller than the rest:")
    metric = WithinTol(preds="preds.y", targets="batch.y", tol=0.5)
    big = metric.get_state(preds=p[:6], targets=t[:6])
    small = metric.get_state(preds=p[6:], targets=t[6:])
    merged = big.merge(small)
    for label, st in [("batch of 6 rows", big), ("batch of 2 rows", small), ("big.merge(small)", merged)]:
        print(f"    {label:22s} {float(st.n_hit):>4.0f} / {float(st.n_total):>3.0f}  = {float(st.compute()):.4f}")
    naive = (float(big.compute()) + float(small.compute())) / 2
    print(f"    {'mean of the two rates':22s} {'':>4s}   {'':>3s}  = {naive:.4f}   <- wrong, and quietly so")
    print("\n  sum_field() adds numerator and denominator separately, so the pooled value is exact")
    print("  however the batches were sized. The same mechanism aggregates a metric across devices:")
    print("  merge is associative, so the order the states arrive in never changes the answer.")
    print("\n  Subclass, annotate the keys, implement one method. The loss never sees a batch dict")
    print("  and the metric never sees the model; the keys deliver exactly what was asked for.")
    return (f"merged {float(merged.n_hit):.0f}/{float(merged.n_total):.0f} = {float(merged.compute()):.4f}"
            f" vs {naive:.4f} from averaging the rates")

custom_loss_and_metric()

We write a custom loss and a custom metric in the exact shape Kauldron expects, which is a frozen dataclass with kontext.Key fields and one method. The loss implements get_values and returns a per-element array; the framework handles reduction and the weight argument, which we confirm by checking that weight=0.5 halves the result exactly. The metric is more interesting, because a Kauldron metric does not return a number but a State that merges. We build ours on AutoState with two sum_field entries, a numerator and a denominator, and then merge a six-row batch with a two-row batch. The pooled result is exact, while the average of the two per-batch rates is visibly wrong, which is precisely what would happen on the ragged last batch of an epoch, and since merge is associative the same mechanism aggregates a metric across devices without caring what order the results arrive in.

Copy CodeCopiedUse a different Browser

SEED_W = np.random.default_rng(7).normal(size=(16, 1)).astype("float32")

def make_loader(split: str):
    """A dataset is any callable returning an array tree. No download, no tf.data, no TFDS."""

    def load():
        rng = np.random.default_rng(0 if split == "train" else 1)
        n = 512 if split == "train" else 128
        x = rng.normal(size=(n, 16)).astype("float32")
        y = (x @ SEED_W + 0.1 * rng.normal(size=(n, 1))).astype("float32")
        return {"x": x, "y": y}

    return load

class MLP(nn.Module):
    inputs: kontext.Key = kontext.REQUIRED          # the model declares where its input comes from
    hidden: int = 32

    @nn.compact
    def __call__(self, inputs: Float["*b f"]) -> dict[str, Float["*b 1"]]:
        h = nn.relu(nn.Dense(self.hidden, name="enc")(inputs))
        return {"y": nn.Dense(1, name="out")(h)}

@section("6. A real Trainer on synthetic data, and a look inside the model")
def train_for_real():
    train_ds = kd.data.InMemoryPipeline(
        loader=make_loader("train"), batch_size=32, shuffle=True, num_epochs=None, seed=0)
    print(f"  element_spec: {kd.inspect.json_spec_like(train_ds.element_spec)}")
    print("\n  batch statistics straight from kd.inspect:")
    print(textwrap.indent(str(kd.inspect.get_batch_stats(next(iter(train_ds)))), "    "))

    trainer = kd.train.Trainer(
        seed=0,
        workdir="/tmp/kauldron_tutorial",
        train_ds=train_ds,
        model=MLP(inputs="batch.x"),
        num_train_steps=300,
        train_losses={"logcosh": LogCosh(preds="preds.y", targets="batch.y")},
        train_metrics={
            "within_tol": WithinTol(preds="preds.y", targets="batch.y"),
            "enc_norm": kd.metrics.Norm(tensor="interms.enc.__call__[0]"),   # an INNER layer
        },
        optimizer=optax.adam(learning_rate=1e-2),
    )

    it = iter(trainer.train_ds)
    state = trainer.trainstep.init(trainer.train_ds.element_spec)
    print(f"\n  params: {jax.tree.map(lambda x: tuple(x.shape), state.params)}")
    print(f"\n  {'step':>5s} {'logcosh':>10s} {'within .25':>11s} {'enc_norm':>10s}")
    for step in range(1, 301):
        # aux is opt-in: the step skips building it unless you ask, because it costs device time.
        state, aux = trainer.trainstep.step(state, next(it), return_losses=True, return_metrics=True)
        if step in (1, 25, 50, 100, 200, 300):
            losses = {k: float(v.compute()) for k, v in aux.loss_states.items()}
            metrics = {k: float(v.compute()) for k, v in aux.metric_states.items()}
            first_loss = losses["logcosh"] if step == 1 else first_loss
            final_loss = losses["logcosh"]
            print(f"  {step:>5d} {losses['logcosh']:>10.4f} {metrics['within_tol']:>11.4f}"
                  f" {metrics['enc_norm']:>10.4f}")

    print("\n  enc_norm was never returned by the model. 'interms.enc.__call__[0]' reaches into the")
    print("  Dense layer named 'enc' through Flax's captured intermediates, so monitoring an inner")
    print("  activation costs one string in the config and zero edits to MLP.")
    return f"logcosh {first_loss:.4f} -> {final_loss:.4f} over 300 CPU steps"

train_for_real()

Now we train. A Kauldron dataset is any callable returning a tree of arrays, so kd.data.InMemoryPipeline turns our synthetic regression data into a real pipeline with batching and shuffling and nothing to download. We assemble a Trainer from a model, that pipeline, our custom loss, our custom metric and an Optax optimizer, and drive its train step directly so we can print a loss curve: the loss falls from 1.51 to 0.005 over three hundred steps in about a second of CPU time. Two details are worth keeping. The train step does not build its auxiliary outputs unless we ask with return_losses and return_metrics, because computing them costs device time. And the enc_norm column is read from interms.enc.__call__[0], a key path into the intermediate output of the Dense layer named enc, so monitoring an inner activation costs one string in the config and no edit at all to the model.

Copy CodeCopiedUse a different Browser

@section("7. A sweep is a for-loop over config overrides")
def sweep():
    with konfig.imports():
        import optax as coptax
        from kauldron import kd as ckd
    with konfig.imports(lazy=True):
        # Classes defined in a notebook live in __main__, which cannot be fake-imported eagerly.
        from __main__ import MLP as CfgMLP
        from __main__ import make_loader as cfg_make_loader
        from __main__ import LogCosh as CfgLogCosh

    def base_config():
        cfg = ckd.train.Trainer()
        cfg.seed = 0
        cfg.workdir = "/tmp/kauldron_sweep"
        cfg.train_ds = ckd.data.InMemoryPipeline(
            loader=cfg_make_loader("train"), batch_size=32, shuffle=True, num_epochs=None)
        cfg.model = CfgMLP(inputs="batch.x", hidden=32)
        cfg.num_train_steps = 200
        cfg.train_losses = {"logcosh": CfgLogCosh(preds="preds.y", targets="batch.y")}
        cfg.optimizer = coptax.adam(learning_rate=1e-2)
        return cfg

    print(f"  cfg.model     = {base_config().model}")
    print(f"  cfg.optimizer = {base_config().optimizer}")
    print("\n  A bare lazy-imported name is a reference, not a call:")
    print(f"    CfgMLP(inputs=...)  -> {{'__qualname__': '__main__.MLP', ...}}   (built when resolved)")
    print(f"    cfg_make_loader     -> {dict(cfg_make_loader)}   (handed over as-is)")

    print(f"\n  {'override':34s} {'final logcosh':>14s}")
    results = {}
    for label, apply_override in [
        ("(baseline)", lambda c: None),
        ("cfg.model.hidden = 4", lambda c: setattr(c.model, "hidden", 4)),
        ("cfg.model.hidden = 128", lambda c: setattr(c.model, "hidden", 128)),
        ("cfg.optimizer.learning_rate = 0.1", lambda c: setattr(c.optimizer, "learning_rate", 0.1)),
        ("cfg.optimizer = optax.sgd(0.05)", lambda c: setattr(c, "optimizer", coptax.sgd(0.05))),
    ]:
        cfg = base_config()
        apply_override(cfg)
        trainer = konfig.resolve(cfg)               # ConfigDict -> a real, frozen Trainer
        it = iter(trainer.train_ds)
        state = trainer.trainstep.init(trainer.train_ds.element_spec)
        for _ in range(200):
            state, aux = trainer.trainstep.step(state, next(it), return_losses=True)
        results[label] = float(aux.loss_states["logcosh"].compute())
        print(f"  {label:34s} {results[label]:>14.4f}")

    print("\n  Five experiments, five one-line edits, and not one character of MLP, LogCosh or the")
    print("  training loop changed. On the command line the same overrides are")
    print("  --cfg.model.hidden=128, which is why a Kauldron sweep is a list of these strings.")
    return (f"best {min(results.values()):.4f} ({min(results, key=results.get)}),"
            f" worst {max(results.values()):.4f} ({max(results, key=results.get)})")

sweep()

This step is the argument for the whole design. We write the experiment once as a config, then run five variants that differ by exactly one line each: two model widths, two optimizer settings, and a wholesale swap of Adam for SGD. Every variant resolves into a fresh Trainer and trains for two hundred real steps, and not one character of the model, the loss or the training loop changes between them. Two konfig details make this work in a notebook. Classes defined in a notebook live in __main__, which cannot be fake-imported eagerly, so we use konfig.imports(lazy=True) for them. And a bare lazy-imported name resolves to the object itself rather than calling it, which is how the loader function is handed to the pipeline intact. On the command line these same overrides are written &#8211;cfg.model.hidden=128, which is why a Kauldron sweep is nothing more than a list of such strings.

Copy CodeCopiedUse a different Browser

@section("8. The guardrail: configs hold configs, never resolved objects")
def guardrails():
    with konfig.imports():
        from kauldron import kd as ckd

    cfg = ckd.train.Trainer()
    print("  Assigning a REAL flax module into a config is refused on the spot:")
    try:
        cfg.model = MLP(inputs="batch.x", hidden=8)
    except ValueError as e:
        print(textwrap.indent(str(e)[:420], "    "))

    print("\n  Why this matters: a half-resolved config cannot be serialized, diffed or overridden")
    print("  from the command line, so konfig refuses to let one exist rather than failing later.")

    print("\n  The same discipline shows up in sub-objects, which default to root-config references:")
    print(f"    kd.data.InMemoryPipeline(...).seed   default -> _FakeRootCfg('cfg.seed')")
    print(f"    kd.evals.Evaluator(...).ds           default -> _FakeRootCfg('cfg.eval_ds')")
    print("  Inside a Trainer those are filled from the root. Built standalone they are not, which")
    print("  is why step 6 passed seed=0 to the pipeline explicitly.")
    return "ConfigDict refused a resolved flax module at assignment"

guardrails()

Kauldron refuses to let a config hold a resolved object, and the refusal is immediate rather than deferred. Assigning a real Flax module into a ConfigDict raises on the spot with a message that suggests the two fixes, wrapping the import in konfig.imports() or using mock_modules in a notebook. A half-resolved config cannot be serialized, diffed, or overridden from the command line, so the system rules out the state entirely instead of failing later in a way that is hard to trace. The same discipline explains something we met in step 6: sub-objects such as pipelines and evaluators default their seed and dataset fields to references into the root config, which are filled in when the object is built inside a Trainer and are not when it is built standalone, which is why we passed the pipeline an explicit seed.

Copy CodeCopiedUse a different Browser

@section("9. Evaluation and checkpointing, and picking up where you left off")
def eval_and_checkpoint():
    import pathlib
    import shutil

    workdir = "/tmp/kauldron_resume"
    shutil.rmtree(workdir, ignore_errors=True)      # start from a clean slate for the demo

    def build(num_steps):
        return kd.train.Trainer(
            seed=0,
            workdir=workdir,
            train_ds=kd.data.InMemoryPipeline(
                loader=make_loader("train"), batch_size=32, shuffle=True, num_epochs=None, seed=0),
            model=MLP(inputs="batch.x"),
            num_train_steps=num_steps,
            log_metrics_every=100,
            train_losses={"logcosh": LogCosh(preds="preds.y", targets="batch.y")},
            train_metrics={"within_tol": WithinTol(preds="preds.y", targets="batch.y")},
            optimizer=optax.adam(learning_rate=1e-2),
            checkpointer=kd.ckpts.Checkpointer(save_interval_steps=100),
            evals={
                "eval": kd.evals.Evaluator(
                    run=kd.evals.EveryNSteps(100),
                    ds=kd.data.InMemoryPipeline(
                        loader=make_loader("eval"), batch_size=32, shuffle=False,
                        num_epochs=1, seed=0),
                    num_batches=4,
                )
            },
        )

    state, _ = build(200).train()
    print(f"  first run finished at step {int(state.step)}")
    saved = sorted(p.name for p in pathlib.Path(workdir).glob("checkpoints/ckpt_*"))
    print(f"  checkpoints on disk: {saved}")

    print("\n  Now build the same Trainer again, on the same workdir, asking for more steps:")
    state2, _ = build(300).train()
    print(f"  second run finished at step {int(state2.step)}")
    print("  The progress bar above started at 200, not 0: train() found the checkpoint and")
    print("  resumed, which is also what happens when a preemptible job is restarted.")
    print("\n  The evaluator ran on its own dataset every 100 steps. It inherited the model, the")
    print("  losses and the metrics from the root config, so declaring it took four lines.")
    return f"trained, evaluated, checkpointed and resumed at step {int(state2.step)}"

eval_and_checkpoint()

We close the loop with the parts that turn a training script into a job. An evaluator is declared in four lines, because it inherits the model, the losses and the metrics from the root config and only needs its own dataset and a schedule saying how often to run. A checkpointer writes state at a fixed step interval. Then we build the same Trainer a second time against the same working directory, asking for more steps, and the progress bar starts at 200 rather than 0: the run found its checkpoint and resumed. That is the same path taken when a preemptible job is restarted, and it is worth seeing once in a notebook where the whole thing takes a second, rather than discovering it for the first time on a cluster.

Copy CodeCopiedUse a different Browser

banner("SUMMARY")
for name, res in RESULTS.items():
    print(f"  {name:<72s}  {res}")
print("""
Where to go next
 - Read the two files that carry the ideas: kauldron/konfig/ (the config system, usable in any
   project with `from kauldron import konfig`) and kauldron/kontext/ (the key system). Both are
   self-contained and have no dependency on the rest of Kauldron.
 - Swap the synthetic pipeline for a real one: kd.data supports TFDS, Grain and PyGrain sources,
   plus transforms (Resize, Rearrange, ValueRange, Elements) that are themselves config entries.
 - Start from a working config: github.com/google-research/kauldron/tree/main/examples
 - Run it as a script: `python -m kauldron.main --cfg=config.py --cfg.model.hidden=128`, which is
   the same override used in step 7, typed on the command line instead.
 - Docs: kauldron.readthedocs.io  (konfig, kontext, data, eval, sharding, checkpoints)
""")

The summary prints the one-line result each section returned, then points at where to go next: the two self-contained modules worth reading on their own, the real data pipelines that replace our synthetic one, the example configs in the repository, and the command line that turns the sweep from step 7 into flags.

In conclusion, we treated Kauldron&#8217;s two claims as things to test rather than repeat, and both held up for an easy-to-state reason. Modularity here is not an abstraction layer but the absence of one: a config is a dictionary describing a Python call, wiring is a string naming a path through data, and neither optax nor our own model needed a single line of Kauldron-aware code to participate. Research velocity follows from that, and we saw it concretely in the sweep, where five experiments cost five edited lines, and in the shape checker, which names the axis that disagreed rather than printing two shapes and leaving us to work it out. The parts we did not need, TensorFlow datasets, Grain, sharding and XManager, sat entirely out of the way while a Trainer ran on synthetic data on a CPU. What we would carry into real work is smaller than the library: keep configuration as data, wire components by path rather than by import, and make metrics states that merge, since all three are useful even in a codebase that never adopts Kauldron itself.

Check out the FULL CODES here. All credit goes to the researcher of this project. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post A Coding Guide to Google Research&#8217;s Kauldron: Configs That Are Plain Data, Components Wired by String, and a JAX Trainer You Can Read End to End appeared first on MarkTechPost.