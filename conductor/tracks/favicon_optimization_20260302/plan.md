# Implementation Plan: Favicon Loading Optimization

## Phase 1: 现状审查与文件验证 (Audit & Verification)
- [ ] Task: 检查项目目录中 `favicon.ico` 文件的确切位置及其文件大小（确保不是异常大文件）。
- [ ] Task: 审查 `dzweb/routes/__init__.py` 或其他路由文件中现有的 `/favicon.ico` 处理逻辑。
- [ ] Task: Conductor - User Manual Verification 'Audit Phase' (Protocol in workflow.md)

## Phase 2: HTML 头部显式声明 (Explicit HTML Declaration)
- [ ] Task: 修改 `dzweb/templates/base.html`，在 `<head>` 区域注入标准的 `<link rel="icon" type="image/x-icon" href="{{ url_for('static', filename='favicon.ico') }}">` 及快捷图标标签。
- [ ] Task: 修改 `dzweb/templates/admin/base.html` (如果有独立的后台基础模板)，同样注入该标签以覆盖后台页面。
- [ ] Task: 编写或更新针对基础模板渲染的单元测试，断言 `<link rel="icon"` 存在。
- [ ] Task: Conductor - User Manual Verification 'HTML Update' (Protocol in workflow.md)

## Phase 3: Flask 路由与缓存优化 (Route & Cache Optimization)
- [ ] Task: 更新现有的 `/favicon.ico` 路由处理器，为其添加强缓存相关的 HTTP Response Headers (`Cache-Control: public, max-age=31536000`)。或者重构为直接由 Flask static 机制托管并全局配置 `SEND_FILE_MAX_AGE_DEFAULT`。
- [ ] Task: 编写测试用例，请求 `/favicon.ico` 并断言响应头中包含正确的缓存控制指令。
- [ ] Task: Conductor - User Manual Verification 'Cache Optimization' (Protocol in workflow.md)
