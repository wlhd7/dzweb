# Track Specification: SEO Optimization for Baidu and Bing

## 概述 (Overview)
优化广州东振工业自动化有限公司官网（dzweb）在搜索引擎，特别是百度（Baidu）和 Bing 上的可见度。重点在于完善元数据、建立动态站点地图、集成站长工具以及增强多语言环境下的权重关联。

## 功能需求 (Functional Requirements)

### 1. 页面级 TDK 优化 (Page-specific TDK)
- **目标**：为所有核心页面（首页、案例、产品、联系我们、关于）在三种语言（中、英、日）下配置精细化的 Title、Description 和 Keywords。
- **动态支持**：产品详情页和案例详情页应能根据数据库中的名称和描述自动生成相关的 TDK。

### 2. 动态 Sitemap 生成 (Dynamic Sitemap)
- **路由**：实现 `/sitemap.xml` 路由。
- **内容**：自动包含所有已发布的产品、案例以及静态页面的多语言 URL。
- **频率**：访问时动态生成，确保始终包含最新内容。

### 3. 百度主动推送集成 (Baidu Active Push)
- **功能**：在管理员通过后台发布新产品或新案例时，通过 API 实时将新 URL 推送给百度搜索资源平台，加快收录速度。

### 4. 多语言 SEO 增强 (Multi-language SEO)
- **Hreflang 标签**：在 HTML `<head>` 中加入 `rel="alternate" hreflang="..."`，明确关联不同语言版本的对应关系。
- **Canonical 标签**：在所有页面加入 `rel="canonical"`，防止重复内容影响权重。

### 5. 站长工具与统计 (Webmaster Tools & Analytics)
- **站点验证**：支持在模板中添加百度和 Bing 的验证元标签。
- **百度统计**：在基础模板中集成百度统计 (Baidu Tongji) 代码。

## 非功能需求 (Non-Functional Requirements)
- **移动端友好**：确保页面在移动端的 Meta 标签（如 `viewport`）和适配性能符合百度移动优先策略。
- **性能优化**：尽量减少脚本阻塞，优化图片加载（Lazy Loading），提升首屏渲染速度。
- **规范性**：遵循 Flask 项目现有的架构和 `{{ _('...') }}` 国际化规范。

## 验收标准 (Acceptance Criteria)
- [ ] `/sitemap.xml` 能够正确显示全站 URL，并能通过百度/Bing 的校验。
- [ ] 首页、产品列表、案例列表及详情页拥有针对性的多语言 TDK 元数据。
- [ ] 页面源代码中包含正确关联的 `hreflang` 和 `canonical` 标签。
- [ ] 后台发布新内容后，后台日志应显示百度主动推送 API 的成功返回信息。
- [ ] 百度统计脚本在全站正常加载。
- [ ] 站点在百度和 Bing 的站长工具中成功通过所有权验证。

## 超出范围 (Out of Scope)
- 外部链接建设（外链）。
- 搜索引擎付费广告（SEM/竞价排名）。
- 社交媒体营销。
