# Implementation Plan - Product Image Cleanup Sync

## Phase 1: 环境准备与基础设施
- [ ] Task: 验证 `UPLOAD_FOLDER` 配置并在测试套件中添加文件模拟工具
- [ ] Task: Conductor - User Manual Verification 'Phase 1: 环境准备与基础设施' (Protocol in workflow.md)

## Phase 2: 产品删除同步
- [ ] Task: TDD - 编写产品删除时物理文件同步删除的失败测试
- [ ] Task: 在 `product.delete` 路由中实现物理文件删除逻辑
- [ ] Task: 完善异常处理（如文件缺失时的报错逻辑）并确保测试通过
- [ ] Task: Conductor - User Manual Verification 'Phase 2: 产品删除同步' (Protocol in workflow.md)

## Phase 3: 产品更新同步
- [ ] Task: TDD - 编写产品更新（替换图片）时旧文件删除的失败测试
- [ ] Task: 在 `product.update` 路由中实现旧图片的物理删除逻辑
- [ ] Task: 验证更新操作后仅旧图被删，新图正确保留
- [ ] Task: Conductor - User Manual Verification 'Phase 3: 产品更新同步' (Protocol in workflow.md)

## Phase 4: 孤儿图片清理工具
- [ ] Task: TDD - 编写清理 CLI 命令的失败测试（模拟孤儿文件并验证删除）
- [ ] Task: 在应用中注册 `flask cleanup-images` 命令并实现清理逻辑
- [ ] Task: 验证清理工具能准确识别并移除所有不在数据库中的图片
- [ ] Task: Conductor - User Manual Verification 'Phase 4: 孤儿图片清理工具' (Protocol in workflow.md)

## Phase 5: 最终验收与文档
- [ ] Task: 运行完整测试套件并确保覆盖率符合要求 (>80%)
- [ ] Task: 手动验证完整链路（创建 -> 更新 -> 删除 -> 清理）
- [ ] Task: Conductor - User Manual Verification 'Phase 5: 最终验收与文档' (Protocol in workflow.md)
