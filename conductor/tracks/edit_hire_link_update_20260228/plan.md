# Implementation Plan - edit_hire_link_update_20260228

## Phase 1: Analysis and Test Preparation
- [ ] Task: 分析现有的 `admin/edit-hire` 路由和 `user/edit-hire-permission.html` 模板
    - [ ] 确认当前模板中链接的 HTML 结构和使用的 I18n 键
    - [ ] 确认 `human.create_position` 的正确 URL 路径
- [ ] Task: 编写针对路由和模板更改的测试用例 (TDD - Red Phase)
    - [ ] 在 `tests/test_admin_auth.py` 中增加或修改测试，验证 `/admin/edit-hire` 页面上的链接是否指向 `/human/create-position`
    - [ ] 验证页面上的文本是否包含预期的“新增职位”描述
    - [ ] 运行测试并确认失败
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Analysis and Test Preparation' (Protocol in workflow.md)

## Phase 2: Template and Route Update
- [ ] Task: 更新 `dzweb/templates/user/edit-hire-permission.html` 模板 (TDD - Green Phase)
    - [ ] 将超链接的 `href` 更新为 `{{ url_for('human.create_position') }}`
    - [ ] 更新链接文本为 `{{ _('点击此处新增职位') }}`
    - [ ] 更新页面标题 `{% block title %}` 为 `{{ _('新增招聘职位') }}`
    - [ ] 更新页面主体描述文案，使其与“新增职位”动作一致
- [ ] Task: 更新翻译文件 (I18n)
    - [ ] 运行 `pybabel extract` 和 `update` 确保新文案被捕获
    - [ ] 完善中、英、日文翻译条目
- [ ] Task: 验证更改并运行测试 (TDD - Green Phase)
    - [ ] 运行 `pytest` 确保所有相关测试通过
    - [ ] 检查代码覆盖率
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Template and Route Update' (Protocol in workflow.md)
