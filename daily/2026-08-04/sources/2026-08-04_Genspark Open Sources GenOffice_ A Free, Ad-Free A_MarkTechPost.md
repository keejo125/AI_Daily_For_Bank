---
publish_time: 1785815176
status: confirmed
category: 国际
is_model_related: false
digest: |
  Genspark 以 Apache 2.0 许可证开源了 GenOffice，一款 AI 原生的免费办公套件，支持 macOS 和 Windows 平台，涵盖文档、表格、幻灯片和 PDF 功能。
  
  GenOffice 将 AI 能力深度嵌入办公流程，用户可通过自然语言指令完成文档撰写、数据分析、演示生成等任务。与微软 Office、Google Workspace 等传统套件相比，GenOffice 完全免费且无广告，定位为 AI 时代的轻量级办公替代方案。
---

# Genspark 开源 AI 原生办公套件 GenOffice，免费替代 Office

> 原文链接：https://www.marktechpost.com/2026/08/03/genspark-open-sources-genoffice-a-free-ad-free-ai-office-suite-for-macos-and-windows-with-docs-sheets-slides-pdf/
> 来源：MarkTechPost

Genspark has released GenOffice as open source under the Apache License 2.0. The repository describes it as an AI-native office suite for macOS and Windows: a word processor, a spreadsheet, a presentation editor and a PDF tool. The implementation is five Electron apps sharing one engine layer, built around AI editing as a first-class workflow rather than a bolted-on chat box. Signed installers ship for macOS (Apple Silicon) and Windows (x64), currently at version 0.4.110. GenOffice is free for everyone, ad-free. All the editing tools you&#8217;d expect, no strings attached.

The team&#8217;s X post is blunt about scope: one engineer, one week, roughly $10,000 in tokens for the Alpha. The product page says free and ad-free, with AI features consuming Genspark credits. Feedback runs through a GenOffice group chat on GenTeam, with 1,000+ credits offered to active contributors.

Is it deployable

Yes, with conditions. Binaries install today on Apple Silicon Macs and Windows x64, and the source builds with Node 20+, npm 10+ and a Rust toolchain for the Sheets sidecar. But this is labeled an Alpha, and the AI path requires a Genspark account, since model calls are proxied service-side.

That maps cleanly to specific buyers. Startups and SMBs are the natural first tier: no license fees, no watermarks, and full .docx/.xlsx/.pptx fidelity. Mid-market teams can fork it, since Apache-2.0 permits commercial modification — although the ee/ directory is reserved for future enterprise modules under a separate GenOffice Enterprise License, and the GenOffice and Genspark names are Mainfunc, Inc. trademarks that forks may not reuse. Regulated enterprises should wait: alpha status plus a cloud-routed AI path means procurement and DPIA work first.

The technical core: byte-preserving round trips

GenOffice archives the original .docx by hash and never touches it. docx-engine parses the top-level elements of word/document.xml into a block tree, where each block is anchored by a docxIndex plus the original XML slice. Editing happens in a TipTap streaming editor with dirty tracking. On save, only dirty blocks are converted to OOXML fragments — referencing existing styles only — and spliced back into the original document.xml. Untouched blocks keep their original bytes, and every other zip entry is copied verbatim.

The stated payoff is that opening and saving never breaks layout in Word. The paginated view reproduces the original line metrics, and tracked changes, comments, styles, equations and ink are supported. Sheets and Slides follow the same philosophy: narrow patches over a source-of-truth file.

What sits under each app

Sheets builds its UI on the open-source Univer core (Apache-2.0) with a large layer of in-house extensions. XLSX import and export run through an in-house Rust sidecar using calamine and IronCalc. Charts are rendered in-house with Konva, alongside pivot tables, slicers, conditional formatting and formula tracing.

Slides uses an in-house pptx parse, render and edit engine covering masters, charts, cropping, ink and text shaping via HarfBuzz metrics. PDF is built on pdf.js and pdf-lib, adding annotations, forms, outlines, stamps, signatures, page operations and print. Shell provides the home screen, tabbed hosting and auto-update.

Engine packages are pure TypeScript, unit-tested, with no Electron dependency: docx-engine, pptx-engine, pptx-render, file-parse, agent-core, ai-provider, ai-search. Docs gets block-granular AI editing with snapshots and diffs; the other apps get a tool-calling agent over document state.

&

Security posture

SECURITY.md section is unusually detailed for an alpha. Every document window runs with contextIsolation: true, nodeIntegration: false and sandbox: true. IPC payloads are schema-checked in the main process, with Sheets using zod end to end. External links pass through a single safeExternalUrl gate enforcing an http/https allowlist; file:, javascript: and custom schemes are rejected.

Two AI threat models are documented. Slides layout scripts are parsed with Acorn and evaluated by a constrained AST interpreter — never eval, Function, a VM context or a worker — with no ambient globals, network, IPC bridge or timers, and statement and call-depth limits. Separately, AI-generated HTML in the pptx export pipeline is rendered in a hidden BrowserWindow treated as hostile: no preload, no IPC surface, driven only through executeJavaScript under a watchdog timeout.

Key Takeaways

GenOffice is Apache-2.0, ships signed macOS and Windows installers, and is explicitly an Alpha.

Docs preserves untouched .docx bytes by patching only dirty paragraphs into the original XML.

Sheets pairs the Univer core with a Rust xlsx sidecar (calamine + IronCalc); Slides and the docx engine are in-house.

AI runs through a signed-in Genspark account and consumes credits; no local model key by default.

Security docs cover full Electron renderer lockdown plus two explicit AI-content threat models.

Check out the Repo and Download it here. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Genspark Open Sources GenOffice: A Free, Ad-Free AI Office Suite for macOS and Windows with Docs, Sheets, Slides, PDF appeared first on MarkTechPost.