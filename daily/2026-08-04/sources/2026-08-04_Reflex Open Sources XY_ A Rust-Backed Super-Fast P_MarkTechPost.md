---
publish_time: 1785836740
status: confirmed
category: 其他
is_model_related: false
digest: |
  Reflex AI 以 Apache 2.0 许可证开源了 XY，一款基于 Rust 后端加速的 Python 图表库，支持交互式 2D 可视化，在百万级数据点场景下仍能保持流畅交互。该工具定位于科学计算和数据探索场景，为 Python 生态提供了高性能可视化选项。
---

# Reflex 开源高性能 Python 图表库 XY：Rust 后端驱动，亿级数据点流畅交互

> 原文链接：https://www.marktechpost.com/2026/08/04/reflex-open-sources-xy/
> 来源：MarkTechPost

Reflex AI has released XY, an Apache-2.0 Python charting library for interactive 2D visualization. Most Python charting stacks create one drawable object per row, so past a few hundred thousand points, render, hover, and zoom degrade. XY moves the work into a native Rust core, sends the browser typed binary buffers instead of JSON, and draws with WebGL2. In the terms of the benchmark, XY holds 0.071 s at 10,000 points and 0.081 s at 100 million. It ships as pip install xy and requires Python 3.11 or newer.

Is it deployable

XY is early alpha at version 0.0.1. It ships as pip install xy and requires Python 3.11 or newer.

That maps to a clear deployment envelope. Startups and mid-size data teams can adopt it now for internal analytics, notebooks, and shareable artifacts. Regulated enterprises should pilot it rather than put it on a customer-facing critical path. Fit is strongest where row counts are the actual bottleneck: quantitative finance (tick data), genomics and bioinformatics (Manhattan plots, allele-frequency scans), observability and telemetry, astronomy, and geospatial analytics. Here is how to install it in 1 line.

Copy CodeCopiedUse a different Browser

pip install xy

Explainer

How the representation ladder works

XY keeps canonical f64 columns in a ColumnStore in Python and picks a rendered representation per trace. Current defaults start M4 decimation above 10,000 rows for long ordered lines, and automatic scatter density above 200,000 points. Density grids default to 512×384 cells. The docs are explicit that these are pre-1.0 policy thresholds, not API guarantees.

Because exact values stay in Python, hover, selection, and pick() still resolve original rows when the active tier has an exact mapping. Zooming into a narrow window returns exact visible points for a padded aligned window, and nearby pans render from that cached window without another request. Reflex is careful not to overclaim here: density is natively binned and GPU-rendered, not an all-GPU ingest pipeline, and ingest, binning, and decimation still scale with source row count.

Performance

The benchmark drives every library through a real browser and stops the clock only when the canvas is verified correct and stable across 10 byte-identical frames. Measurements come from one Apple M5 Pro, one run per cell.

PointsXYMatplotlib (WebAgg)Plotly (scattergl)1M0.084 s0.357 s0.614 s10M0.083 s2.804 s3.367 s50M0.076 s13.385 s✕100M0.081 s✕✕

That is a stated 34× speedup at 10M and 177× at 50M. Peak Python-side memory at 10M is 0.32 GiB for XY against 0.84 GiB for Matplotlib and 1.86 GiB for Plotly. With density=False, XY still draws 100M exact markers in 1.343 s on 5.26 GiB. Reflex also reports rendering the full OpenStreetMap dataset — 10 billion points.

A 10-million-point interactive scatter exports to 258 KiB of HTML, versus a stated 259 MiB for the Plotly equivalent. The payload stays near 258 KiB from 1M through 100M rows.

API surface and integration

Charts are composed declaratively from marks, axes, legends, tooltips, and annotations. Fourteen chart families ship today, including scatter, line, area, histogram, box, violin, ECDF, heatmap, hexbin, and contour. Styling accepts CSS and Tailwind classes through stable DOM slots. For migration, import xy.pyplot as plt runs common Matplotlib pyplot code, though the compatibility guide notes not everything is supported. A separate reflex-xy adapter turns any chart into a Reflex component with no JavaScript or iframe.

Key Takeaways

XY holds ~0.08 s render time from 10k to 100M points by drawing screen-bounded representations, not per-row markers.

Rust core plus binary transport cuts a 10M-point interactive export to 258 KiB against Plotly&#8217;s 259 MiB.

Exact f64 columns stay in Python, so hover, selection, and zoom drilldown still return original rows.

Deployable today for notebooks, internal dashboards, and shareable HTML; version 0.0.1 alpha argues against critical paths.

Best fit is finance, genomics, telemetry, and astronomy, where sampling before plotting is the current default.

Check out the GitHub Repo and Technical details. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Reflex Open Sources XY: A Rust-Backed Super-Fast Python Charting Library That Keeps 100 Million Point Charts Interactive appeared first on MarkTechPost.