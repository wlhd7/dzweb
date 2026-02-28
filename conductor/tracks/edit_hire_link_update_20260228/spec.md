# Track Specification - edit_hire_link_update_20260228

## Overview
此任务旨在更新 `admin/edit-hire` 路由对应的 `user/edit-hire-permission.html` 页面上的链接及其描述性文字。目前，该页面的“请点击这里”链接未正确指向“新增职位”功能。本次修改将更新链接指向 `human.create_position`，并同步优化 UI 以保持页面一致性。

## Functional Requirements
- **链接更新**：将 `user/edit-hire-permission.html` 中的超链接更新为指向 `/human/create-position` (即 `human.create_position` 路由)。
- **文案更新**：将链接文字“请点击这里”修改为更具描述性的文案（例如：“点击此处新增职位”）。
- **页面同步**：确保页面的标题（Title）和主体描述内容与“新增职位”这一操作完全对应，消除歧义。

## Non-Functional Requirements
- **一致性**：保持现有的专业工业风视觉风格。
- **国际化 (I18n)**：所有新增或修改的字符串必须使用 `{{ _('...') }}` 或 `_l('...')` 进行国际化处理。

## Acceptance Criteria
- [ ] 访问 `/admin/edit-hire` 时，页面显示的链接正确跳转至 `/human/create-position`。
- [ ] 页面上的链接文字已更新。
- [ ] 页面的标题和描述文本已同步更新，能够准确反映新增职位的意图。
- [ ] 修改不破坏现有的国际化支持。

## Out of Scope
- 修改 `human.create_position` 的实际后端逻辑。
- 修改其他管理员路由或招聘管理之外的页面。
