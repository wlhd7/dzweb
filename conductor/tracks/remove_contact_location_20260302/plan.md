# Implementation Plan - 删除 contact/location 路由

## Phase 1: 准备与测试环境搭建 [checkpoint: a53a1a0]
- [x] Task: 备份并确认环境。 (657d33e)
- [x] Task: 编写针对 `contact.location` 路由当前行为的测试用例（确认其目前返回 200）。 (657d33e)
- [x] Task: Conductor - User Manual Verification 'Phase 1: 准备与测试环境搭建' (Protocol in workflow.md) (a53a1a0)

## Phase 2: 代码与模板清理
- [x] Task: 修改 `dzweb/routes/contact.py`，移除 `location` 视图函数，并添加 301 重定向逻辑。 (f574686)
    - [x] 移除 `location` 视图函数。 (f574686)
    - [x] 添加 `@bp.route('/location')` 装饰器指向重定向函数或在 `location` 原位置返回 `redirect(url_for('.contact_us'), code=301)`。 (f574686)
- [x] Task: 修改 `dzweb/templates/contact/main.html`，移除指向 `location` 的 `<a>` 标签。 (d9e22d9)
- [ ] Task: 修改 `dzweb/routes/home.py`，从循环列表或逻辑中移除 `contact.location`。
- [ ] Task: 修改 `dzweb/static/sitemap.xml`，删除 `/contact/location` 条目。
- [ ] Task: 物理删除 `dzweb/templates/contact/location.html`。
- [ ] Task: Conductor - User Manual Verification 'Phase 2: 代码与模板清理' (Protocol in workflow.md)

## Phase 3: 验证与验收
- [ ] Task: 更新测试用例。
    - [ ] 确认访问 `/contact/location` 返回 301 并重定向到 `/contact/`。
    - [ ] 确认重定向后的目标页面返回 200。
- [ ] Task: 运行全量测试套件，确保没有回归。
- [ ] Task: Conductor - User Manual Verification 'Phase 3: 验证与验收' (Protocol in workflow.md)
