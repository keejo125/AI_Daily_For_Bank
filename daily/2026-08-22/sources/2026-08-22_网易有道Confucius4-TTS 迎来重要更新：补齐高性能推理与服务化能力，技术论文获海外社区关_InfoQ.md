---
publish_time: 1787374825
link: https://www.infoq.cn/article/A59yGpmHXR5BbokJAPk5
source: InfoQ
status: confirmed
category: 国内
is_model_related: true
digest: |
  网易有道开源 TTS 模型 Confucius4-TTS 迎来更新，新增 vLLM 推理后端、流式语音生成与 Web Demo/API，补齐高性能推理与服务化能力；配套论文介绍其跨语种零样本语音合成与音色克隆方案。在英→中、中→英、中→韩、中→日方向人工评测中，该模型斩获3项综合第一、音色相似度4项第一、16项核心指标10项第一，获海外社区关注。
---

# 网易有道Confucius4-TTS 迎来重要更新：补齐高性能推理与服务化能力，技术论文获海外社区关注

> 原文链接：https://www.infoq.cn/article/A59yGpmHXR5BbokJAPk5
> 来源：InfoQ

Confucius4-TTS近日迎来一次重要更新，进一步补齐开源模型的高性能推理与服务化能力：新增vLLM推理后端，支持流式语音生成，并提供Web Demo与API接口，让开发者更容易部署和接入实际应用。

相关技术论文《Confucius4-TTS: Transcript-Free Cross-Lingual Zero-Shot TTS with a Learnable Speaker Encoder》已上线arXiv，系统介绍了模型在跨语种零样本语音合成与音色克隆方面的技术方案。

论文发布后也获得海外社区关注，官方推文评论区反响热烈，技术开发者对模型的实际效果给予高度评价。知名AI论文博主AK对相关内容进行了转发。斯坦福大学博士、硅谷语音AI公司OrukLabs创始人Nathan Roll在体验后称赞模型表现出色。

斯坦福大学博士、硅谷语音AI公司OrukLabs创始人Nathan Roll在体验后称赞模型表现出色。

在效果验证上，团队将Confucius4-TTS与ElevenLabs、MiniMax、OmniVoice、Qwen3、VoxCPM等5款主流开源及闭源TTS服务进行了人工主观评测。在中→英、英→中、中→韩、中→日4个跨语种方向中，Confucius4-TTS斩获3项综合第一、1项综合第二；音色相似度4个方向全部排名第一；16项核心指标中10项排名第一、15项进入前二。

从模型开源、效果验证，到推理加速、流式输出与服务化部署，网易有道正在持续完善Confucius4-TTS从“模型能力”到“开发者可用”的完整链路，为实时翻译、语音助手、数字人及内容创作等场景提供更加易用的多语种语音基础能力。