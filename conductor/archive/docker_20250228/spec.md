# Specification - docker_20250228

## 目标
为 dzweb 项目实现一个本地 Docker 开发环境，支持热重载和 SQLite 持久化。

## 背景
目前项目依赖本地 Python 环境，使用 Docker 可以统一开发环境并简化部署流程。

## 功能需求
- **Dockerfile**: 包含 Python 3.8+、Flask、gunicorn 及其依赖。
- **docker-compose.yml**: 协调应用和任何未来服务，挂载源代码卷实现热重载。
- **环境配置**: 支持通过环境变量配置关键参数。