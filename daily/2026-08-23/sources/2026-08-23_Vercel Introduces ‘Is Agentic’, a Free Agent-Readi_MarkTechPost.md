---
publish_time: 1787470634
status: confirmed
category: 国际
is_model_related: false
source: MarkTechPost
link: https://www.marktechpost.com/2026/08/23/vercel-introduces-is-agentic-a-free-agent-readiness-scoring-tool-that-audits-public-websites-using-oras-100-checks/
digest: |
  Vercel 发布免费公开工具 Is Agentic，用于给网站评分——衡量 AI 智能体能否发现、访问、理解并使用该网站。扫描与评分由时代实验室旗下的 agent 体验研究公司 Ora 完成，覆盖发现（20 分）、访问（30 分）、可用性（40 分）、支付（10 分）四层共 118 项检查，对标真实的智能体运行而非主观意见。工具提供网页、只读 API、CLI 与 MCP 服务器，均无需 API Key；CLI 可接入 CI 作为回归门禁，MCP 服务器暴露报告/方法论/开发者文档三类工具。Vercel 声明其非认证、安全审计或可访问性审查，仅视为带优先级的技术复审。
---

# Vercel 推出 Is Agentic：用 100+ 项检查审计网站智能体就绪度的免费评分工具

> 原文链接：https://www.marktechpost.com/2026/08/23/vercel-introduces-is-agentic-a-free-agent-readiness-scoring-tool-that-audits-public-websites-using-oras-100-checks/
> 来源：MarkTechPost

Vercel has released Is Agentic, a public tool that scores how readily AI agents can discover, access, understand, and use a website. Scans are run and scored by Ora, an agent-experience research company from era labs. Vercel operates the interface, report pages, storage, and the grouping that produces the displayed score.

Is it deployable?

Yes — at zero cost. Is Agentic is currently free, with no paid plans, subscription charges, or per-report fees. The public site, read-only API, CLI, and MCP server require no API key or billing account. Enter a URL in the browser, or run the CLI:

Copy CodeCopiedUse a different Browser

npx is-agentic <domain>
npx is-agentic <domain> --json

Which level of company: Any organization owning a public web surface. Seed-stage startups get a free baseline audit with no procurement. Mid-market SaaS teams can wire --json output into CI as a regression gate. Enterprises can benchmark documentation portals, developer sites, and commerce surfaces across business units.

Industries: Developer tools and SaaS, e-commerce and retail, travel and hospitality, fintech, marketplaces, healthcare provider directories, and media or documentation publishers. Anywhere an agent may shop, book, integrate, or cite on a user&#8217;s behalf.

Applications: Pre-launch agent-readiness audits. CI checks that fail builds when server-rendered content regresses. Competitive benchmarking against public scores. Validating an MCP server or OpenAPI surface is actually discoverable. Prioritizing technical fixes with copy-pasteable remediation prompts.

What Exactly it Measures

Ora&#8217;s methodology walks four layers an agent moves through. Discovery carries 20 points across 15 checks. Access carries 30 points across 41 checks. Usability carries 40 points across 56 checks. Payments carries 10 points across 6 checks. That totals 118 checks, matching Vercel&#8217;s &#8220;100+ checks&#8221; claim. Ora says the checklist is reverse-engineered from real agent runs, not authored by opinion.

Ora also publishes a letter scale: A+ at 95–100, A at 86–94, B at 70–85, C at 48–69, D at 28–47, and F at 0–27.

Vercel regroups those checks into its own displayed scoring model. Essential checks share an 80-point pool. Recommended checks share a 20-point pool. Emerging signals add a bonus capped at five points, and their absence never lowers a score. Not-applicable checks are excluded rather than counted as failures. Partial results receive proportional credit, and duplicated check IDs across MCP surfaces are averaged.

That applicability logic matters. Recommended checks activate only when scan evidence positively identifies an API, OAuth flow, GraphQL endpoint, MCP server, developer portal, or commerce surface. A marketing site is not penalized for omitting an interface it never claimed to offer.

Inside a report

Every finding ships with observed evidence and, where available, a concrete recommendation. A live API response shows the shape: score, score_label, scanned_at, eligible_checks, a score_breakdown with earned and available points per tier, and an issues array. Each issue carries id, name, details, recommendation, result, and tier.

Real check IDs include content-no-js, agent-friendly-404, markdown-negotiation-vary, json-ld, sitemap, trust-anchors, and metadata-completeness. The 404 check asks for a real HTTP 404 status rather than a 200 serving an app shell.

Reports also include an observed agent journey showing where one agent hit friction. Vercel keeps that run outside the numeric score, since one task cannot represent every agent. &#8220;Prompt to fix&#8221; converts actionable recommendations into an implementation brief for a coding agent.

Machine interfaces

Three read-only surfaces expose completed reports. The report API lives at /api/v1/report, rate-limited to 120 requests per client IP per 60-second window. Errors use RFC 9457 problem details with stable codes such as invalid_url, report_not_found, and rate_limit_exceeded. The OpenAPI description is the supported integration contract, discoverable through an RFC 9727 API catalog. Deprecations signal via RFC 9745 headers, with Sunset announced at least 90 days ahead.

The MCP server at https://is-agentic.com/mcp exposes is_agentic_get_report, is_agentic_get_methodology, and is_agentic_get_developer_docs over Streamable HTTP. Hosts supporting MCP Apps render an interactive score card. An official agent skill installs via npx skills add vercel-labs/is-agentic.

The site practices what it scores. Report pages render the score in the initial HTML response, serve a Markdown variant under Accept: text/markdown, and set Vary: Accept so shared caches never mix representations.

Key Takeaways

Is Agentic scores public sites on agent discovery, access, usability, and payments — free, with no API key.

Ora supplies 118 checks across four weighted layers; Vercel regroups them into Essential 80, Recommended 20, Bonus 5.

Not-applicable checks are excluded, so marketing sites are not penalized for missing APIs or commerce surfaces.

Reports ship as HTML, Markdown, JSON, CLI output, and MCP tools, all read-only and unauthenticated.

Vercel states it is not a certification, security audit, or accessibility review — treat it as a prioritized technical review.

The post Vercel Introduces &#8216;Is Agentic&#8217;, a Free Agent-Readiness Scoring Tool That Audits Public Websites Using Ora&#8217;s 100+ Checks appeared first on MarkTechPost.