# Track Specification: 更新 SEO (SEO Update)

## 概述 (Overview)
通过增强动态 Sitemap 生成逻辑、优化经典案例页面的 Meta 标签以及清理冗余的静态文件，提升广州东振机电设备有限公司网站在各大搜索引擎（百度、Google、Bing）的收录效果。

## 功能需求 (Functional Requirements)
1.  **动态 Sitemap 增强**：
    *   在 `/sitemap.xml` 路由生成的站点地图中包含所有“经典案例”详情页的 URL。
    *   确保每个 URL 均包含 zh、en、ja 三个语言版本的 `hreflang` 关联。
2.  **移除静态文件**：
    *   物理删除 `dzweb/static/sitemap.xml`，确保搜索引擎直接访问动态生成的 `/sitemap.xml` 路由。
3.  **案例页 Meta 优化**：
    *   为案例展示页面 (`case/display.html`) 实现动态的 `<title>`、`<meta name="description">` 和 `<meta name="keywords">` 块。
    *   元数据内容应从案例标题和案例内容中提取，并应用多语言翻译。
4.  **结构化数据增强**：
    *   在产品详情页 (`product/display.html`) 进一步完善 `Product` Schema（JSON-LD）。
    *   在案例详情页增加适当的结构化数据（如 `CreativeWork` 或通用 `WebPage`）。

## 非功能需求 (Non-Functional Requirements)
*   **兼容性**：确保生成的 XML 符合 Google/Baidu 最新的 Sitemap 协议标准。
*   **多语言一致性**：SEO 标签应随语言切换自动适配，不产生硬编码中文。

## 验收标准 (Acceptance Criteria)
*   [ ] 访问 `/sitemap.xml` 可以查看到包含产品和案例详情的完整列表。
*   [ ] 物理路径中不再存在 `dzweb/static/sitemap.xml`。
*   [ ] 任意案例详情页的 HTML 源码中，`<title>` 和 `<meta>` 标签均与其标题一致。
*   [ ] Google 富媒体搜索结果测试工具（Rich Results Test）通过。

## 超出范围 (Out of Scope)
*   新增 SEO 关键词的人工翻译（仅使用现有 `_()` 翻译机制）。
*   修改页面 UI 布局。
