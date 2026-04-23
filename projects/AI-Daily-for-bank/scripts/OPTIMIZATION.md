# fetch_articles 性能优化说明

## v2 架构变更（2026-04-23）

### 新方式：导出接口（当前）

使用 `/api/rss/export/{date}` 一键导出接口：

- **请求数**：1 次 GET
- **耗时**：1-3 秒
- **登录态依赖**：导出接口从本地 SQLite 读取，不依赖微信登录态
- **数据完整性**：直接返回当天所有文章，含 content（HTML格式）
- **无需翻页**：服务端完成日期过滤，客户端直接拿结果

### 旧方式：逐公众号翻页（已废弃）

| 指标 | 原始版本 | 优化版本 |
|------|---------|---------|
| 请求数 | 18+（每公众号1-5页） | 18+ |
| 每页文章数 | 10 | 50 |
| 全文获取 | 逐篇串行 | 5线程并行 |
| 总耗时 | 5-10 分钟 | 2-4 分钟 |
| 登录态 | 必需 | 必需 |

旧方式保留在 `fetch_articles.py.bak` 中（如有需要）。

## fetch_articles_fast.py

`fetch_articles_fast.py` 现在直接调用 `fetch_articles.py` 的 main()，不再有独立逻辑。
保留此文件仅为兼容旧调用方式。

## 配置说明

`fetch_articles.py` v2 无需额外配置，使用 `config.json` 中的 `server.base_url` 构建导出接口 URL。

## 降级方案

如果导出接口不可用（如服务器重启、接口报错），可使用 SSH + sqlite3 直接查数据库：

```bash
ssh root@115.29.206.55 "sqlite3 /home/claw/wechat-query-skill/services/wechat-download-api/data/rss.db \"
SELECT a.aid, a.title, a.link, a.digest, a.content,
       a.publish_time, s.nickname
FROM articles a
JOIN subscriptions s ON a.fakeid = s.fakeid
WHERE a.publish_time >= strftime('%s','YYYY-MM-DD 00:00:00')
  AND a.publish_time < strftime('%s','YYYY-MM-DD 23:59:59')
ORDER BY a.publish_time DESC
\""
```

## 注意事项

1. **content 字段格式**：导出接口返回的 content 为 HTML 格式，脚本自动转换为纯文本保存到 .md 文件
2. **日期时区**：导出接口使用东八区日期边界，无需客户端计算时间戳
3. **登录态**：导出接口从本地数据库读取，不依赖微信登录态；但数据库本身的更新仍依赖登录态
