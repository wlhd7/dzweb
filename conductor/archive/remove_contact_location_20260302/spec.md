# Track Specification: 删除 contact/location 路由

## Overview
广州东振机电设备有限公司网站的 `contact/location` 路由（用于显示公司位置）已被决定移除。
其功能将被完全删除，且所有旧链接将通过 301 永久重定向到 `contact` 首页（`contact.contact_us`）。

## Functional Requirements
- **移除路由**: 从 `dzweb/routes/contact.py` 中删除 `location` 视图函数。
- **配置重定向**: 在 `dzweb/routes/contact.py` 中为原路径配置 301 重定向到 `contact.contact_us`。
- **清理模板**: 删除 `dzweb/templates/contact/location.html`。
- **更新链接**:
  - 更新 `dzweb/templates/contact/main.html` 中的导航链接。
  - 更新 `dzweb/routes/home.py` 中引用的路由列表。
- **SEO 清理**: 从 `dzweb/static/sitemap.xml` 中移除相关 URL。

## Non-Functional Requirements
- **SEO 友好**: 确保所有旧链接通过 301 重定向，避免 404 错误影响排名。

## Acceptance Criteria
- [ ] 访问 `/contact/location` 能够自动 301 重定向到 `/contact/` (或对应的 contact 首页路径)。
- [ ] `dzweb/templates/contact/location.html` 文件已被物理删除。
- [ ] `dzweb/templates/contact/main.html` 中不再包含指向 `location` 的无效链接。
- [ ] `dzweb/routes/home.py` 逻辑运行正常，不受影响。
- [ ] `sitemap.xml` 中不再包含已删除的 URL。

## Out of Scope
- 其他 contact 子路由（如 `contact_us`, `message_board`, `mailbox`）的修改。
- 网站整体布局或样式的重大更改。