# Gemini CLI Configuration (Bilingual)

## 业务背景 (Business Context)
- **企业名称**：广州东振工业自动化有限公司 (Guangzhou Dongzhen Industrial Automation Co., Ltd.)
- **核心业务**：机器人焊接、非标自动化设备、工装夹具、视觉系统集成。
- **语言偏好**：用户交互优先使用 **中文**。

## 开发规范 (Technical Specs - English)

### 1. Flask Architecture
- **Factory Pattern**: Must use `create_app()` in `dzweb/__init__.py`.
- **Blueprints**: All routes must be registered via `dzweb.routes.bps`.
- **Naming**: Snake_case for Python, kebab-case for CSS classes.

### 2. UI/UX Guidelines
- **CSS**: Use `dzweb/static/css/base.css` as foundation. Maintain consistency with industrial/professional aesthetic.
- **SVGs**: Prefer SVG icons over raster images for UI elements (located in `static/images/*.svg`).

### 3. I18n Mandatory
- Never hardcode Chinese/English strings in templates.
- Always use `{{ _('String') }}` or `_l('String')`.

### 4. Resource Integrity Protocol
- **Sync Deletion**: When a database record (e.g., product) is deleted, the associated physical file (image) must be removed from `UPLOAD_FOLDER`.
- **Sync Update**: When a record is updated with a new file, the previous physical file must be cleaned up to prevent storage bloat.
- **Maintenance**: Always provide or maintain CLI commands for mass orphan file cleanup.

## 交互偏好 (Interaction Preferences)
- **分析优先**：在修改代码前，必须先分析对应的 `routes/*.py` 和 `templates/*.html`。
- **原子化更新**：每次修改尽量只涉及一个模块（如只改 Product 模块）。
