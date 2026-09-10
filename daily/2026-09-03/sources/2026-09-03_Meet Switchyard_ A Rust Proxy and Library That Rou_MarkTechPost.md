---
publish_time: 1788372352
link: https://www.marktechpost.com/2026/09/02/nvidia-releases-switchyard-rust-proxy-llm-traffic-openai-anthropic-api-translation/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  英伟达开源Switchyard，一款Apache 2.0的Rust代理与库，用于LLM流量在OpenAI与Anthropic格式间路由与翻译。Coding Agent常因Claude Code用Anthropic API、Codex用OpenAI而受限，Switchyard解码为厂商中立类型、运行路由算法选后端、重编码请求，并记录运维指标、暴露可组合路由算法。目前为预-alpha评估版，不支持生产。
---

# 英伟达开源Switchyard：跨OpenAI与Anthropic API路由与翻译的Rust代理

> 原文链接：https://www.marktechpost.com/2026/09/02/nvidia-releases-switchyard-rust-proxy-llm-traffic-openai-anthropic-api-translation/
> 来源：MarkTechPost

Teams running coding agents hit the same wall. Claude Code speaks the Anthropic Messages API, Codex CLI speaks OpenAI, and the model a team actually wants to serve sits behind vLLM, NVIDIA NIM, or Ollama. Rewriting the agent is not an option, so the translation layer has to live somewhere else.

Switchyard is NVIDIA&#8217;s answer: a Rust proxy and library for LLM traffic that routes requests across providers, translates between OpenAI and Anthropic formats, records operational metrics, and exposes typed, composable routing algorithms. It is released under Apache 2.0 with documentation at docs.nvidia.com/nemo/switchyard.

Is it deployable? Yes, but for evaluation only. The binary installs from crates.io and the launcher from PyPI, and it self-hosts anywhere, but NVIDIA labels Switchyard pre-alpha and experimental, warns it is not for production use, and expects the API and algorithms to change significantly before v1.0.

What Switchyard does

Clients keep their native API. Switchyard decodes the inbound request into provider-neutral Rust types, runs a routing algorithm to pick a backend, re-encodes the request in that backend&#8217;s own wire format, calls it, and translates the response, including streaming events, back into the shape the client expects.

The server accepts three inbound formats: OpenAI Chat Completions, OpenAI Responses, and Anthropic Messages. Any of the three can address any route, and each configured LLM client selects one upstream format of its own. That decoupling is the point: the agent&#8217;s API and the backend&#8217;s API no longer have to match.

Three ways to run it

The launcher path targets coding agents. Install the published tool with uv tool install --python 3.12 "nemo-switchyard[cli]", then run switchyard launch claude, switchyard launch codex, or switchyard launch openclaw against a packaged deployment or your own TOML file.

The server path installs the standalone proxy with cargo install --locked switchyard-server, validates a config with --dry-run, and serves on a host and port you choose.

The library path uses switchyard-libsy, which embeds the routing algorithms in a Rust application without owning an HTTP stack. It never calls a model itself; the algorithm decides which target to use and hands every model call back to the caller.

Routing algorithms

A route is one client-visible model ID plus the algorithm behind it. The server supports:

passthrough sends every request to one target.

random splits traffic across targets using optional relative weights, with an optional seed that reproduces the selection sequence. This is the A/B and cost-experiment path.

llm_classifier calls a classifier target for a capability verdict, then routes to a weak or strong target. base_threshold is required; min_confidence, capability_elevated_floor, and session_affinity tune it, and anything the judge cannot decide falls through to the strong target. Setting mode = "escalation" runs every turn on the weak tier first and lets a judge decide whether to rerun it on the strong tier.

stage_router scores tool-result and agent-progress signals from recent turns to pick a capable or efficient target, avoiding an extra classifier call on most turns.

Strong, weak, capable, and efficient are roles inside a route, not fixed properties of a model. The same upstream model can serve different roles in different routes.

Observability

GET /metrics returns Prometheus text from the server&#8217;s process-wide OpenTelemetry provider. The families cover requests, errors, model-call latency, full-turn latency, prompt, completion, cached, cache-creation, and reasoning tokens, and upstream HTTP attempts by outcome and code. A tier label carries strong or weak for distinguishable classifier decisions, and classifier calls are excluded from those families.

The more interesting metric is switchyard_routing_overhead_ms, which reports the algorithm&#8217;s run time minus the call that served the request. Classifier calls are not subtracted, so an LLM-classifier route reports its classification time here while passthrough and random report the sub-millisecond cost of picking a target. Buckets start at 0.1 ms. Separately, --routing-log-file appends a JSON record per completed response, and GET /v1/routing/session-stats returns per-session call and token totals from that log.

Configuration

A TOML deployment has three layers: llm_clients define base URL, wire format, credential environment variable, and retry policy; targets bind one upstream model ID to a client; routes expose one client-visible model ID and its algorithm. Secrets never sit in the file, since api_key_env only names an environment variable. max_retries defaults to 2 and applies to transport failures, timeouts, HTTP 408/429, and 5xx responses.

Key Takeaways

Switchyard is an Apache-2.0 Rust proxy and library that routes and translates LLM traffic.

It bridges OpenAI Chat, OpenAI Responses, and Anthropic Messages in both directions, including streams.

Four route types ship: passthrough, random, LLM-classifier, and signal-driven stage router.

Prometheus metrics isolate routing overhead from model-call latency, per model and tier.

It is pre-alpha and explicitly not for production, so treat it as an evaluation tool.

Check out the GitHub Repo and Documentation. Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Meet Switchyard: A Rust Proxy and Library That Routes and Translates LLM Traffic Across OpenAI and Anthropic APIs appeared first on MarkTechPost.