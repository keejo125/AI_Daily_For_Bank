# sources adapter package
"""
数据源适配器包 — 工厂模式

架构原则（重要）：
- 每个信源适配器负责"抓取 + 归一化"，输出统一的文章结构：
  [{"title", "link", "content", "source", "publish_time"}, ...]
- 编排层（fetch_web_articles.py）通过 create_adapter() 工厂按 type 实例化适配器，
  之后只依赖统一结构，完全不感知信源差异（RSS / 公众号 / 官方API / 热榜…）。
- 新增信源类型 = 新增一个适配器类 + 在 ADAPTER_REGISTRY 注册 + 在 sources.json 加一条配置，
  无需改动编排层和下游（filter / classify / generate）。
"""
from .base import BaseSourceAdapter
from .rss_adapter import RSSAdapter
from .wechat_rss_adapter import WechatRSSAdapter
from .kr36_adapter import Kr36APIAdapter

# 信源类型 → 适配器类 的注册表
ADAPTER_REGISTRY = {
    "rss": RSSAdapter,              # 官网 RSS/Atom（极客公园、Solidot、美团技术等）
    "wechat_rss": WechatRSSAdapter, # 第三方公众号RSS服务（decemberpei.cyou 等）
    "kr36_api": Kr36APIAdapter,     # 36氪官方热榜API（结构化JSON，含摘要）
}


def create_adapter(source_config: dict, global_settings: dict, article_fetch_api: str = "") -> BaseSourceAdapter:
    """
    工厂函数：根据信源配置中的 type 字段实例化对应适配器。

    source_config 必须包含:
      - type: 信源类型（见 ADAPTER_REGISTRY）
      - name: 信源名称
      - url:  信源地址
    未知 type 抛出 ValueError，由编排层捕获后跳过该信源（不中断管线）。
    """
    stype = source_config.get("type", "rss")
    adapter_cls = ADAPTER_REGISTRY.get(stype)
    if adapter_cls is None:
        raise ValueError(f"未知的信源类型: {stype}（可用: {', '.join(ADAPTER_REGISTRY)}）")
    return adapter_cls(source_config, global_settings, article_fetch_api)


__all__ = [
    "BaseSourceAdapter",
    "RSSAdapter",
    "WechatRSSAdapter",
    "Kr36APIAdapter",
    "ADAPTER_REGISTRY",
    "create_adapter",
]
