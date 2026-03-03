# Plan: 详情页原图 WebP 性能优化 (product_image_webp_optimization_20260303)

## Phase 1: 基础设施与库准备
- [ ] Task: 依赖检查与安装
    - [ ] 确保服务器环境下 `Pillow` 已安装且支持 WebP 编码。
    - [ ] 在 `requirements.txt` 中显式添加依赖。
- [ ] Task: Conductor - User Manual Verification 'Phase 1: 基础设施与库准备' (Protocol in workflow.md)

## Phase 2: 后端上传与处理逻辑 (Sync)
- [ ] Task: 修改上传函数
    - [ ] 在 `dzweb/routes/product.py` 中，修改 `upload_product` 逻辑。
    - [ ] 保存原图后，调用 `Pillow` 生成一份同名但后缀为 `.webp` 的文件，保存至 `static/uploads/`。
- [ ] Task: 维护物理删除一致性
    - [ ] 修改 `delete_product` 逻辑。
    - [ ] 确保删除数据库记录时，物理删除对应的：1. 原始 JPG/PNG 2. WebP 衍生图 3. 现有缩略图。
- [ ] Task: Conductor - User Manual Verification 'Phase 2: 后端上传与处理逻辑 (Sync)' (Protocol in workflow.md)

## Phase 3: 存量图片全量转换 (Migration)
- [ ] Task: 编写一次性迁移脚本
    - [ ] 编写一个 Flask CLI 命令或独立脚本 `scripts/migrate_to_webp.py`。
    - [ ] 遍历 `static/uploads/` 中所有非缩略图（即原始产品图片）。
    - [ ] 检查是否存在对应的 `.webp`，若无则生成。
- [ ] Task: 执行全量转换
    - [ ] 在服务器上运行该脚本。
- [ ] Task: Conductor - User Manual Verification 'Phase 3: 存量图片全量转换 (Migration)' (Protocol in workflow.md)

## Phase 4: 前端模板重构 (UI)
- [ ] Task: 修改 `display.html`
    - [ ] 将 `<img>` 标签重构为使用 `<picture>` 标签。
    - [ ] `source` 指向 `.webp`，`img` 指向原始 `.jpg/.png` (Fallback)。
- [ ] Task: 实现 Blur-up 过渡效果
    - [ ] 详情页默认加载已有的 **极小缩略图 (Thumbnail)** 并应用 CSS 模糊滤镜。
    - [ ] 当 WebP 原图加载完成后，平滑替换掉模糊背景。
- [ ] Task: Conductor - User Manual Verification 'Phase 4: 前端模板重构 (UI)' (Protocol in workflow.md)

## Phase 5: 验证与验收
- [ ] Task: 手动冒烟测试
    - [ ] 上传一个新产品，检查文件目录是否生成了 `.webp`。
    - [ ] 浏览器审查元素，确认加载的是 WebP 资源。
    - [ ] 删除该产品，确认所有物理文件均已清理。
- [ ] Task: Conductor - User Manual Verification 'Phase 5: 验证与验收' (Protocol in workflow.md)
