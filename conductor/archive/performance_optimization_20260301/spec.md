# Track Specification - performance_optimization_20260301

## Overview
针对用户反馈的网页加载慢（特别是图片和产品展示页）的问题，开展专项性能优化。通过前端技术手段减少首屏加载流量，提升视觉响应速度。

## Functional Requirements
- **图片延迟加载 (Lazy Loading)**：在 `dzweb/templates/` 下的所有相关模板中，为 `<img>` 标签添加 `loading="lazy"` 属性。
- **图片压缩**：编写并运行一次性脚本，使用 `Pillow` 库对 `dzweb/static/images/` 目录下的超大 JPG/PNG 图片进行压缩优化。
- **静态资源缓存**：在 Flask 应用配置中，确保为静态文件（CSS, JS, Images）设置合理的 `SEND_FILE_MAX_AGE_DEFAULT` 或通过响应头设置缓存策略。
- **性能审计**：使用 Lighthouse 评估优化前后的性能指标（如 LCP, FCP）。

## Non-Functional Requirements
- **画质平衡**：压缩后的图片在视觉上不应有明显降级，需保持工业自动化设备的专业展示效果。
- **兼容性**：Lazy Loading 采用原生属性，对旧版浏览器应能优雅降级（即正常同步加载）。

## Acceptance Criteria
- [ ] 产品展示页的所有产品图片均已启用 `loading="lazy"`。
- [ ] `dzweb/static/images/` 目录下的总资源体积显著减小。
- [ ] Lighthouse 审计中的 Performance 分数有明显提升。
- [ ] 页面在低速网络环境下的“首次有效渲染时间”得到缩短。

## Out of Scope
- 更换图片服务器或引入第三方 CDN 服务。
- 改变现有的 UI 布局或设计风格。
