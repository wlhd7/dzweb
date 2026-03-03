# Track Specification: Remove Email Failure Flash Messages

## Overview
当系统邮件发送失败时（例如在客户反馈或内部通知场景下），目前的逻辑会触发一个 `<div class="flash">` 提示。由于该行为与现有的页面级提示（如 `<p>` 标签）重复，本项目旨在**全局移除**这种邮件发送失败时的 Flash 消息显示。

## Functional Requirements
1.  **全局清理 (Global Cleanup)**：
    - 在所有涉及 `flask-mail` 发送逻辑的视图函数（Blueprints）中，定位并移除用于显示“邮件发送失败”的 `flash()` 调用。
    - 确保 `dzweb/routes/contact.py` 及其它潜在路由中的冗余提示已被移除。
2.  **日志保留 (Logging)**：
    - 移除 UI 提示的同时，必须保留现有的后台错误日志（`current_app.logger.error`），以确保管理员能够通过服务器日志排查问题。

## Acceptance Criteria
- [ ] 在 `contact` 页面故意模拟邮件发送失败（例如使用错误的 SMTP 配置），系统**不会**显示 Flash 消息。
- [ ] 系统日志中能够正常看到对应的邮件发送失败记录。
- [ ] 现有的页面级提示（如 `<p>` 标签）应正常保留。
