# Implementation Plan - product_image_optimization_20260302

## Phase 1: 基础架构与缩略图逻辑 (Infrastructure & Core Logic)
- [x] Task: 创建图片处理工具函数 (ee23209)
    - [x] 在 `dzweb/utils/` 创建 `image.py`。
    - [x] 使用 Pillow 实现 `generate_thumbnail(file_path, thumb_path, size=(400, 300))`。
- [ ] Task: 确保缩略图目录存在
    - [ ] 更新 `dzweb/__init__.py` 的 `create_app`，自动创建 `instance/uploads/thumbs` 目录。
- [ ] Task: 添加缩略图访问路由
    - [ ] 在 `dzweb/routes/__init__.py` 中添加 `thumbnail_files` 路由。
    - [ ] 映射 `/thumbnail-files/<filename>` 到 `instance/uploads/thumbs`。

## Phase 2: 产品模块更新与资源同步 (Product Module Update & Sync)
- [ ] Task: 更新产品“创建”逻辑
    - [ ] 在 `dzweb/routes/product.py` 的 `create` 视图中引入缩略图生成逻辑。
- [ ] Task: 更新产品“更新”逻辑
    - [ ] 在 `update` 视图中，上传新图片时生成对应缩略图，并删除旧的缩略图。
- [ ] Task: 更新产品“删除”逻辑
    - [ ] 在 `delete` 视图中，删除产品的同时删除对应的缩略图文件。
- [ ] Task: 增强图片清理 CLI 命令
    - [ ] 更新 `cleanup-images` 命令，使其能够扫描并清理 `thumbs/` 目录下的孤儿缩略图。

## Phase 3: 前端集成 (Frontend Integration)
- [ ] Task: 在首页应用缩略图
    - [ ] 更新 `dzweb/templates/home/index.html`，将产品展示图片的 `url_for` 指向 `thumbnail_files`。
- [ ] Task: 在产品列表页应用缩略图
    - [ ] 更新 `dzweb/templates/product/main.html`，统一使用缩略图。
- [ ] Task: 在搜索结果页应用缩略图
    - [ ] 更新 `dzweb/templates/product/search.html`。

## Phase 4: 旧数据迁移 (Data Migration)
- [ ] Task: 实现迁移 CLI 命令
    - [ ] 在 `dzweb/routes/product.py` 中添加 `flask generate-thumbs` 命令。
    - [ ] 遍历数据库中所有产品，为缺失缩略图的产品生成缩略图。

## Phase 5: 测试与验证 (Testing & Verification)
- [ ] Task: 编写自动化测试
    - [ ] 验证上传图片后 `thumbs/` 目录确实产生了文件。
    - [ ] 验证删除产品后缩略图被物理删除。
- [ ] Task: 执行手动验证
    - [ ] 运行迁移命令并检查结果。
    - [ ] 检查首页加载速度及图片路径。
- [ ] Task: Conductor - User Manual Verification 'Product Image Optimization' (Protocol in workflow.md)
