# Implementation Plan: 删除'经典案例'(case) 模块内容并合并页面

## 阶段 1：准备与备份 (Preparation and Backup) [checkpoint: a1eaa99]
在该阶段，我们将完成图片的备份和原始模板的移动工作。

- [x] Task: 在项目根目录下创建 `case/` 目录用于备份。 (5bd87be)
- [x] Task: 将 `dzweb/static/images/case-*` 图片移动到根目录 `case/` 下，并从 `static/images/` 中移除。 (1cfffbc)
- [x] Task: Conductor - User Manual Verification '阶段 1：准备与备份' (Protocol in workflow.md)

## 阶段 2：重构路由与清理模板 (Route and Template Refactor) [checkpoint: 9e422cb]
在该阶段，我们将修改 Flask 路由定义并清理相关的 HTML 模板。

- [x] Task: 编写测试用例验证 `/case` 路由的可用性，并确认子页面路由（如 `/case/extruder`）应失效。 (7fa1f30)
- [x] Task: 修改 `dzweb/routes/case.py`：移除子页面路由，保留或重构 `case.main` 路由。 (4faf48c)
- [x] Task: 清理 `dzweb/templates/case/`：删除所有子页面模板，将 `main.html` 设置为基础空白页。 (9719559)
- [x] Task: 运行测试并确保所有测试通过。 (00d8696)
- [x] Task: Conductor - User Manual Verification '阶段 2：重构路由与清理模板' (Protocol in workflow.md)

## 阶段 3：全局引用清理 (Cross-Reference Cleanup)
在该阶段，我们将清理其他模块对已删除内容的引用。

- [x] Task: 编写测试用例验证导航栏中“经典案例”链接的有效性，并确认子菜单内容已移除。 (7c7317b)
- [x] Task: 修改 `dzweb/templates/base.html`，更新“经典案例”导航项链接并移除子菜单引用。 (890f426)
- [x] Task: 修改 `dzweb/routes/home.py`，移除对已删除子页面规则的引用。 (6367281)
- [x] Task: 运行全面测试并验证代码覆盖率。 (4c79d04)
- [ ] Task: Conductor - User Manual Verification '阶段 3：全局引用清理' (Protocol in workflow.md)

## 阶段 4：收尾工作 (Cleanup)
- [ ] Task: 确认所有静态资源（图片）已正确迁移且不再被引用。
- [ ] Task: Conductor - User Manual Verification '阶段 4：收尾工作' (Protocol in workflow.md)
