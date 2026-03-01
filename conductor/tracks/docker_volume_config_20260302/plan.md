# Implementation Plan: 为 instance 目录配置 Docker Volume

## Phase 1: Dockerfile 更新 [checkpoint: b738187]
- [x] Task: 分析并更新 `Dockerfile`。 (b738187)
    - [x] 确保在镜像内创建 `/app/instance` 目录。 (b738187)
    - [x] 设置 `chown` 指令以确保非 root 用户对该目录拥有读写权限。 (b738187)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Dockerfile 更新' (Protocol in workflow.md) (b738187)

## Phase 2: Docker Compose 配置 [checkpoint: 7eb3c64]
- [x] Task: 分析并更新 `docker-compose.yml`。 (ac76b4e)
    - [x] 在 `services` 节点下为应用容器添加 `volumes` 映射。 (ac76b4e)
    - [x] 使用绑定挂载（bind mount）将宿主机的 `./instance` 映射到容器内的 `/app/instance`。 (ac76b4e)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Docker Compose 配置' (Protocol in workflow.md) (7eb3c64)

## Phase 3: 部署与持久化验证 [checkpoint: 0607bb0]
- [x] Task: 重新构建并启动服务。 (b738187)
    - [x] 执行 `docker compose up --build -d` 以应用更改。 (b738187)
- [x] Task: 验证挂载配置。 (b738187)
    - [x] 运行 `docker inspect` 检查挂载点。 (b738187)
    - [x] 在容器内创建文件，确认宿主机对应目录同步。 (b738187)
- [x] Task: Conductor - User Manual Verification 'Phase 3: 部署与持久化验证' (Protocol in workflow.md) (0607bb0)
