---
publish_time: 1792021045
link: https://www.marktechpost.com/2026/10/14/datalab-omniparsebench-open-ocr-document-parsing-benchmark/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Datalab开源OmniParseBench，一个面向文档解析器的OCR评测基准：以16288项yes/no测试覆盖2937页、2343份文档、92种语言，帮工程师回答'哪款解析器适配我的文档'。基准以uv安装即可运行，Datalab自家解析器在榜单位列Gemini 3.8 Flash之后。
---

# Datalab 开源 OmniParseBench：面向文档解析器的 16288 项 Pass/Fail OCR 评测基准

> 原文链接：https://www.marktechpost.com/2026/10/14/datalab-omniparsebench-open-ocr-document-parsing-benchmark/
> 来源：MarkTechPost

Datalab has released OmniParseBench, an open OCR benchmark for document parsers. It scores parsers with 16,288 yes/no tests on 2,937 pages from 2,343 documents. The pages span 92 languages. The dataset and code are public. It helps engineers answer a sharper question than a leaderboard does: which parser handles documents like mine? Datalab sells a parser, and its own top setting, Datalab accurate, ranks second on the launch leaderboard, behind Gemini 3.8 Flash.

Is it deployable? Yes. OmniParseBench is an evaluation harness, not a model. It installs with uv pip install omni-parse-bench, needs Python 3.11+, and scores outputs offline with no API keys.

TL;DR

Size: 16,288 tests, 2,937 pages, 2,343 documents, 22 suites, 92 languages.

Runs on: any machine with Python 3.11+. Scoring needs no network. Vendor runs need each vendor&#8217;s API key.

Performance: the top 3 reported systems sit within 1.3 headline points.

Best: Gemini 3.8 Flash leads at 92.9; Datalab accurate follows at 92.7.*

Bottom line: every score is a share of pass/fail tests, sliceable by tag.

* used in building some tests

What is OmniParseBench?

OmniParseBench is a document-parsing benchmark from Datalab where every test is a yes/no question about 1 page. A parser&#8217;s score is the share of tests it passes. Datalab built it to be clear, auditable and explorable.

Why build another OCR benchmark?

Datalab names two problems with existing benchmarks. olmOCR-bench showed that pass/fail unit tests work. Datalab now calls it saturated. In its view, top systems are separated by output conventions and overfitting, not reading. Each olmOCR-bench test also sits in 1 bucket, set by its page&#8217;s source. A handwritten table gets averaged into whichever bucket its page landed in.

ParseBench from LlamaIndex splits parsing into 5 capabilities, each with its own metric. Datalab argues those scores share no unit, so they cannot be compared or combined cleanly.

How does OmniParseBench scoring work?

The final score is the mean of 3 family scores: text, tables and layout. Five test types feed those families:

present: a text, number or equation appears (text)

order: text A comes before text B (text)

repeat: a line appears exactly N times (text)

table_cell: a cell sits under given headings and beside given neighbors (tables)

layout_kind: the block holding a line is a heading, text or table (layout)

Numbers must match digit for digit, though 1,240 matches 1240. Equations are compared by what KaTeX renders, so \frac{a}{b} equals \dfrac{a}{b}. Each decision is pass, fail, unsupported or error. The last 2 are left out of every score. No model judges the outputs; the scorer is open code.

What do tags and derivations add?

A test checks one or more args, each of which is the content at one place on the page. Each arg carries tags on 5 axes: structure, rendering, role, script and language. Scripts use ISO 15924 codes; languages use ISO 639-3 codes. Tags never decide a verdict or the headline. They only select tests, so any slice gets its own score.

The table tag covers 6,767 tests on 1,000 pages from 875 documents. English covers 10,089 tests. Non-English languages cover 1,931 tests on 529 pages from 321 documents.

Every test also records its derivation, meaning how its answer was established. There are 10 derivations. They include publisher JATS XML, the PDF text layer, authored pages, olmOCR-bench tests, model panels and human review.

&&&

What are the OmniParseBench launch results?

ParserHeadlineTextTablesLayoutGemini 3.8 Flash*92.991.395.292.2Datalab accurate92.790.891.895.6Datalab balanced91.690.089.295.5Reducto90.885.491.295.8LlamaParse90.488.292.690.4Mistral OCR89.582.891.993.8Claude Sonnet 5.5*88.793.195.477.5GPT-5.6 Sol87.885.491.686.5Extend83.364.192.593.4Azure83.074.681.792.8Tesseractnone17.60.0unsupported

*Used in creating and verifying at least some tests, per Datalab.

Claude Sonnet 5.5 posts the top text (93.1) and tables (95.4) scores. Its layout score of 77.5 pulls its headline to 88.7. Reducto leads layout at 95.8. Datalab also plotted each headline against median latency and price per 1,000 pages. Latency was measured on 200 sampled pages, sent 8 at a time.

Datalab does not top its own benchmark. It flags the two models that helped build tests, and it tells readers to weigh the fact that it sells a parser. It commits to reporting OmniParseBench scores for future releases. Its advice: the best benchmark is your own documents.

How do you run OmniParseBench?

Copy CodeCopiedUse a different Browser

uv pip install omni-parse-bench                 # score(): no network, no API keys
uv pip install 'omni-parse-bench[harness]'      # + vendor adapters, to predict
uv pip install 'omni-parse-bench[benchmark]'    # + dataset access, to run the benchmark
opb benchmark --out runs/ --limit 5 --providers datalab openai/gpt-5.6-sol

Vendors need keys such as DATALAB_API_KEY or OPENROUTER_API_KEY. The CLI shows its plan and asks before calling any vendor. Runs are resumable. The query guide shows how to compare runs by tag, suite or test type.

OmniParseBench vs olmOCR-bench vs ParseBench vs OmniDocBench

FeatureOmniParseBencholmOCR-benchParseBenchOmniDocBenchMaintainerDatalabAi2LlamaIndexOpenDataLabScale16,288 tests, 2,937 pages, 2,343 docs7,010 tests, 1,403 PDFs169,011 rules, 2,078 pages, 1,211 docs1,651 PDF pagesLanguages92EnglishNot disclosed5 language typesScoring unitPass/fail test; headline = mean of 3 familiesPass/fail unit tests5 dimensions, each with its own metricOverall from text edit distance, table TEDS, formula CDMModel judgeNoneNot used for scoringNone by default (opt-in for charts)Not used for scoringContent tagsPer arg: structure, rendering, role, script, language7 source categories5 capability dimensionsPage, text and table attributesPer-test provenanceYes, derivation on every testExtraction method per categoryHuman-verified pagesNot per testLatency and costMedian s/page, $ per 1,000 pagesNot in dataset card¢ per page on leaderboardNot disclosedLicenseCode Apache 2.0; tests CC BY 4.0 with exceptions; page data licensed per sourceDataset ODC-BY 1.0Apache 2.0Code Apache 2.0; data research only

Key Takeaways

16,288 yes/no tests on 2,937 pages in 92 languages.

Headline = mean of text, tables and layout pass rates.

Tags slice results; they never change a verdict.

Datalab built it and ranks second: Gemini 3.8 Flash 92.9*, Datalab accurate 92.7.

Apache 2.0 code; scoring runs offline without API keys.

* used in building some tests

Check out the blog post, dataset and GitHub repo.

Thanks to the Datalab team for the resources behind this article. Datalab supported and sponsored this content.

The post Datalab Releases OmniParseBench: An Open OCR Benchmark With 16,288 Pass/Fail Tests to Audit OCR Parsers appeared first on MarkTechPost.