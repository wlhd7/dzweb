# Implementation Plan: Global Company Name Update

## Phase 1: 国际化与翻译更新 (i18n & Translation Update) [checkpoint: 2bd35f1]
重点是通过翻译系统进行源头修改，确保核心名称的自动转换。

- [x] Task: 编写测试用例，验证各语言版本下公司名称的输出 [15a1a58]
- [x] Task: 更新 `dzweb/translations/en/LC_MESSAGES/messages.po` 对应条目 [15a1a58]
- [x] Task: 更新 `dzweb/translations/ja/LC_MESSAGES/messages.po` 对应条目 [15a1a58]
- [x] Task: 编译翻译文件 (`pybabel compile -d dzweb/translations`) [15a1a58]
- [x] Task: Conductor - User Manual Verification 'Phase 1: i18n Update' (Protocol in workflow.md) [2bd35f1]

## Phase 2: 模板与元数据重构 (Template & Meta Refactoring)
清理可能存在的硬编码字符串，并更新 SEO 关键字段。

- [x] Task: 全局搜索并替换模板 (`templates/**/*.html`) 中硬编码的旧公司名称 [15a1a58]
- [x] Task: 更新 `base.html` 中的 JSON-LD 结构化数据 [15a1a58]
- [x] Task: 检查并更新 `instance/config.py` 中的 SEO 默认值 [15a1a58]
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Template Refactoring' (Protocol in workflow.md)

## Phase 3: 项目文档同步 (Documentation Sync)
确保开发辅助文档与实际名称保持一致。

- [ ] Task: 更新 `conductor/product.md` 中的产品定义
- [ ] Task: 更新 `PRD.md` 和 `README.md` 中的引用
- [ ] Task: 更新 `SEO_SETUP_GUIDE.md` 中的指南内容
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Documentation Sync' (Protocol in workflow.md)

## Phase 4: 全站验证与提交 (Final Validation & Commit)
进行最后的回归测试，确保没有遗漏点。

- [ ] Task: 执行全量单元测试
- [ ] Task: 手动检查全站各语言页面的 Footer、Title 和 Meta 信息
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Validation' (Protocol in workflow.md)
