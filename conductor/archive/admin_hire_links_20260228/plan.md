# Implementation Plan - admin_hire_links_20260228

## Phase 1: Analysis and Test Preparation [checkpoint: 50b229e]
- [x] Task: 分析现有的 `dzweb/templates/human/hire.html` 模板及其逻辑
    - [x] 确认判断管理员登录状态的现有变量或 Session 逻辑 (session.get('is_admin') and g.user)
    - [x] 确认编辑 (`human.update_position`) 和删除 (`human.delete_position`) 的路由名称及参数
- [x] Task: 编写针对管理员招聘链接显示的测试用例 (TDD - Red Phase) cfbea6a
    - [x] 在 `tests/test_human.py` 或相关测试文件中编写测试
    - [x] 验证普通用户访问 `/human/hire` 时，页面不包含“编辑”和“删除”链接
    - [x] 验证管理员登录后，页面包含“编辑”和“删除”链接且跳转正确
    - [x] 运行测试并确认失败
- [x] Task: Conductor - User Manual Verification 'Phase 1: Analysis and Test Preparation' (Protocol in workflow.md) 50b229e

## Phase 2: Template Update and Verification [checkpoint: f49dcff]
- [x] Task: 更新 `dzweb/templates/human/hire.html` 模板 (TDD - Green Phase) 4e00e1f
    - [x] 添加条件判断逻辑，仅在管理员已登录时显示管理区域
    - [x] 编写符合样式要求的链接 (蓝色文本, `blue link` 类)
    - [x] 添加 `onclick="return confirm('...')"` 删除确认逻辑
    - [x] 所有文案进行 I18n 处理
- [x] Task: 运行测试并确认通过 (TDD - Green Phase) 4e00e1f
    - [x] 运行 `pytest` 确认所有相关测试通过
    - [x] 检查代码覆盖率是否达标
- [x] Task: 更新翻译文件 (I18n) d42838f
    - [x] 提取并补充新增文案的中、英、日语翻译
- [x] Task: Conductor - User Manual Verification 'Phase 2: Template Update and Verification' (Protocol in workflow.md) f49dcff
