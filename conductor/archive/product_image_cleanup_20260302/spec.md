# Specification: Product Image Cleanup Sync

## Overview
目前系统在删除或更新产品图片时，物理文件会保留在服务器上（`instance/uploads/`），导致存储空间浪费。本 Track 旨在实现数据库记录与物理文件的同步删除，并提供存量孤儿文件的清理工具。

## Functional Requirements
1.  **同步删除 (Sync on Delete)**:
    - 修改 `/product/<id>/delete` 路由。
    - 在删除数据库记录前，定位对应的图片文件并执行删除。
    - 如果文件删除失败（如 IO 错误），需向用户报错并停止数据库删除操作。
2.  **更新清理 (Cleanup on Update)**:
    - 修改 `/product/<id>/update` 路由。
    - 当用户上传新图片替换旧图片时，在保存新图并更新数据库成功后，自动删除旧的图片文件。
3.  **孤儿文件清理脚本 (Orphan Cleanup Tool)**:
    - 实现一个 CLI 工具（如 `flask cleanup-images`）。
    - 遍历 `UPLOAD_FOLDER` 目录下的所有文件。
    - 检查文件名是否在 `products` 表的 `filename` 字段中存在。
    - 删除所有在数据库中无记录的图片文件。

## Non-Functional Requirements
- **安全性**: 仅删除 `UPLOAD_FOLDER` 下的文件，防止路径穿越风险。
- **一致性**: 采用严格同步策略，确保数据库状态与物理文件状态一致。

## Acceptance Criteria
- [x] 成功删除产品后，对应的图片文件从 `instance/uploads/` 中消失。
- [x] 成功更新产品图片后，旧图片文件被自动移除。
- [x] 若物理文件无法删除，系统应通过 Flash 消息告知用户，且不删除数据库记录。
- [x] 运行清理脚本后，所有“孤儿”文件被正确识别并删除。

## Out of Scope
- 图片的备份或版本管理。
- 对第三方图床（如阿里云 OSS）的支持（目前仅限本地文件系统）。
