---
publish_time: 1794638294
link: https://www.marktechpost.com/2026/11/13/vercel-ui-sdk-agent-ui-behaviors/
source: MarkTechPost
status: confirmed
category: 国际
is_model_related: false
digest: |
  Vercel Labs开源UI SDK（beta，Apache 2.0），面向编码智能体的无头界面行为库：不以成品组件交付，而是提供键盘导航、焦点、选择、弹层、拖拽等50+行为，由智能体组合成React、Vue、Svelte、Solid与Web Components组件。核心@ui-sdk/core定义原语，5个框架适配器渲染同一份行为；并通过createAgent桥接让智能体直接读写UI状态、免截图操作。Vercel自测：在一项设置任务上，接入桥接的Agent工具调用减少69%、耗时从41秒降至16秒、成本降56%。已发布6个npm包，最低要求React 19+。
---

# Vercel 发布 UI SDK：面向 AI 编码智能体的 50+ 界面行为

> 原文链接：https://www.marktechpost.com/2026/11/13/vercel-ui-sdk-agent-ui-behaviors/
> 来源：MarkTechPost

Vercel Labs has released UI SDK, an open-source beta library of interface behaviors built for coding agents. Vercel UI SDK is a headless library that ships behaviors, not finished components. Agents combine those behaviors into accessible components for React, Vue, Svelte, Solid and Web Components. You can check the deployment options and specs here through our GPULeaderboard.com chrome extension.

TL;DR

Size: 50+ behaviors, 51 component modules in the repo, 6 npm packages at 0.1.0-beta.1

Runs on: Any modern browser, no GPU. React 19+, Vue 3.5+, Svelte 5.33+, Solid 2 RC, or plain Web Components

Performance: In Vercel&#8217;s own test, an agent used 69% fewer tool calls on a settings task

Best: Task time fell 61%, from 41 s to 16 s, with the agent bridge (self-reported)

Worst: That benchmark covers 1 task and 3 runs, and beta APIs may still change

What is Vercel UI SDK?

UI SDK is a library of UI behaviors from Vercel Labs that agents assemble into components. The README lists keyboard navigation, focus, selection, dismissal, popups, drag and drop, and the ARIA they need. All of it lives in @ui-sdk/core. Thin adapters render it in each framework.

The project site explains the idea with a Select. You do not hand the agent a finished Select. You hand it a popup, a selection model and typeahead. Those same parts can produce an autocomplete, a combobox, or a component nobody has designed yet.

How does UI SDK work?

Components start as primitives defined with definePrimitive. A primitive declares state, an API and slots. Slots attach attributes, events and behaviors to DOM parts. The README example builds a search field with createFocusRecovery. Its Clear button appears only when there is text.

Each framework then renders the primitive with createParts. The README says the parts are the same in all 5 adapters. So 1 behavior definition can serve a React app and a Svelte app.

Which behaviors ship?

Behaviors shown on ui-sdk.dev include:

createRovingFocus: arrow keys move through a list with 1 Tab stop

createTypeahead: type a few letters to jump to an item

createPopup: opens next to its trigger and stays on screen

createSelection: select 1 or many, with Shift and Ctrl

createReorder, createResize, createViewport and createVirtualizer

The docs group behaviors into 10 categories, from Focus and Keys to Canvas. Prebuilt components include Select, Combobox, Date Picker, Menu, Tree and Color Picker.

How do agents learn it?

Setup is a prompt you paste into your agent. It installs the packages and adds a note to AGENTS.md. That note points the agent to the ui-sdk skill and to llms.txt inside the package docs. The skill installs with npx skills add vercel-labs/ui --skill ui-sdk. Pages without a build step can load web.js and web.css from ui-sdk.dev, per the skill listing.

&&

Can agents operate the UI directly?

Yes, the agent docs describe a bridge created with createAgent() before the page renders. agent.snapshot() lists components, their state and available actions. agent.act() runs an action, such as renaming a project with setValue. Apps can pass an allow callback to approve or refuse actions. Change callbacks receive source: "agent" and can cancel the change. Tools can also be registered with supported browsers through WebMCP.

UI SDK benchmark: agent bridge vs browser tools

Vercel compared its bridge against browser tools on 1 project-settings task. The agent renamed a project, updated members and notification settings, then saved. Both agents used Sonnet through Claude Code, with the same task and system prompt. Figures are medians of 3 runs.

MetricBrowser toolsUI SDK + bridgeChangeTool calls165-69%Text read (characters)39.8k6.8k-83%Time41 s16 s-61%Cost$0.073$0.032-56%

Treat these as directional. The sample is 1 task, and the browser-tools run used a different component library. Vercel does not name the Sonnet version.

Deployment and availability

All 6 packages are on npm at 0.1.0-beta.1, published November 12, 2026, under Apache-2.0. Install with npm install @ui-sdk/react @ui-sdk/core, swapping the adapter per framework. Peer requirements are strict: React 19+, Vue 3.5+, Svelte 5.33+ and Solid 2.0.0-rc.14+. An optional web.css file gives components a default look.

How does UI SDK compare with Radix, React Aria, Base UI and Ark UI?

MetricsUI SDKRadix PrimitivesReact Aria ComponentsBase UIArk UIModelBehaviors composed by agentsUnstyled componentsHooks and componentsUnstyled componentsComponents on Zag.js state machinesFrameworksReact, Vue, Svelte, Solid, Web ComponentsReactReactReactReact, Vue, Solid, SvelteLicenseApache-2.0MITApache-2.0MITMITLatest npm version0.1.0-beta.11.8.11.22.11.9.05.40.0React peer range19+16.8 to 1916.8 to 1917 to 1918+Agent skill and runtime bridgeYes (skill, llms.txt, createAgent, WebMCP)Not disclosedNot disclosedNot disclosedNot disclosed

Versions and peer ranges are from npm as of November 13, 2026. React Aria hooks and Ark UI&#8217;s Zag.js machines already separate behavior from markup. UI SDK&#8217;s difference is the agent layer: a skill, bundled llms.txt and a runtime bridge

Key Takeaways

50+ behaviors, 1 core, 5 framework adapters.

Agents compose components from behaviors, not templates.

createAgent lets agents act on UI state without screenshots.

Self-reported: 61% faster and 56% cheaper on 1 task.

Beta at 0.1.0-beta.1, with React 19 as the minimum.

Check out the GitHub repo, docs and npm package. You can check the deployment options and specs here through our GPULeaderboard.com chrome extension.

Also, feel free to follow us on Twitter and don’t forget to join our 150k+ML SubReddit and Subscribe to our Newsletter. Wait! are you on telegram? now you can join us on telegram as well.

Need to partner with us for promoting your GitHub Repo OR Hugging Face Page OR Product Release OR Webinar etc.? Connect with us

The post Vercel Releases UI SDK: 50+ UI Behaviors for AI Coding Agents appeared first on MarkTechPost.