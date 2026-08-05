#!/usr/bin/env python3
"""一次性脚本：更新 2026-08-02 所有文章 front matter"""
import os, glob, re

BASE = "/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/daily/2026-08-02/sources"

articles = {
    # filename pattern -> (category, is_model_related, digest)
    "AI短剧取代真人剧": ("其他", False, """\
AI短剧市场正在快速膨胀。2026年上半年国内AI短剧市场规模突破220亿元，全年有望冲击400亿元。影视制作人谭飞指出，目前约95%的微短剧已由AI制作，大量真人腰部演员和群众演员面临无戏可拍的困境。AI以更低成本、更快速度产出内容，入行门槛被抬升，真人演员若不珍惜每次表演机会，可能被AI无声取代。但AI短剧也有明显短板——演员表情空洞、缺乏真实感，恐怖谷效应让不少观众本能划走。与此同时，短剧造星逻辑已被颠覆：一部爆款即可催生"顶流"，但短剧记忆度和观众黏性远不及传统影视，新星如流星般快速来去。文章呼吁：科技最终应该是辅助人提升价值，而非取代人。"""),

    "李飞飞教机器人摸麻将": ("国际", False, """\
李飞飞的具身智能研究又进一步。继提出空间智能概念后，今年6月她参与的研究T-Rex为机器人加入高频触觉反馈，使其完成翻书页、拿鸡蛋、挤牙膏、拧灯泡等高精度操作。研究发现，当前多模态模型普遍存在"幻景推理"问题——模型在没有看到图片的情况下仍能生成看似合理的描述，纯靠语言统计猜测而非真正视觉理解。这解释了为什么机器人需要多传感器融合：深度相机、3D激光雷达、触摸传感器等各司其职，才能确认物体的真实位置和物理属性。World Labs将当前世界模型分为三类：渲染器负责生成像素，模拟器负责物理属性，规划器负责行动决策。区分渲染与真正理解，是具身智能走向实用的关键门槛。"""),

    "谷歌机器人整了波大活儿": ("国际", False, """\
Google DeepMind发布Gemini Robotics 2，主打"全身智能"概念。该模型由三个子模型组成：Gemini Robotics ER 2负责环境理解和任务规划，Gemini Robotics 2将视觉和语言直接转化为动作，On-Device 2将动作模型压缩至本地设备，可用少于200个样例完成新本体适配。核心突破在于：机器人不再"先站好、再伸手"，而是将双腿、躯干、双臂和手指作为一个相互耦合的整体进行协调控制。Apptronik Apollo 2展示了弯腰捡水壶、从货架取手套等动作，但数据也揭示现实差距：地面取物成功率仅45.7%，多指灵巧手拧上灯泡成功率仅36%，扎垃圾袋仅44%。机器人距离实用还有"最后几厘米"的精度缺口。"""),

    "贝索斯用 AI 寻找下一块硅": ("国际", False, """\
亚马逊创始人贝索斯投资AI材料发现公司CuspAI。该公司完成4.5亿美元B轮融资后估值达26亿美元，投资方包括Kleiner Perkins、NEA、英国主权AI基金、AMD和三星等。CuspAI成立不到两年，核心路线是：用AI从已知走向未知——不局限于处理现有信息，而是帮助人类发现全新的材料。传统材料研发依赖试错和化学直觉，而AI可在近乎无限的化学空间中高效搜索，加速半导体材料、固态电解质、催化剂等关键材料的发现。文章指出，人类工业文明的每次跃迁都依赖于一种关键材料（青铜、钢铁、硅、锂），而AI正成为寻找"下一块硅"的新引擎。"\
"""),

    '"榨"出硅的极限': ("国内", False, """\
AI行业正从"造芯"转向"榨芯"——提高现有GPU利用率成为新热点。CMU研究显示，756块GPU集群中近20%执行时间处于空转状态，Azure Code负载高达65%能耗浪费在无效等待上。推理引擎赛道火热：Baseten一年收入增长20倍、估值达130亿美元；fireworks七个月估值翻四倍至175亿；开源双子星vLLM和SGLang先后商业化，种子轮均超1亿美元。文章由SGLang孵化的RadixArk联合创始人深度解读AI Infra四层架构（能源→硬件→分布式系统→推理引擎），指出全栈协同优化是将每瓦算力效率榨到极限的关键路径。"""),

    "25岁，爆仓": ("deleted", False, ""),

    "观众需要AI明星吗": ("其他", False, """\
AI演员近期引爆网络，话题#两个AI演员比内娱待爆艺人都火#登顶微博热搜第一，霸榜超8小时。2026年上半年国内AI短剧市场规模突破220亿元，安徽卫视自7月22日起在晚间黄金档开播全AI制作剧集，AI漫剧官宣二搭视频半天斩获29万点赞，热度不输真人顶流。但争议同样激烈：观众批评AI演员"表情空洞、缺乏真实感"，恐怖谷效应让许多人本能划过。制作方则看重低成本、零塌房风险、百倍产能等压倒性优势。老牌明星开始将肖像授权给AI，传统卫视也向AI演员开放，AI造星生态正在形成。"""),

    "突发！OpenAI下一代AI攻克": ("国际", True, """\
OpenAI内部模型Astra一次性攻克10个长期悬而未决的数学难题，涵盖高维几何、编码理论、群论、算子代数、量子复杂度、格密码学和极值组合学等领域。最突出的成果包括：终结了Gromov自1999年提出的非sofic群问题，构造出首个无限有限呈现的非sofic群；突破1978年以来高维球体堆积密度上限；推翻1982年菲尔兹奖得主Connes的刚性猜想。全部10项突破总推理成本不足2000美元，每个难题平均约200美元，相当于一名研究生一个周末的津贴。OpenAI公开了249页完整论文和Lean 4形式化证明。数学家评价这是"现代数学史单日跨度最大的一次飞跃"，AI正式成为数学家的"破壁者"。"""),

    "如何让自己变得让人工智能": ("其他", False, """\
与其哭诉AI取代工作，不如成为"不可受雇"的超级个体。文章系统性地剖析了现代社会的"薪资奴役"困境：雇主主导的单一技能体系禁锢人的多元潜能，上班8小时后精神透支、无力发展自己，最终在AI淘汰潮中毫无反击之力。真正出路在于建立"事业型个人品牌"——不再依赖单一雇主，而是围绕好奇心、激情、掌控感和精通感这四大心流驱动力，构建可持续的个人内容或产品体系，在心流状态下持续突破能力边界，让自己成为AI无法复制的独特存在。"""),

    "马斯克和 Altman": ("其他", False, """\
极客公园综合资讯，包含多条与AI相关的快讯：①马斯克和Altman罕见达成共识，均认为人类已进入AI奇点时代，Altman称AI已可自动化30-40%的人类工作；②高通完成收购AI基础设施公司Modular，Chris Lattner出任高通AI软件与平台执行副总裁；③谷歌、微软、Meta、亚马逊四巨头承诺未来数年投入2.4万亿美元建设AI数据中心，但自由现金流均已转负或接近转负；④苹果警告AI算力短缺可能导致产品延期发布；⑤亚马逊CEO贾西称AI基础设施投入与AWS早期扩张路径相似，长期回报可期。"""),

    "NVIDIA AI Releases Molt": ("国际", False, """\
NVIDIA NeMo团队发布Molt，一个PyTorch原生的Agent强化学习框架。其核心设计目标极为独特：代码库仅约8600行（对比verl的6.2万行、slime的2.5万行），精简到研究者可将整个框架装进大脑、AI编程助手能完整阅读和理解。Molt由Ray负责资源调度、vLLM负责rollout、NVIDIA AutoModel+FSDP2负责训练，三个组件均未fork上游，可直接获取最新改进。默认配置需2节点×8 H100 GPU（8训练+8rollout），适用于多轮工具调用Agent、代码执行Agent、视觉语言环境和LLM-as-judge奖励循环等场景。采用Apache 2.0开源协议。"""),

    "AMD Releases Instella": ("国际", True, """\
AMD发布Instella-MoE-16B-A3B，一个完全开放的混合专家（MoE）语言模型。总参数160亿，活跃参数约28亿，从零开始在AMD Instinct MI300X加速器上训练完成。模型采用标准MoE架构，推理时仅激活约18%的参数，兼顾性能和效率。AMD同步发布了完整训练代码、数据集、模型权重和评估结果，成为少数提供全开源训练配方的大模型厂商。此举标志着AMD在AI软件生态上的持续加码，直接与NVIDIA在模型开源层面展开竞争。"""),

    "Accelerating Transformer Training": ("国际", False, """\
NVIDIA发布技术教程，详解Transformer Engine如何通过融合GPU内核、BF16和FP8混合精度加速Transformer模型训练。核心原理是在训练前向和反向传播中动态缩放张量到FP8精度，利用H100/H200 GPU的FP8 Tensor Core实现更高吞吐量，同时通过自动混合精度管理防止精度损失。融合内核将多个连续操作（如矩阵乘法+偏置+激活函数）合并为单个GPU内核调用，大幅减少显存读写和kernel启动开销，是当前大模型训练效率优化的关键技术路径。"""),
}

def update_file(filepath, category, is_model_related, digest):
    with open(filepath) as f:
        content = f.read()

    # Replace entire front matter
    pt = re.search(r'publish_time:\s*(\d+)', content).group(1)
    new_fm = f"""---
publish_time: {pt}
status: confirmed
category: {category}
is_model_related: {str(is_model_related).lower()}
digest: |
  {digest.strip()}
---

"""
    # Remove old front matter
    rest = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    new_content = new_fm + rest

    with open(filepath, 'w') as f:
        f.write(new_content)

    print(f"  ✅ {os.path.basename(filepath)[:50]} -> {category} {'🔵' if is_model_related else ''}")

# Scan and update
deleted_files = []
for mp in sorted(glob.glob(os.path.join(BASE, "*.md"))):
    bn = os.path.basename(mp)
    matched = False
    for key, (cat, imr, dig) in articles.items():
        if key in bn:
            if cat == "deleted":
                deleted_files.append(mp)
                print(f"  🗑️  {bn[:50]} -> DELETE")
            else:
                update_file(mp, cat, imr, dig)
            matched = True
            break
    if not matched:
        print(f"  ⚠️  No match for: {bn[:50]}")

# Remove deleted files
for f in deleted_files:
    os.remove(f)
    print(f"  🗑️  Removed: {os.path.basename(f)[:50]}")

print(f"\n📊 Done: {len(articles)} articles processed")

# Verify
confirmed = 0
for mp in glob.glob(os.path.join(BASE, "*.md")):
    with open(mp) as f:
        c = f.read()
    if 'status: confirmed' in c:
        confirmed += 1
        cat = re.search(r'category:\s*(\S+)', c)
        imr = re.search(r'is_model_related:\s*(\S+)', c)
        print(f"  📄 {os.path.basename(mp)[:50]} | {cat.group(1) if cat else '?'} | model={imr.group(1) if imr else '?'}")

print(f"\n✅ Confirmed: {confirmed} articles")
