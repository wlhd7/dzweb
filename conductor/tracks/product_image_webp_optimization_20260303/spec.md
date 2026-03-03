# Track: 详情页原图 WebP 性能优化 (product_image_webp_optimization_20260303)

## 1. 概览 (Overview)
优化 `product/display.html`（单个产品详情页）中原始图片的加载性能。目前的详情页直接加载未经压缩的大图，导致加载时间过长。本任务将针对这些原图引入 **WebP 衍生版本**，并在详情页优先通过 WebP 渲染，同时保持缩略图（Thumbnail）现有逻辑不变。

## 2. 功能要求 (Functional Requirements)
*   **后端图片处理 (Python/Flask)**:
    *   在上传产品图片逻辑中（`product.py`），除了保存原始 JPG/PNG 供未来可能的使用，**必须**同步生成一份对应的 **WebP 高质量版本**（用于详情页展示）。
    *   **存量处理**: 针对现有的所有详情页原图，提供脚本一次性生成对应的 WebP 副本。
*   **详情页重构 (Template)**:
    *   仅修改 `templates/product/display.html`。
    *   使用 `<picture>` 标签重构详情页图片渲染逻辑，优先请求 WebP 格式。
    *   **保留缩略图**: 首页及列表页使用的缩略图逻辑（目前工作良好）保持原状，不进行 WebP 改造。
*   **Blur-up 体验**:
    *   在原图加载期间，利用现有的极小缩略图（作为 Placeholder）实现模糊过渡效果，增强感知性能。
*   **交互策略**:
    *   **方案 A (性能优先)**: 浏览器会优先选择 WebP（更小更快）。此时右键“在新标签页中打开”获取的是 **`.webp`**。

## 3. 验收标准 (Acceptance Criteria)
1. 在单产品详情页，Chrome DevTools 确认加载的图片资源后缀为 `.webp`，大小显著减少。
2. 首页和列表页（使用缩略图的部分）代码和逻辑完全不受影响。
3. 删除产品时，原图、WebP 衍生图、缩略图三者均被清理干净。
