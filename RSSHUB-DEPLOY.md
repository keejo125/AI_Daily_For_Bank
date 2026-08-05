# RSSHub 自建部署文档

> 为 AI 每日早报提供网页端稳定信源，替代被微信屏蔽的公众号信源
> 部署日期：2026-08-02
> 部署路径：`/home/claw/rsshub/`
> 最后更新：2026-08-02 21:40

---

## 一、对外访问地址

| 方式 | 地址 | 状态 |
|------|------|------|
| **HTTPS（推荐）** | `https://www.torandom.com/rsshub/<路由>` | ✅ 生产 |
| 内网直连 | `http://localhost:1200/<路由>` | 仅服务器本地 |

RSSHub 通过 **nginx 反向代理**对外暴露，挂载在现有域名 `www.torandom.com` 的 `/rsshub/` 路径下。
- 无需额外开放安全组端口（1200 仅本地监听）
- 复用已有 HTTPS 证书，自动加密
- 与现有 `/wechat-api/`、`/web/` 等服务共存，路径隔离

---

## 二、服务器信息

| 项目 | 配置 |
|------|------|
| 服务器 | 阿里云 115.29.206.55 |
| 用户 | root（Docker + nginx 管理） |
| 部署目录 | `/home/claw/rsshub/` |
| 容器端口 | `1200`（仅本地监听，不对外） |
| 对外域名 | `https://www.torandom.com/rsshub/` |
| 镜像加速 | `docker.m.daocloud.io` |

### nginx 反代配置

```nginx
# /etc/nginx/conf.d/https.conf（已生效）
location /rsshub/ {
    rewrite ^/rsshub/(.*)$ /$1 break;
    proxy_pass http://127.0.0.1:1200;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 30s;
}
```

修改后执行：`nginx -t && nginx -s reload`

---

## 三、架构

```
  本地脚本/web_fetch               浏览器
       │                              │
       │  GET /rsshub/meituan/tech    │
       ▼                              ▼
  https://www.torandom.com/rsshub/*  ←── nginx (443, HTTPS)
       │
       │  rewrite + proxy_pass
       ▼
  http://127.0.0.1:1200/*  ←── RSSHub 容器 (bridge网络)
       │                              │
       ├──▶ tech.meituan.com          │  ✅ 稳定
       ├──▶ www.infoq.cn              │  ✅ 稳定
       ├──▶ 36kr.com                  │  ✅ 稳定
       └──▶ blog.csdn.net/kuaishoutech│  ⚠️ CSDN 限速 521
       │
  Redis :6379（请求缓存 10min）
```

---

## 三、容器清单与资源占用

| 容器名 | 镜像 | 内存 | 端口 | 状态 |
|--------|------|------|------|------|
| `rsshub` | `diygod/rsshub:latest` | ~230MB | 1200 | ✅ |
| `rsshub-redis` | `redis:alpine` | ~12MB | 6379（内部） | ✅ |
| `wechat-download-api` | 自定义 | ~52MB | 5000 | ✅ |
| **合计** | | **~295MB** / 1.7GB | | 余量充裕 |

> 基础版镜像不含 Chromium，目标信源均为服务端渲染 HTML，无需 Puppeteer。

---

## 四、可用信源路由

### ✅ 已确认可用

| # | 信源 | 路由 | 每轮 | 分类 | 响应速度 | 内容特点 |
|---|------|------|------|------|----------|----------|
| 1 | 美团技术团队 | `/meituan/tech` | ~10篇 | 国内 | 1-2s | 大模型、AI Agent 前沿实践 |
| 2 | InfoQ AI频道 | `/infoq/topic/AI` | ~30篇 | 国际 | 2-5s | 行业深度报道、英文技术访谈 |
| 3 | 36氪最新资讯 | `/36kr/information/web_news` | ~30篇 | 其他 | 1-3s | 综合科技快讯（需 AI 过滤） |
| 4 | **快手技术 CSDN** | `/csdn/blog/kuaishoutech` | ~20篇 | 国内 | ⚠️ 首次 3-10s | 可灵多模态/KAT-Coder/顶会论文 |

> 总计 4 个信源，每轮 **~90 篇文章**，覆盖国际视野 + 大厂实战 + 行业快讯。
> 快手 CSDN 内容质量极高：可灵多模态、KAT-Coder、生成式推荐、AAAI 顶会——信息密度甚至超过美团。

### ❌ 不可用

| 信源 | 路由 | 原因 |
|------|------|------|
| HuggingFace Blog | `/huggingface/blog` | 国外站点，服务器访问超时（被墙） |
| 36kr AI专属 | `/36kr/motif/ai` | RSSHub 返回 503 |
| 腾讯云开发者 | `/tencent/cloud/blog` | RSSHub 路由 503，目标站 SPA 反爬 |
| 阿里达摩院 | `/alibaba/damo` | 不存在路由；目标站 Nuxt SPA，无 RSS |
| 阿里云开发者AI | `/alibaba/cloud/developer` | RSSHub 不支持该路由 |

---

## 五、使用方法

### 5.1 快速验证

```bash
# 测试单个信源
curl -s --max-time 30 "https://www.torandom.com/rsshub/meituan/tech" | python3 -c "
import sys, xml.etree.ElementTree as ET
tree = ET.parse(sys.stdin.buffer)
items = tree.getroot().findall('.//item')
print(f'文章数: {len(items)}')
for item in items[:5]:
    print(f'- {item.findtext(\"title\",\"?\")}')
"
```

### 5.2 Python 集成脚本（推荐）

```python
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

RSSHUB_BASE = "https://www.torandom.com/rsshub"

ROUTES = {
    "meituan": {
        "route": "/meituan/tech",
        "category": "国内",
        "source_name": "美团技术团队",
        "timeout": 15,
    },
    "infoq": {
        "route": "/infoq/topic/AI",
        "category": "国际",
        "source_name": "InfoQ",
        "timeout": 20,
    },
    "36kr": {
        "route": "/36kr/information/web_news",
        "category": "其他",
        "source_name": "36氪",
        "timeout": 15,
        "need_filter": True,
        "filter_keywords": ["AI", "大模型", "智能", "Agent", "OpenAI", "Claude",
                            "DeepSeek", "算力", "GPU", "模型", "ChatGPT", "LLM"],
    },
    "kuaishou": {
        "route": "/csdn/blog/kuaishoutech",
        "category": "国内",
        "source_name": "快手技术",
        "timeout": 30,  # ⚠️ CSDN 首次请求慢（521 限速重试），需要更长超时
    },
}

def fetch_rsshub(source_id):
    """从自建 RSSHub 获取文章列表"""
    cfg = ROUTES[source_id]
    url = f"{RSSHUB_BASE}{cfg['route']}"

    resp = requests.get(url, timeout=cfg["timeout"])
    if resp.status_code != 200:
        raise Exception(f"HTTP {resp.status_code}")
    if len(resp.content) == 0:
        raise Exception("0 字节返回 → 容器可能卡住或 OOM")

    tree = ET.fromstring(resp.content)
    articles = []
    for item in tree.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pubdate = item.findtext("pubDate") or ""

        if not title or not link:
            continue

        if cfg.get("need_filter"):
            text = title.lower()
            if not any(kw.lower() in text for kw in cfg["filter_keywords"]):
                continue

        articles.append({
            "source": cfg["source_name"],
            "title": title,
            "link": link,
            "published": pubdate,
            "category": cfg["category"],
        })

    return articles


# 抓取所有信源（带容错）
all_articles = []
for source_id in ROUTES:
    try:
        articles = fetch_rsshub(source_id)
        print(f"✅ {source_id}: {len(articles)} 篇")
        all_articles.extend(articles)
    except requests.Timeout:
        print(f"⏱️ {source_id}: 超时（超过 {ROUTES[source_id]['timeout']}s）")
    except Exception as e:
        print(f"❌ {source_id}: {e}")

print(f"\n总计: {len(all_articles)} 篇")
```

### 5.3 一键健康检查脚本

```bash
#!/bin/bash
# check-rsshub.sh - 验证所有信源

BASE="${1:-https://www.torandom.com/rsshub}"

ROUTES=(
  "meituan/tech|10"
  "infoq/topic/AI|20"
  "36kr/information/web_news|15"
  "csdn/blog/kuaishoutech|30"
)

echo "RSSHub 健康检查 @ $BASE"
echo "========================="

for entry in "${ROUTES[@]}"; do
  route="${entry%%|*}"
  timeout_s="${entry##*|}"
  url="$BASE/$route"

  code=$(curl -s -o /tmp/rsshub_test.xml -w '%{http_code}' --max-time "$timeout_s" "$url")
  size=$(wc -c < /tmp/rsshub_test.xml 2>/dev/null || echo 0)

  if [ "$code" = "200" ] && [ "$size" -gt 500 ]; then
    title=$(python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('/tmp/rsshub_test.xml')
print(tree.find('.//item/title').text[:50] if tree.find('.//item/title') is not None else '?')
" 2>/dev/null)
    echo "✅ /$route → HTTP 200, ${size}B, 首篇: $title"
  elif [ "$code" = "000" ]; then
    echo "🔴 /$route → 超时 (${timeout_s}s) — TCP 握手成功但无响应，容器可能 OOM"
  else
    echo "⚠️  /$route → HTTP $code, ${size}B"
  fi
done
```

---

## 六、运维命令

### 服务器上操作

```bash
ssh root@115.29.206.55

# 服务管理
cd /home/claw/rsshub
docker compose up -d          # 启动
docker compose restart        # 快速重启（缓存保留）
docker compose down           # 停止并清理
docker compose pull && docker compose up -d   # 更新镜像

# 查看状态
docker compose ps
docker logs rsshub --tail 50
docker stats --no-stream

# 容器内直接验证
curl -s --max-time 10 http://localhost:1200/meituan/tech | head -c 200
```

### 本机远程操作

```bash
# 查看服务状态
ssh root@115.29.206.55 "docker compose -f /home/claw/rsshub/docker-compose.yml ps"

# 重启（如果首次请求慢或超时）
ssh root@115.29.206.55 "docker compose -f /home/claw/rsshub/docker-compose.yml restart"

# 清理并重建（彻底修复异常状态）
ssh root@115.29.206.55 "cd /home/claw/rsshub && docker compose down && docker compose up -d"

# 查看资源占用
ssh root@115.29.206.55 "docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'"
```

---

## 七、故障排查

### 🔴 症状 1：访问超时、0 字节返回

nginx 反代链路：`外网 → nginx(:443) → rewrite → 127.0.0.1:1200 → RSSHub容器`，逐层排查：

```bash
# 第一层：nginx 是否可达
curl -s -o /dev/null -w "HTTP %{http_code} %{time_total}s\n" --max-time 5 https://www.torandom.com/rsshub/meituan/tech

# 第二层：nginx 反代是否通到 RSSHub（服务器本地）
ssh root@115.29.206.55 "curl -s -o /dev/null -w 'HTTP %{http_code} %{time_total}s' --max-time 5 http://localhost/rsshub/meituan/tech"

# 第三层：RSSHub 容器是否正常
ssh root@115.29.206.55 "curl -s -o /dev/null -w 'HTTP %{http_code} %{time_total}s' --max-time 5 http://localhost:1200/meituan/tech"
```

| 外网 HTTPS | 本机 nginx | localhost:1200 | 诊断 |
|-----------|-----------|---------------|------|
| ❌ 超时 | ❌ 超时 | ❌ 超时 | 容器挂了 |
| ❌ 超时 | ❌ 超时 | ✅ 正常 | nginx 配置问题 |
| ❌ 超时 | ✅ 正常 | ✅ 正常 | 外网/DNS 问题 |
| ❌ 404 | ✅ 正常 | ✅ 正常 | nginx rewrite 路径错误 |
| ✅ 正常 | ✅ 正常 | ✅ 正常 | 其他原因（目标站响应慢等） |

**容器挂了修：**
```bash
ssh root@115.29.206.55 "cd /home/claw/rsshub && docker compose down && docker compose up -d"
```

**nginx 配置问题修：**
```bash
ssh root@115.29.206.55 "grep -A 8 rsshub /etc/nginx/conf.d/https.conf"
# 确认 rewrite 和 proxy_pass 正确 → nginx -t && nginx -s reload
```

### ⚠️ 症状 2：CSDN（快手技术）返回慢或部分文章 521

**CSDN 的反爬虫策略**：首次请求会返回大量 `521` 错误（RSSHub 自动重试最多 2 次），导致首请求耗时 3-10 秒。

```bash
# 查看 CSDN 限速日志
ssh root@115.29.206.55 "docker logs rsshub --tail 30 | grep 521"

# 正常现象：缓存后第二次请求只需 4ms
# 不需要修复，保持 30s 超时 + 请求间加间隔即可
```

**应对策略：** 在抓取脚本中，对 CSDN 路由使用 30s 超时，且避免高频并发请求（每次间隔 5s+）。

### 症状 3：RSSHub 内存 OOM（230MB → 超过物理内存）

```bash
# 在 docker-compose.yml 添加内存限制
services:
  rsshub:
    deploy:
      resources:
        limits:
          memory: 400M
```

修改后 `docker compose up -d` 重建容器。

### 症状 4：目标网站改版导致路由 503

```bash
# 更新 RSSHub 镜像（社区会持续修复路由）
ssh root@115.29.206.55 "cd /home/claw/rsshub && docker compose pull && docker compose up -d"
ssh root@115.29.206.55 "docker image prune -f"
```

### 症状 5：Docker 镜像拉取失败

服务器 `/etc/docker/daemon.json`：
```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerhub.timeweb.cloud"
  ]
}
```
修改后 `systemctl restart docker`。

---

## 八、docker-compose.yml

```yaml
# /home/claw/rsshub/docker-compose.yml
services:
  rsshub:
    image: diygod/rsshub:latest
    container_name: rsshub
    restart: unless-stopped
    ports:
      - '1200:1200'
    environment:
      NODE_ENV: production
      CACHE_TYPE: redis
      CACHE_EXPIRE: 600
      CACHE_CONTENT_EXPIRE: 1800
      REDIS_URL: redis://redis:6379/
    depends_on:
      redis:
        condition: service_started
    dns:
      - 100.100.2.136
      - 100.100.2.138
    logging:
      options:
        max-size: '50m'
        max-file: '3'

  redis:
    image: redis:alpine
    container_name: rsshub-redis
    restart: unless-stopped
    volumes:
      - redis_data:/data
    logging:
      options:
        max-size: '10m'
        max-file: '1'

volumes:
  redis_data:
```

---

## 九、部署踩坑全记录

| # | 问题 | 根因 | 解决 |
|---|------|------|------|
| 1 | Docker Hub 拉取超时 | `ccr.ccs.tencentyun.com` DNS 失败 | 换 `docker.m.daocloud.io` |
| 2 | 公共实例全 403 | 官方限流 | 自建 |
| 3 | HuggingFace 超时 | 国外被墙 | 放弃 |
| 4 | Docker Hub 拉取超时 | `ccr.ccs.tencentyun.com` DNS 失败 | 换 `docker.m.daocloud.io` |
| 5 | CSDN 首请求 521 | CSDN 反爬限速 | 用 30s 超时 + Redis 缓存 |
| 6 | 服务器 SSH 偶发超时 | 阿里云 1Mbps 带宽限制 | 加大 ConnectTimeout |

---

## 十、与现有早报流水线的关系

| 抓取方式 | 状态 | 适用阶段 |
|----------|------|----------|
| 公众号 RSS（w`echat-download-api`） | ❌ 被微信屏蔽 | `wechat-article` skill → 已废弃 |
| 原生 RSS（36kr.com/feed） | ✅ 可用 | 噪音大，不如 RSSHub 结构化 |
| HTML 直抓（tech.meituan.com） | ⚠️ 需定制 | 网站改版即断 |
| **自建 RSSHub** | ✅ 主力方案 | 统一 RSS 格式 → 接入现有 `filter_articles.json` → `generate_html.py` |

### 集成到早报的路径

```
RSSHub 自建实例 (:1200)
    │
    ▼
fetch_web_articles.py   ← 新脚本，调用上方 Python 集成代码
    │ 输出 filtered_articles.json（与公众号格式对齐）
    ▼
build_classification.py ← 复用现有分类引擎
    │
    ▼
generate_html.py        ← 复用现有 HTML 生成
    │
    ▼
GitHub Pages → 飞书推送
```
