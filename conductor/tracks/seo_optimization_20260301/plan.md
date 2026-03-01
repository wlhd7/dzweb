# Implementation Plan: SEO Optimization for Baidu and Bing

## Phase 1: 多语言 SEO 基础设施 (Multi-language SEO Infrastructure) [checkpoint: 0be90ed]
该阶段重点在于基础模板的增强，加入通用的多语言关联标签和 TDK 逻辑。

- [x] Task: 编写多语言 `hreflang` 和 `canonical` 标签的单元测试 [f19da50]
- [x] Task: 在 `base.html` 中实现 `hreflang` 自动关联逻辑 [f19da50]
- [x] Task: 在 `base.html` 中实现 `canonical` 标签逻辑 [f19da50]
- [x] Task: 更新全局基础 TDK 默认值（中/英/日）并在 `base.html` 中应用 [f19da50]
- [x] Task: Conductor - User Manual Verification 'Phase 1: Multi-language SEO Infrastructure' (Protocol in workflow.md) [0be90ed]

## Phase 2: 动态 Sitemap 与 站长验证 (Dynamic Sitemap & Verification Tags)
实现动态站点地图，并添加百度/Bing 的所有权验证。

- [x] Task: 编写 `sitemap.xml` 路由的单元测试 [bb72ed4]
- [x] Task: 在 `dzweb/routes/home.py` 中实现动态生成 `sitemap.xml` 的逻辑 [bb72ed4]
- [x] Task: 在 `base.html` 中添加百度、Bing 的站点验证元标签（Meta Tags） [f19da50]
- [x] Task: 更新 `robots.txt` 以正确引导搜素引擎抓取 `sitemap.xml` [ce61f11]
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Dynamic Sitemap & Verification Tags' (Protocol in workflow.md)

## Phase 3: 核心页面 TDK 精细化优化 (Core Page TDK Optimization)
针对具体路由和模板，配置针对性的 TDK 元数据。

- [ ] Task: 为首页、关于、联系、服务、人才招聘页面配置精细化的 TDK 单元测试
- [ ] Task: 在各页面对应的路由 (`routes/*.py`) 和模板 (`templates/*.html`) 中覆盖默认 TDK
- [ ] Task: 实现产品详情和案例详情页的动态 TDK 生成逻辑
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Core Page TDK Optimization' (Protocol in workflow.md)

## Phase 4: 百度主动推送与统计集成 (Baidu Integration: Active Push & Tongji)
集成百度特有的 SEO 工具，提升收录效率和流量监控。

- [ ] Task: 编写百度主动推送 API (Baidu Active Push) 的集成测试（模拟 API 返回）
- [ ] Task: 在 `dzweb/routes/admin.py` 的产品/案例发布逻辑中加入主动推送代码
- [ ] Task: 在 `base.html` 中集成百度统计 (Baidu Tongji) 脚本
- [ ] Task: 配置主动推送成功/失败的日志记录
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Baidu Integration' (Protocol in workflow.md)

## Phase 5: 全站移动端验证与最终发布 (Mobile Verification & Final Release)
确保 SEO 优化在移动端生效，并完成最终全站验证。

- [ ] Task: 编写移动端 SEO 元标签验证测试
- [ ] Task: 进行全站移动端布局和交互测试，确保符合百度移动友好标准
- [ ] Task: 执行全量测试套件并验证代码覆盖率 > 80%
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Mobile Verification & Final Release' (Protocol in workflow.md)
