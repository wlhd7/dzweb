# Implementation Plan: Global Removal of Flash Message System

## Phase 1: 全面审计 (Full Audit)
- [x] Task: 使用 `grep` 扫描全站 Python 文件，确认所有 `flash()` 调用点。
- [x] Task: 使用 `grep` 扫描全站 HTML 文件，确认所有 `get_flashed_messages()` 调用点。
- [x] Task: Conductor - User Manual Verification 'Phase 1: 全面审计' (Protocol in workflow.md) [checkpoint: 14c5dcb]

## Phase 2: 后端清理 (Backend Cleanup)
- [x] Task: 移除 `dzweb/routes/admin.py` 中的 `flash()`。 14c5dcb
- [x] Task: 移除 `dzweb/routes/product.py` 中的 `flash()`。 14c5dcb
- [x] Task: 移除 `dzweb/routes/contact.py` 及其它模块中的 `flash()`。 14c5dcb
- [x] Task: Conductor - User Manual Verification 'Phase 2: 后端清理' (Protocol in workflow.md) [checkpoint: f0671eb]

## Phase 3: 前端清理 (Frontend Cleanup)
- [x] Task: 修改 `dzweb/templates/base.html`，删除 Flash 渲染块。 84b9365
- [x] Task: 检查并修改 `login.html`, `mailbox.html` 等子模板，移除重复的 Flash 逻辑。 84b9365
- [x] Task: 修改 `dzweb/static/css/base.css`，删除 `.flash` 相关样式。 84b9365
- [x] Task: Conductor - User Manual Verification 'Phase 3: 前端清理' (Protocol in workflow.md) [checkpoint: 84b9365]

## Phase 4: 验证与交付 (Verification & Delivery)
- [~] Task: 运行现有测试套件，确认业务流程未受损。
- [ ] Task: 手动触发一次登录失败，验证内联 `<p>` 提示是否依然如预期工作。
- [ ] Task: Conductor - User Manual Verification 'Phase 4: 验证与交付' (Protocol in workflow.md)
