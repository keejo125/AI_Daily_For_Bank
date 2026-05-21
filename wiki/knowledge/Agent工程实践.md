## Java微服务本地化改造：AI Coding的最后一公里

### 问题的本质：微服务架构天然不AI友好

Java微服务项目重度依赖HSF/TDDL/OSS/Diamond/MetaQ等云端基础设施。本地`mvn spring-boot:run`直接启动失败，AI写完代码没有任何办法验证自己写的东西能不能跑。经典循环：我把代码推到预发，等5分钟部署完成，手动触发一次调用，发现NPE，截图贴回给AI，AI改了两行，我再推预发，再等5分钟……三轮下来半小时过去了，改的只是一个参数注入顺序的问题。同样的模型、同样的Prompt，差距不在AI能力，在如何构建AI友好的工程环境。

**改造前工作流**：本地Vibe Coding → 推预发部署 → 人工验证 → 反馈给AI → AI继续改 → 再次推预发 → 再次人工验证……人在每个环节都是阻塞点。

### 三条改造原则

**1. 依赖倒置，接口先行**

上层逻辑依赖抽象接口，不依赖具体实现。云端和本地只是接口的不同实现。抽一个`StorageAdapter`接口，线上的OSS实现加一行`implements StorageAdapter`，本地新写一个`LocalStorageAdapter`用`java.nio.file`映射到本地路径。工厂类检测参数自动选择，切换运行环境就是换一个接口实现，上层代码完全不用改。

```
StorageAdapter (接口)
 ├── OssStorageAdapter (线上，走OSS SDK)
 └── LocalStorageAdapter (本地，走java.nio.file)

CommandExecutor (接口)
 ├── SandboxCommandExecutor (线上，调远程沙箱API)
 └── LocalCommandExecutor (本地，ProcessBuilder + bash -c)
```

**2. 零侵入，Profile隔离**

本地改造不能让线上代码路径多走一行额外的代码。Spring Profile隔离：本地专属Bean通过`@Profile("local")`装配，线上专属的通过`@Profile("!local")`守卫。`@Nullable`参数注入：可选依赖标`@Nullable`，不存在时Spring注入null。条件守卫：`localFsBasePath`不为空就走本地，`ossClient`不为空就走线上。最终效果：删掉所有本地相关代码后，线上行为完全不变。

**3. 工具AI化：CLI优先**

AI Agent的能力边界 = 它能调用的工具的边界。GUI对AI不可见，CLI才是AI能用的东西。通过`mw-cli`查询Diamond运行时配置、通过`mw hsf address`查询HSF服务地址。团队使用的运维工具是否有CLI入口？配置管理是否可通过命令行查询？是否有MCP Server或Skill将内部系统能力暴露给AI Agent？

**工具AI化优先级**：CLI直接可用（mw-cli、mvn、git、arthas）> MCP Server协议适配 > Skill/Tool自定义封装 > GUI不可用。

### 改造效果

| 对比项 | 改造前 | 改造后 |
|--------|--------|--------|
| 文件操作验证 | 推预发，通过OSS控制台查看 | 本地直接`ls`查看 |
| Bash执行验证 | 推预发，登录沙箱查看 | 本地Terminal直接看 |
| AI自主验证 | 做不到 | ReadFile → 验证WriteFile结果 |
| 单次迭代耗时 | 5-10分钟（含部署等待） | 秒级 |
| AI自主修复轮数 | 0（每轮都要人工介入） | 平均3-5轮后自行收敛 |

完整bug fix流程：改造前需要3-4轮人工推预发验证、总耗时30分钟以上；改造后AI在本地自主迭代，通常2分钟内收敛，人只需要最后review结果。

### 配套Harness工程

**CLAUDE.md**：给AI一张地图。项目根目录放一份，告诉AI这个项目是什么、怎么构建、怎么测试、本地环境怎么启动。100行以内，重点是让AI能快速定位该看哪些代码、该跑什么命令。

**验证脚本**：`scripts/verify-local.sh`让AI自己检查：编译→单元测试→本地启动检查→文件系统闭环检查。AI改完代码跑一次`bash scripts/verify-local.sh`，不需要人工介入就能知道本地环境是否正常。

### 对我行的启示

1. **本地Harness是基础中的基础**：CLAUDE.md写得再好，AI连代码能不能编译通过都验证不了，后面一切都是空谈。我行Java项目占比高，本地环境改造需求更迫切
2. **接口抽象是关键杠杆**：依赖倒置不只是设计原则，更是让AI跑起来的必要条件——不抽接口，本地化无从谈起
3. **Profile隔离保证安全**：零侵入原则确保本地改造不引入线上风险，这对金融系统尤为重要
4. **CLI化是AI化的前提**：行内Diamond/HSF/Switch等管理平台GUI化程度高，需要先CLI桥接才能让AI调用
5. **渐进式改造可行**：不需要一次性改造完所有依赖，找到核心链路（请求→LLM→Tool→返回）所需最小依赖集合，先让这条链路本地跑通

---

## 文章引用列表

| # | 标题 | 来源 | 核心要点 |
|---|------|------|----------|
| [1] | Harness Engineering（驾驭工程） | 微信公众号 | R.E.S.T框架、PPAF循环、REPL容器、六原则、四层沙箱 |
| [2] | 从 Prompt Engineering 到 Harness Engineering | 阿里妹 | 三次范式跃迁、四根支柱、四种失败模式、十阶段流程、AI代码率25%→90% |
| [3] | 终端沙箱：Agent Harness 的基础设施 | Qoder/通义灵码 | 终端沙箱三层防护、三平台实现、性能开销、对银行启示 |
| [4] | 一个 AI 还是不够 | MiniMax 稀宇科技 | Agent Team 架构、Leader-Worker-Verifier、四场景落地、成本验证 |
| [5] | OpenClacky Harness 工程7个决策 | AI Maker Summit（李亚飞） | 两代失败教训、双Cache标记、System Prompt字节冻结、Skill子Agent、固定16工具、压缩策略、工具自进化、内置浏览器接管 |
| [6] | Java微服务本地化改造：AI Coding的最后一公里 | 内部技术实践 | 依赖倒置/零侵入Profile/CLI优先三条原则，本地Harness让AI自主验证，单次迭代从10分钟降到秒级 |

---

_最后更新：2026-05-21_  
_版本：v1.5_