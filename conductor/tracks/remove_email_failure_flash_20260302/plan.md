# Implementation Plan: Remove Email Failure Flash Messages

## Phase 1: 扫描与复现 (Scanning & Reproduction)
- [x] Task: 扫描代码库中包含“邮件发送失败，请稍后重试或联系管理员”或类似文本的 `flash()` 调用点。 218397a
- [~] Task: 模拟邮件发送失败（例如通过临时更改 `.env` 中的 SMTP 密码），确认目前确实会弹出 `<div class="flash">`。
- [ ] Task: Conductor - User Manual Verification 'Phase 1: 扫描与复现' (Protocol in workflow.md)

## Phase 2: 清理与移除 (Cleanup & Removal)
- [ ] Task: 移除 `dzweb/routes/contact.py` 及其它潜在路由中相关的 `flash()` 调用。
- [ ] Task: 检查 `dzweb/mail.py` 中的 `send_email` 或其他工具函数，确保不再返回可能触发 flash 的状态码或逻辑。
- [ ] Task: Conductor - User Manual Verification 'Phase 2: 清理与移除' (Protocol in workflow.md)

## Phase 3: 验证与验收 (Verification & Acceptance)
- [ ] Task: 再次模拟失败场景，验证不再显示 flash 提示，但原本已有的 `<p>` 标签提示功能应保持正常（如果有）。
- [ ] Task: 确认服务器后台日志仍能正确记录 `current_app.logger.error` 信息。
- [ ] Task: Conductor - User Manual Verification 'Phase 3: 验证与验收' (Protocol in workflow.md)
