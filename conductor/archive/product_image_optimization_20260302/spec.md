# Specification - product_image_optimization_20260302

## 1. 概述 (Overview)
实现产品图片的缩略图生成逻辑，以优化首页和产品列表页的加载速度。目前系统直接加载原图，导致性能瓶颈。

## 2. 功能需求 (Functional Requirements)
- **缩略图生成**：
    - 在产品“创建”和“更新”时，自动为上传的图片生成缩略图。
    - 缩略图尺寸固定为 **400x300**（按比例缩放并裁剪）。
    - 格式保持与原图一致（JPG/PNG）。
- **存储管理**：
    - 缩略图存储在 `instance/uploads/thumbs/` 目录下。
    - 文件名与原图保持一致。
- **前端显示**：
    - 首页、产品列表页（fixture, automation, non_standard, robotics）以及搜索结果页应优先加载缩略图。
    - 产品详情页（display.html）继续加载原图。
- **资源同步**：
    - 删除产品时，必须同时删除对应的原图和缩略图。
    - 更新产品图片时，必须清理旧的原图和旧的缩略图。
- **数据迁移**：
    - 提供一个 CLI 命令（例如 `flask generate-thumbs`），为系统中所有现有的产品图片一次性生成缩略图。

## 3. 非功能需求 (Non-functional Requirements)
- **性能**：使用 Pillow 库进行高效的图片处理。
- **可靠性**：如果生成缩略图失败，应记录日志但尽量不中断产品创建流程。

## 4. 验收标准 (Acceptance Criteria)
- [ ] 首页加载的产品图片链接指向 `/instance/uploads/thumbs/` 路径（通过路由映射）。
- [ ] 宿主机 `instance/uploads/thumbs/` 目录下存在对应的缩略图文件。
- [ ] 运行 `flask cleanup-images` 也能清理孤儿缩略图。
- [ ] 运行迁移命令后，所有旧产品都有了缩略图。
