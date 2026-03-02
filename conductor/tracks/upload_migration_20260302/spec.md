# Specification: Uploads Directory Migration

## Overview
目前，网站的上传文件存储在 `instance/uploads/` 目录中，由于 `instance/` 默认不进入版本控制，导致这些资源无法同步到 GitHub。本 Track 的目标是将上传目录移至 `dzweb/static/uploads/`，使其成为网站源码的一部分，并由 Git 跟踪。

## Functional Requirements
1. **目录迁移**: 将所有现有的文件和子目录从 `instance/uploads/` 移动到 `dzweb/static/uploads/`。
2. **版本控制**: 确保 Git 跟踪 `dzweb/static/uploads/` 及其下的所有文件（修改 `.gitignore`）。
3. **Flask 配置更新**: 更新应用配置中的 `UPLOAD_FOLDER`，使其指向新位置。
4. **业务逻辑同步**: 
   - 修改所有涉及文件保存、删除和缩略图生成的工具类 (`dzweb/utils/image.py`)。
   - 确保路由层 (`routes/product.py` 等) 正确引用新的上传路径。
5. **Docker 配置同步**: 修改 `docker-compose.yml` 和 `Dockerfile`，调整对应的挂载卷 (Volumes) 和目录权限设置。

## Non-Functional Requirements
- **路径一致性**: 在代码中应使用相对于包根目录的动态路径，避免硬编码绝对路径。
- **资源完整性**: 迁移过程中需确保现有图片与数据库记录的对应关系不损坏。

## Acceptance Criteria
- [ ] `instance/uploads/` 已成功迁移并移除旧目录。
- [ ] `dzweb/static/uploads/` 中的资源可以被 Git 跟踪。
- [ ] 网站各模块（产品、案例等）的图片显示正常。
- [ ] 新上传的文件能正确保存到新路径。
- [ ] 在 Docker 环境下，上传功能与持久化存储依然有效。

## Out of Scope
- 迁移至第三方对象存储（如阿里云 OSS 或 AWS S3）。
- 对图片处理逻辑进行大规模重构（仅针对路径变更做必要修改）。
