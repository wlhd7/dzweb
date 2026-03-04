# Implementation Plan: 更新 SEO (SEO Update)

## Phase 1: 基础清理与环境准备 (Preparation & Cleanup) [checkpoint: 384599e]
- [x] Task: 物理删除静态文件 `dzweb/static/sitemap.xml` (25dc8a4)
- [x] Task: 编写测试用例验证 `/sitemap.xml` 路由的响应状态 (5f1ec2f)
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md) (384599e)

## Phase 2: 动态 Sitemap 增强 (Sitemap Enhancement)
- [x] Task: 修改 `dzweb/routes/home.py` 中的 `sitemap` 路由，包含所有“经典案例”详情页 URL (8cae6c1)
- [x] Task: 在 Sitemap 中为案例 URL 增加多语言 (`hreflang`) 支持 (8cae6c1)
- [x] Task: 为不同类型的页面分配合理性的 SEO 权重 (Priority) (8cae6c1)
- [x] Task: 编写测试验证 Sitemap XML 中包含预期的产品和案例 URL 数量 (8cae6c1)
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: 案例展示页 Meta 优化 (Case Page SEO Optimization)
- [ ] Task: 在 `dzweb/templates/case/display.html` 中增加 `title`、`description` 和 `keywords` 的 Jinja2 Block
- [ ] Task: 实现从案例内容中动态提取描述信息的逻辑（优先使用摘要，无摘要则截取正文）
- [ ] Task: 编写测试验证不同语言环境下案例页面的 `<title>` 标签正确显示
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: 结构化数据 (JSON-LD) 增强 (Structured Data Enhancement)
- [ ] Task: 优化 `dzweb/templates/product/display.html` 中的 `Product` Schema，增加缺失的属性（如 brand, offers 等，视现有数据而定）
- [ ] Task: 在 `dzweb/templates/case/display.html` 中集成 `Article` 或 `CreativeWork` 类型的 JSON-LD
- [ ] Task: 验证结构化数据的语法正确性（使用测试用例模拟渲染结果）
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: 最终验证与交付 (Final Verification)
- [ ] Task: 全局回归测试，确保 SEO 修改未影响现有业务逻辑
- [ ] Task: 检查 `robots.txt` 是否正确指向动态 Sitemap 路由
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)
