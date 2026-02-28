# Sub-Agents Registry (Bilingual)

## 1. i18n-specialist (English)
- **Responsibility**: Handle `Flask-Babel` extraction, translation file synchronization, and language toggle logic.
- **Workflow**: `pybabel extract` -> `pybabel update` -> `manual edit .po` -> `pybabel compile`.

## 2. route-architect (English)
- **Responsibility**: Design and implement new Blueprints and views.
- **Constraints**: Ensure every view handles `@login_required` correctly and links to corresponding templates in `templates/<module>/`.

## 3. static-asset-manager (English)
- **Responsibility**: Manage `static/images` (SVGs, JPGs) and `static/css`. 
- **Guideline**: Ensure new images follow the naming convention (e.g., `case-<type>-<num>.jpg`).

## 4. 业务逻辑专家 (Chinese)
- **职责**：确保所有代码实现符合“广州东振”的业务逻辑，包括产品分类、招聘流程及内部应用权限。
