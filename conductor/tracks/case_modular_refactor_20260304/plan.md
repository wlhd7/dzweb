# Implementation Plan: "经典案例" (Case) 模块化重构

## Phase 1: Database & Model Layer
- [x] Task: 更新数据库架构，添加 `case_modules` 和 `case_contents` 表以支持模块化存储。 (dffd7d5)
- [x] Task: 在 `dzweb/db.py` 中实现案例及其内容块的 CRUD (增删改查) 逻辑。 (e5d8b2d)
- [x] Task: 为数据库访问逻辑编写单元测试。 (a55106c)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Database & Model Layer' (Protocol in workflow.md)

## Phase 2: Content Management Backend (API)
- [x] Task: 在 `dzweb/routes/case.py` 中实现案例管理 API（创建、删除模块，添加、编辑、删除、排序内容块）。 (c0154b4)
- [x] Task: 集成现有 WebP 转换和缩略图生成逻辑，支持案例图片的自动化处理。 (7fa5535)
- [x] Task: 实现物理资源清理逻辑，确保删除案例或图片时物理文件同步移除。 (7248f48)
- [x] Task: 编写针对 API 和资源清理逻辑的集成测试。 (5ee3b47)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Content Management Backend (API)' (Protocol in workflow.md)

## Phase 3: Admin Sidebar & Module Initialization
- [x] Task: 更新 `dzweb/templates/case/main.html` 及侧边栏，实现管理员“新增”按钮 and 模块列表展示。 (10a1215)
- [x] Task: 实现模块初始化前端逻辑（弹窗收集标题、Slug 等基本信息）。 (24000c0)
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Admin Sidebar & Module Initialization' (Protocol in workflow.md)

## Phase 4: Dynamic Content Stream & Sorting UI
- [x] Task: 实现内容流编辑界面（交互式的“+”方框、内容块预览面板、排序按钮）。 (36585ad)
- [x] Task: 完成多语言翻译 (I18n) 集成，确保标题和文案支持中英日切换。 (36585ad)
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Dynamic Content Stream & Sorting UI' (Protocol in workflow.md)

## Phase 5: Dynamic Routing & Final Integration
- [x] Task: 实现公共展示页面的动态路由 `/case/<slug>`，支持按序渲染案例内容块。 (10a1215)
- [x] Task: 确保侧边栏在所有案例独立页面均可正常工作，并支持高亮当前选中的案例。 (10a1215)
- [x] Task: 执行全面冒烟测试，验证从后台管理到前台展示的完整闭环。 (371b621)
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Dynamic Routing & Final Integration' (Protocol in workflow.md)

## Phase 6: Automated Translation Integration
- [x] Task: 集成 `deep-translator` 并在后台实现中文标题和文案的自动英日翻译。 (ef2a01d)
- [x] Task: 更新 `requirements.txt`。 (ef2a01d)
- [ ] Task: Conductor - User Manual Verification 'Phase 6: Automated Translation Integration' (Protocol in workflow.md)
