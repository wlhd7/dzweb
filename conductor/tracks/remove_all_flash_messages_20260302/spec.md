# Track Specification: Global Removal of Flash Message System

## Overview
全站范围内废除 Flask 的 `flash()` 消息机制。由于系统已采用更现代的内联 `<p>` 标签反馈机制，现有的全局 Flash 提示会导致界面重复、样式不统一及用户体验干扰。本项目将彻底清理后端代码、前端模板及样式表中的 Flash 相关残留。

## Functional Requirements
1.  **后端代码清理 (Backend Cleanup)**:
    - 遍历 `dzweb/routes/` 下的所有模块（`admin.py`, `product.py`, `contact.py`, `home.py` 等）。
    - 移除所有 `flash()` 调用。
    - 确保移除后原有的业务逻辑流（如跳转）保持完整。
2.  **前端模板清理 (Template Cleanup)**:
    - 从 `base.html` 中移除全局的 `get_flashed_messages()` 渲染代码块。
    - 检查并移除 `admin/login.html`、`contact/mailbox.html` 等子模板中独立的 Flash 渲染逻辑。
3.  **样式表清理 (Style Cleanup)**:
    - 从 `dzweb/static/css/base.css` 中删除 `.flash` 类及其子类的所有样式。

## Acceptance Criteria
- [ ] 代码库中不再存在 `flash(` 字符串（文档除外）。
- [ ] 全站页面头部不再出现带背景色的提示条。
- [ ] 关键业务反馈（如登录失败）仍能通过现有的内联 `<p>` 标签正常显示。
- [ ] 页面布局未因移除 `.flash` 容器而发生意外坍塌。
