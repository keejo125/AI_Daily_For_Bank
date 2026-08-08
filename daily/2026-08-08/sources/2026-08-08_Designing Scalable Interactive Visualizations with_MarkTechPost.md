---
publish_time: 1786182138
status: pending
---

# Designing Scalable Interactive Visualizations with Reflex XY: Composition, Million-Point Rendering, Streaming, Custom Marks, and Export

> 原文链接：https://www.marktechpost.com/2026/08/08/designing-scalable-interactive-visualizations-with-reflex-xy-composition-million-point-rendering-streaming-custom-marks-and-export/
> 来源：MarkTechPost

In this tutorial, we explore the advanced visualization capabilities of the XY Python library by building interactive, scalable, and extensible charts. We begin with XY’s composition model, where we combine multiple marks, dual axes, annotations, tooltips, legends, themes, and interactive controls within a single chart declaration. We then work with Pandas DataFrames, faceted layouts, linked viewports, and million-point datasets that automatically switch to density-based rendering for efficient exploration. We also connect browser interactions back to Python through selections and callbacks, update charts dynamically through streaming, customize visual components with DOM slots and CSS, and extend the library with a reusable custom trendline mark. Also, we use the Matplotlib-compatible interface and export our visualizations as standalone HTML, SVG, and PNG files.

Copy CodeCopiedUse a different Browser

import subprocess, sys, os
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "xy"], check=True)
WIDGETS_OK = True
try:
   from google.colab import output as _colab_output
   _colab_output.enable_custom_widget_manager()
except Exception:
   WIDGETS_OK = False
import numpy as np
import pandas as pd
import xy
from IPython.display import display, HTML
print("xy", xy.__version__, "| live widgets:", WIDGETS_OK)
def render(chart, note=""):
   if note:
       display(HTML(f"<h3 style='font:600 15px system-ui;margin:18px 0 6px'>{note}</h3>"))
   try:
       display(chart)
   except Exception:
       display(HTML(chart.to_html()))
   return chart
rng = np.random.default_rng(7)
days    = np.arange(180)
trend   = 200 + 0.9 * days + 18 * np.sin(days / 9.0)
revenue = trend + rng.normal(0, 12, days.size)
sigma   = 10 + 6 * np.abs(np.sin(days / 15.0))
conv    = 0.06 + 0.02 * np.sin(days / 21.0) + rng.normal(0, 0.003, days.size)
peak    = int(np.argmax(revenue))
layered = xy.chart(
   xy.error_band(days, revenue - 1.96 * sigma, revenue + 1.96 * sigma,
                 name="95% band", color="#7c3aed", opacity=0.16),
   xy.line(days, revenue, name="Revenue", color="#7c3aed", width=2.5,
           curve="smooth"),
   xy.scatter(days[::12], revenue[::12], name="Weekly check", color="#7c3aed",
              size=7, stroke="#ffffff", stroke_width=1.5),
   xy.line(days, conv, name="Conversion", color="#f59e0b", width=2,
           dash="dashed", y_axis="y2"),
   xy.x_axis(label="Day", grid=True),
   xy.y_axis(label="Revenue (k)", grid=True, format=",.0f"),
   xy.y_axis(id="y2", label="Conversion", side="right", grid=False, format=".1%"),
   xy.x_band(120, 150, text="Campaign", color="#22c55e", opacity=0.10),
   xy.hline(float(revenue.mean()), text="mean", color="#94a3b8"),
   xy.callout(float(days[peak]), float(revenue[peak]), "peak", dx=-60, dy=-40),
   xy.legend(loc="upper left", ncols=2, toggle=True),
   xy.tooltip(title="Day", format={"y": ",.1f"}),
   xy.modebar(True),
   xy.theme(palette=["#7c3aed", "#f59e0b"], grid_color="#e6e6ef"),
   title="Layered composition · dual axes · annotations",
   width=900, height=440, crosshair=True,
)
render(layered, "1 · Composition model")

We install and initialize the XY library in Google Colab while enabling support for interactive widgets. We define a reusable rendering function that displays live charts and falls back to standalone HTML when widget support is unavailable. We then build a layered visualization with multiple marks, dual axes, annotations, tooltips, legends, themes, and interactive navigation controls.

Copy CodeCopiedUse a different Browser

n = 4000
df = pd.DataFrame({
   "x":      rng.normal(0, 1, n),
   "noise":  rng.normal(0, 1, n),
   "region": rng.choice(["North", "South", "East", "West"], n),
})
df["y"]   = 2.1 * df["x"] + df["noise"] * 0.9
df["mag"] = np.abs(df["y"])
render(xy.scatter_chart(
   xy.scatter("x", "y", color="mag", colormap="plasma",
              size=5, opacity=0.7, color_domain=(0, 6)),
   xy.colorbar(title="|y|"),
   xy.x_axis(label="x"), xy.y_axis(label="y"),
   data=df, title="Columns resolved by name", width=760, height=420,
), "2 · DataFrame-driven channels")
render(xy.facet_chart(
   xy.scatter("x", "y", color="#0ea5e9", size=4, opacity=0.6),
   by="region", data=df, cols=2,
   share_x=True, share_y=True, link=True, link_select=True,
   width=760, height=220, gap=12, title="Faceted by region",
), "3 · Facets with linked axes")
N = 1_500_000
r     = 6.0 * rng.beta(1.2, 3.0, N)
theta = 2.9 * np.log1p(r) + rng.integers(0, 4, N) * (np.pi / 2) + rng.normal(0, 0.05, N)
big = xy.scatter_chart(
   xy.scatter(r * np.cos(theta), r * np.sin(theta),
              color=np.exp(-r / 2.2), colormap="magma_r",
              density=True,
              size=2.5, opacity=0.85,
              zoom_size_factor=2.6, zoom_opacity=0.95),
   xy.colorbar(title="density"),
   title=f"{N:,} points · drag to pan, scroll to zoom",
   width=760, height=520, zoom=True, pan=True, wheel_zoom=True,
)
render(big, "4 · Million-point density surface")
mem = big.memory_report()
print(f"canonical f64 held in Python : {mem['canonical_bytes']/1e6:.1f} MB")
print(f"bytes sent for first paint   : {mem['transport_bytes_first_paint']/1e6:.2f} MB "
     f"({mem['transport_bytes_per_point']:.3f} B/point)")
print(f"compute backend              : {mem['backend']}")

We create a structured Pandas DataFrame and use column names directly as visualization channels. We generate a color-encoded scatter plot, divide the dataset into linked regional facets, and preserve shared axis behavior across panels. We also visualize 1.5 million points through XY’s density rendering system and inspect its memory usage and data-transfer efficiency.

Copy CodeCopiedUse a different Browser

sel = big.select_range(-1.0, 1.0, -1.0, 1.0)
sx, sy = sel.xy(0)
print(f"\nselect_range hit {len(sel):,} rows; x array {sx.shape}")
print("first rows:", sel.rows(limit=2))
print("pick(trace=1, index=10):", layered.pick(1, 10))
def on_select(selection):
   xs, ys = selection.xy(0)
   print(f"[callback] {len(selection):,} rows selected, mean y = {ys.mean():.3f}")
def on_view_change(payload):
   print("[callback] viewport:", payload)
render(xy.scatter_chart(
   xy.scatter("x", "y", color="#ef4444", size=5, opacity=0.7),
   data=df, select=True, on_select=on_select, on_view_change=on_view_change,
   title="Shift-drag a box → payload lands in Python",
   width=760, height=380,
), "5 · Selections routed back to the kernel")
stream = xy.line_chart(
   xy.line([0.0], [0.0], color="#10b981", width=2, name="live"),
   xy.x_axis(label="t"), xy.y_axis(label="value", domain=(-3, 3)),
   title="Streaming via chart.append()", width=760, height=320,
)
render(stream, "6 · Streaming")
import time
for k in range(1, 60):
   t = k / 3.0
   stream.append(0, [t], [float(np.sin(t) + rng.normal(0, 0.08))])
   time.sleep(0.03)

We select exact data points from the large visualization and retrieve their original row values directly from Python. We define callback functions that receive browser-side selections and viewport changes while keeping the underlying data inside the kernel. We also create a streaming line chart and continuously append new observations to update the visualization in real time.

Copy CodeCopiedUse a different Browser

print("\navailable slots:", ", ".join(sorted(xy.CHART_DOM_SLOTS)))
CSS = """
.xy-card {background:#fafaf9;border:1px solid #e7e5e4;border-radius:16px;padding:10px}
.xy-title{font:600 16px/1.2 ui-sans-serif;letter-spacing:-.01em;color:#1c1917}
.xy-tip  {border-radius:10px;background:#1c1917;color:#fafaf9}
"""
display(HTML(f"<style>{CSS}</style>"))
styled = xy.line_chart(
   xy.line(days, revenue, color="#111827", width=2,
           animation=xy.animation(duration=700,
                                  easing=xy.spring(stiffness=180, damping=22))),
   xy.x_axis(label="Day"), xy.y_axis(label="Revenue"),
   title="Slot-addressed styling",
   class_name="xy-card",
   class_names={"title": "xy-title", "tooltip": "xy-tip"},
   styles={"canvas": {"border-radius": "12px"}},
   width=760, height=360,
)
render(styled, "7 · CSS slots, tokens, spring animation")
def _fit(cols):
   x = np.asarray(cols["x"], float); y = np.asarray(cols["y"], float)
   b, a = np.polyfit(x, y, 1)
   order = np.argsort(x); xs = x[order]
   fit   = a + b * xs
   resid = float(np.std(y - (a + b * x)))
   return {"x": xs, "y": y[order], "fit": fit,
           "lo": fit - 1.96 * resid, "hi": fit + 1.96 * resid}
def _build(ctx):
   color = ctx.options.get("color", "#2563eb")
   c, nm = ctx.columns, (ctx.name or "trend")
   return [
       xy.error_band(c["x"], c["lo"], c["hi"], color=color, opacity=0.18, name=f"{nm} CI"),
       xy.line(c["x"], c["fit"], color=color, width=2.5, name=nm),
   ]
if "trendline" not in xy.registered_marks():
   xy.register_mark(xy.MarkPlugin(name="trendline", build=_build,
                                  columns=("x", "y"), calc=_fit,
                                  doc="OLS fit with a 95% band."))
render(xy.chart(
   xy.scatter("x", "y", color="#94a3b8", size=4, opacity=0.5, name="observations"),
   xy.mark("trendline", x="x", y="y", color="#e11d48", name="OLS"),
   xy.legend(loc="upper left"),
   data=df, title="Third-party mark kind", width=760, height=400,
), "8 · Custom mark plugin")

We customize chart components through stable DOM slots, CSS classes, inline styles, and spring-based animations. We define an ordinary least-squares calculation that produces a fitted trendline and a 95% confidence band from the supplied data. We then register this calculation as a reusable custom XY mark and combine it with built-in scatter, line, error-band, and legend components.

Copy CodeCopiedUse a different Browser

import xy.pyplot as plt
t = np.linspace(0, 10, 400)
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.plot(t, np.sin(t), "r--", label="sin")
ax.plot(t, np.cos(t), label="cos")
ax.set_xlabel("t"); ax.set_ylabel("amplitude"); ax.set_title("xy.pyplot compatibility")
ax.legend(); ax.grid(True, alpha=0.3)
plt.show()
os.makedirs("out", exist_ok=True)
layered.to_html("out/chart.html")
layered.to_svg("out/chart.svg")
layered.to_png("out/chart.png", scale=2)
for f in ("chart.html", "chart.svg", "chart.png"):
   print(f"out/{f}: {os.path.getsize('out/'+f)/1024:.0f} KB")
print("\n tutorial complete")

We use the xy.pyplot compatibility layer to create plots with familiar Matplotlib-style commands. We generate sine and cosine curves, configure labels, titles, legends, and grid settings, and display the resulting figure. We finally export the layered chart as standalone HTML, SVG, and high-resolution PNG files and verify the size of each generated artifact.

In conclusion, we built a comprehensive understanding of how XY supports modern interactive visualization workflows directly from Python. We created layered and faceted charts, analyzed large datasets efficiently, retrieved exact selected rows from the kernel, streamed new observations into live visualizations, and customized chart appearance through themes, animations, CSS classes, and stable DOM slots. We also demonstrated how we extend XY with our own statistical mark plugin and reuse familiar Matplotlib-style plotting commands through the xy.pyplot bridge. We finished with portable exports that allow us to share charts outside the notebook while preserving either interactivity or publication-ready graphical quality.

Check out the FULL CODES here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Designing Scalable Interactive Visualizations with Reflex XY: Composition, Million-Point Rendering, Streaming, Custom Marks, and Export appeared first on MarkTechPost.