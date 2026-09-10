---
publish_time: 1785493973
status: confirmed
category: 国际
is_model_related: false
digest: |
  JetBrains Research开源了KotlinLLM，这是一个为Kotlin/JVM项目设计的IntelliJ IDEA插件，引入了"Smart Macros"语言特性，允许在运行时通过LLM生成Kotlin源代码并通过JDI（Java调试接口）进行热重载。
  
  其公共API设计精简：asLlm<F,T>(from, hint)将输入转换为类型化值，mockLlm<T>()生成接口的有状态实现。运行时循环中，插件扫描asLlm和mockLlm调用，在JDI下启动运行配置并注册断点。当生成逻辑不匹配运行时场景时，插件捕获运行时值和类型信息，LLM代理提交代码更新，编译后通过类重定义重试原始调用。
  
  在适配的Spring Petclinic项目评估中，18个asLlm调用点的24个应用场景全部完成，热重载成功率100%，编译/重定义仅增加约1%运行时开销。该工具需要IntelliJ IDEA 2025.2.x、JDK 21和OpenAI API密钥，以Apache 2.0许可发布。
  
  KotlinLLM定位为研究原型而非生产运行时，但其输出是可部署的——行为生成后，目标项目可独立编译运行而无需再次LLM请求。最适合拥有大量JVM/Kotlin代码库的金融科技和银行行业。
---

# JetBrains Open-Sources KotlinLLM: Smart Macros That Generate Kotlin Source Code at Runtime and Hot-Reload It Through JDI

> 原文链接：https://www.marktechpost.com/2026/07/31/jetbrains-research-open-sources-kotlinllm-intellij-plugin-kotlin-runtime-llm/
> 来源：MarkTechPost

JetBrains Research Open-Sources KotlinLLM. KotlinLLM is an IntelliJ IDEA plugin for Kotlin/JVM projects that adds a language feature called Smart macros. A Smart macro is a regular Kotlin function call whose body is generated Kotlin code. The public API is deliberately small. asLlm<F, T>(from, hint) converts an input of type F into a typed value T, such as a data class, enum, list, or primitive. mockLlm<T>() generates a stateful implementation of an interface T, whose behavior depends on which methods are called on it.

Copy CodeCopiedUse a different Browser

val issuesApiUrl: String = asLlm(repoInput, hint = "GitHub API URL: get all issues, including closed")
val issues: List<Issue> = asLlm(response, hint = "Return all beginner-friendly issues for this repository")

The runtime loop

When a project launches through the KotlinLLM run configuration, the plugin scans for asLlm and mockLlm calls, updates generated bootstrap/provider/parser/mock files, launches the run configuration under JDI, and registers breakpoints on generated regenerate hooks. If generated logic does not match a runtime scenario, execution reaches a hook. The plugin captures runtime values and type information from the suspended frame, the LLM agent submits a code update, and the plugin compiles it and redefines the loaded class before retrying the original call.

KotlinLLM targets Kotlin/JVM specifically because the runtime evolution loop depends on JVM class redefinition through JDI.

Explainer: how a Smart macro evolves

The embed below walks the macro API, animates the nine-step runtime loop, and models why covered scenarios stop costing inference calls. 

&&

Reported results

On an adapted Spring Petclinic Kotlin project with 18 asLlm call sites, 24 of 24 application scenarios completed after Smart macro evolution, with a 100% hot-reload success rate and compilation/redefinition adding roughly 1% of total runtime overhead. A synthetic &#8220;GitHub Beginner Issue Radar&#8221; parsed real issue data across 20 repositories and 30k+ issues, reaching about 0.89 recall on ground-truth beginner labels.

Setup requirements

The plugin requires IntelliJ IDEA 2025.2.x, JDK 21, and an OpenAI API key stored in the target project&#8217;s .kotlinllm file via Tools > KotlinLLM Settings. It is released under the Apache License 2.0, with runnable examples, the thesis write-up, and the KotlinConf 2026 talk recording in the repository.

Is it deployable?

Not as a production runtime, at least not yet. JetBrains labels KotlinLLM a research prototype, and it is described it as an experimental IntelliJ IDEA plugin. The plugin is experimental, but its output is deployable. Once behavior has been generated, the target project can compile and run that behavior without another LLM request for the same scenario. You ship plain Kotlin, not a model dependency.

Company level: best fit today is R&D groups, platform teams at mid-size to large Kotlin/JVM entities, and startups with tolerance for prototype tooling. Regulated enterprises should treat generated sources as reviewable code, which is exactly how KotlinLLM stores them.

Industries: fintech and banking (heavy JVM/Kotlin estates), developer tooling, e-commerce, logistics, and any team parsing messy third-party API payloads.

Applications: normalizing semi-structured API responses into typed values, building evolving test doubles, adapting to upstream schema drift, and classification over noisy text fields.

Key Takeaways

KotlinLLM is a JetBrains Research prototype, not a production runtime.

Smart macros generate Kotlin source that is committed, reviewed, and run without the plugin.

Covered scenarios trigger no further LLM call, so no added latency or cost.

Petclinic evaluation: 24/24 scenarios, 100% hot-reload, ~1% overhead.

Apache 2.0, Kotlin/JVM only, IntelliJ IDEA 2025.2.x plus JDK 21.

Sources: JetBrains Research blog, the kotlinllm-plugin README, and InfoWorld 

The post JetBrains Open-Sources KotlinLLM: Smart Macros That Generate Kotlin Source Code at Runtime and Hot-Reload It Through JDI appeared first on MarkTechPost.