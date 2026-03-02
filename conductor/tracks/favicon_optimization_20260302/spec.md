# Specification: Favicon Loading Optimization

## Overview
用户报告在浏览 dzweb (广州东振机电设备有限公司官方网站) 时，每次刷新页面浏览器都需要加载一会儿才能显示 `favicon`。目前使用的是 `.ico` 格式的文件，且该问题影响全站所有页面。本 Track 旨在排查并优化 `favicon.ico` 的加载与缓存策略，消除页面刷新时的图标加载延迟。

## Functional Requirements
1. **明确的资源引用**: 在全站公共的 `<head>` 区域（如 `base.html`）中，显式声明 `<link rel="icon" href="...">` 和 `<link rel="shortcut icon" href="...">`。
2. **高效的路由/静态服务**: 确保 `/favicon.ico` 的请求被正确且高效地处理。如果目前通过 Flask 路由提供，需审查其性能；更佳实践是利用 Flask 的静态文件缓存机制或 Nginx 的静态资源处理。
3. **缓存控制 (Cache-Control)**: 为 `favicon.ico` 设置激进的客户端缓存头部（例如 `max-age=31536000`, `public`），确保浏览器仅在首次访问时下载，后续刷新直接从本地缓存读取。

## Non-Functional Requirements
- **性能**: 消除因重复请求 `favicon.ico` 造成的页面加载视觉延迟。
- **兼容性**: 需兼容主流现代浏览器（Chrome, Firefox, Safari, Edge）以及百度等搜索引擎的爬虫习惯。

## Acceptance Criteria
- [ ] 所有页面的 HTML `<head>` 中均包含正确的 `favicon` 引用标签。
- [ ] 浏览器开发者工具 (Network 选项卡) 显示，在第二次访问或刷新页面时，`favicon.ico` 能够从磁盘缓存或内存缓存中命中 (HTTP Status 200/304 with Cache-Control headers)。
- [ ] 肉眼观察页面刷新时，标签页图标不再出现闪烁或延迟加载。

## Out of Scope
- 重新设计或更换新的品牌 Logo 图标。
- 提供 `.svg` 或 `.png` 等现代格式的 Favicon（除非 `.ico` 文件本身存在损坏或极端过大需要替换格式以压缩体积，目前默认维持 `.ico`）。
