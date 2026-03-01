# Track Specification: 为 instance 目录配置 Docker Volume

## Overview
为了确保用户上传的图片和 SQLite 数据库在 Docker 容器重启或销毁后能够持久化存储，需要为 `instance/` 目录配置 Docker Volume。

## Functional Requirements
- **挂载配置**: 更新 `docker-compose.yml`，将宿主机的 `./instance` 目录挂载到容器内的 `/app/instance` 目录（或相应的应用根路径）。
- **目录预置**: 更新 `Dockerfile`，确保在镜像构建阶段创建 `instance` 目录并设置正确的读写权限（尤其是在使用非 root 用户运行时）。
- **同步验证**: 确保挂载后，容器内对 `instance/` 的修改能实时同步到宿主机。

## Non-Functional Requirements
- **持久性**: 执行 `docker compose down` 后，`instance/` 目录下的数据不应丢失。
- **安全性**: 确保挂载的宿主机目录权限仅限 Docker 守护进程或特定应用用户。

## Acceptance Criteria
- [ ] `docker-compose.yml` 中包含 `volumes` 配置项，正确映射了 `instance` 目录。
- [ ] `Dockerfile` 中包含创建 `instance` 目录并设置权限的指令。
- [ ] 运行 `docker inspect <container_id>` 确认挂载点状态为 `bind` 且路径正确。
- [ ] 容器启动后，`instance` 目录下的文件可在宿主机对应的目录中被查看到。

## Out of Scope
- `/static` 目录的持久化挂载。
- 迁移现有的生产环境数据。