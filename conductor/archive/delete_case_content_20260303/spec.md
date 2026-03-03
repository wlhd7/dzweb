# Specification: 删除'经典案例'(case) 模块内容并合并页面

## 1. 概述 (Overview)
本任务旨在清理“经典案例”(case) 模块。具体操作包括备份并移除所有特定案例（如挤出机、机器人焊接等）的子页面与相关图片，并将该模块合并为一个单一的空白主页面，同时保持导航链接的可用性。

## 2. 功能需求 (Functional Requirements)
- **图片备份与清理**：
    - 在项目根目录下创建 `case/` 目录。
    - 将 `dzweb/static/images/` 中所有以 `case-` 开头的图片移动至根目录下的 `case/` 文件夹中进行备份。
- **路由重构**：
    - 修改 `dzweb/routes/case.py`，移除 `extruder`, `assembly_line`, `ass`, `robot_welding` 等特定子页面的路由定义。
    - 保留（或新增）`case.main` 路由，作为“经典案例”模块的唯一入口。
    - 更新 `dzweb/routes/home.py` 中引用的相关规则列表。
- **模板清理**：
    - 删除 `dzweb/templates/case/` 目录下的所有子页面模板：`extruder.html`, `assembly-line.html`, `ass.html`, `robot-welding.html`。
    - 清空 `dzweb/templates/case/main.html` 的具体内容，使其呈现为一个符合页面框架的基础空白页。
- **导航更新**：
    - 修改 `dzweb/templates/base.html`，确保“经典案例”导航项链接到 `case.main` 路由，并移除对已删除子页面的任何引用。

## 3. 非功能需求 (Non-Functional Requirements)
- **代码一致性**：遵循现有的 Flask Blueprint 结构和命名规范。
- **链接完整性**：确保导航栏中的“经典案例”链接在点击后不会产生 404 错误。

## 4. 验收标准 (Acceptance Criteria)
- [ ] 根目录下存在 `case/` 文件夹，且包含所有原 `case-*.jpg/png` 图片。
- [ ] `static/images/` 目录下不再包含 `case-*.jpg/png` 图片。
- [ ] 点击导航栏中的“经典案例”会跳转到一个显示空白内容的主页面（`case.main`）。
- [ ] 所有子页面路由（如 `/case/extruder`）均已失效（返回 404 是正常的，因为需求是删除它们）。
- [ ] `dzweb/templates/case/` 文件夹内仅保留 `main.html`。

## 5. 超出范围 (Out of Scope)
- 为“经典案例”添加新的内容或动态管理功能。
- 修改其他模块（如产品或服务模块）。
