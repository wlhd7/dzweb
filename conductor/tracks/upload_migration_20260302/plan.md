# Implementation Plan: Uploads Directory Migration

## Phase 1: 调研与准备 (Research & Analysis)
- [x] Task: 搜索整个项目中所有对 `instance/uploads` 和 `UPLOAD_FOLDER` 的硬编码引用。
- [x] Task: 分析 `dzweb/utils/image.py` 中的图片处理逻辑，确认其路径依赖。
- [x] Task: Conductor - User Manual Verification 'Research & Analysis' (Protocol in workflow.md)

## Phase 2: 环境与配置更新 (Environment & Configuration)
- [x] Task: 修改 `.gitignore`，移除对 `dzweb/static/uploads/` 的忽略规则（或添加例外），确保其被 Git 跟踪。 4fd2099
- [~] Task: 更新 Flask 工厂函数 (`dzweb/__init__.py`) 中的 `UPLOAD_FOLDER` 配置，将其指向 `dzweb/static/uploads/`。
- [ ] Task: 更新 `Dockerfile` 和 `docker-compose.yml`，调整挂载卷（Volumes）路径及容器内目录权限。
- [ ] Task: Conductor - User Manual Verification 'Environment & Configuration' (Protocol in workflow.md)

## Phase 3: 业务逻辑与测试迁移 (TDD Logic Migration)
- [ ] Task: 迁移图片工具类逻辑。
    - [ ] Write tests for path resolution in `tests/test_image_utils.py`.
    - [ ] 修改 `dzweb/utils/image.py` 使其通过测试。
- [ ] Task: 更新产品管理模块的上传逻辑。
    - [ ] Write tests for product image creation and deletion in `tests/test_product_api.py`.
    - [ ] 更新 `dzweb/routes/admin.py` 或 `dzweb/routes/product.py` 中的相关路由逻辑。
- [ ] Task: 更新模板中的图片引用路径（如果之前使用的是 `url_for('uploaded_file', ...)`，可能需要调整）。
- [ ] Task: Conductor - User Manual Verification 'Code Logic Migration' (Protocol in workflow.md)

## Phase 4: 物理迁移与最终验证 (Data Migration & Final Verification)
- [ ] Task: 执行物理迁移：将 `instance/uploads/` 下的所有内容移动到 `dzweb/static/uploads/`。
- [ ] Task: 验证网站现有产品、案例图片的显示是否正常。
- [ ] Task: 在 Docker 环境下执行一次干净的构建和启动，验证权限与持久化是否正常。
- [ ] Task: 清理旧的 `instance/uploads/` 目录。
- [ ] Task: Conductor - User Manual Verification 'Data Migration & Final Verification' (Protocol in workflow.md)
