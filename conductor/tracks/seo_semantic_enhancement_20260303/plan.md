# SEO 结构优化与语义化增强 实施计划

## 阶段 1: 环境准备与自动化测试定义 (Phase 1: Setup & TDD) [checkpoint: 7f5411c]
- [x] Task: 在 `dzweb/static/css/base.css` 中定义 `.visually-hidden` 类，用于隐藏 <h1>。 [2c36c2d]
- [x] Task: 在 `tests/test_seo.py` 中编写自动化测试，验证 <h1> 的唯一性和图片 `alt` 属性。 [f449b3d]
    - [x] 检查首页 <h1> 及其内容。 [f449b3d]
    - [x] 检查产品分类列表页 <h1> 及其内容。 [f449b3d]
    - [x] 检查产品详情页 <h1> 及其内容。 [f449b3d]
    - [x] 检查全站关键图片的 `alt` 属性。 [f449b3d]
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md) [7f5411c]

## 阶段 2: 模板结构升级与语义化增强 (Phase 2: Template Refactoring)
- [x] Task: 修改 `dzweb/templates/base.html`，在首页区块添加视觉隐藏的 <h1>。 [ac29c9b]
- [~] Task: 修改 `dzweb/templates/product/main.html`，将产品分类页的标题 (<p>) 升级为 <h1>，并保持原有样式。
- [ ] Task: 修改 `dzweb/templates/product/display.html`，将详情页产品标题 (<h2>) 升级为 <h1>，并保持原有样式。
- [ ] Task: 修改 `dzweb/templates/macro.html`，为 `side_bar_imag()` 宏中的图片添加 `alt` 属性。
- [ ] Task: 遍历首页 (`home/index.html`)，为所有建筑、招聘及服务系统的图片添加描述性的 `alt` 属性。
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## 阶段 3: 验证与最终部署 (Phase 3: Validation & Finalization)
- [ ] Task: 运行所有 SEO 相关的自动化测试，确保功能通过且无回归。
- [ ] Task: 手动检查全站视觉效果，确保 <h1> 升级没有破坏布局和间距。
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
