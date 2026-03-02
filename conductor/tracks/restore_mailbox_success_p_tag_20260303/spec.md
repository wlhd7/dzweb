# Specification: Restore Mailbox Success <p> Tag

## Overview
在 `contact/mailbox` 页面提交表单发送成功后，恢复原本出现在页面底部的成功提示 `<p>` 标签。该功能在之前的“全局移除 Flash 消息”任务中被误删，且需按照用户要求，不再使用 Flask 的 Flash 系统，改为直接插入的标签。

## Functional Requirements
1. **后端路由**：在 `dzweb/routes/contact.py` 的 `mailbox` 函数中，当邮件发送成功后，渲染模板时传递 `success=True` 变量。
2. **前端模板**：在 `dzweb/templates/contact/mailbox.html` 的表单下方插入逻辑，渲染内容为 `_('感谢您的反馈，我们会尽快处理！')` 的 `<p>` 标签。
3. **样式与翻译**：确保标签样式正确，并支持 I18n 多语言翻译。

## Acceptance Criteria
- [ ] 成功提交表单后，页面底部显示“感谢您的反馈，我们会尽快处理！”。
- [ ] 仅在成功提交后显示，直接访问或刷新页面时不显示。
- [ ] 标签不再依赖 `get_flashed_messages()`。
