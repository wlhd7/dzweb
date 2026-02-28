# Tech Stack - dzweb

## 核心技术
- **编程语言**: Python 3.8+ (后端逻辑处理)
- **后端框架**: Flask 3.1.2 (轻量级 Web 框架)
- **前端技术**: Jinja2 Templates + Vanilla CSS (原生 CSS，无需 Tailwind 或其他框架) + SVG 图标
- **数据库**: SQLite (轻量级关系型数据库，用于存储用户、产品和消息)

## 关键库与集成
- **国际化 (I18n)**: Flask-Babel 4.0.0 (支持中、英、日三种语言切换)
- **安全**: 基于环境变量的预设密码认证 (通过 `ADMIN_PASSWORD` 环境变量配置)
- **邮件服务**: Flask-Mail (用于处理系统邮件发送)

## 生产与部署 (Production & Deployment)
- **容器化**: **Docker** (使用 Docker 容器化整个应用环境，确保开发与生产环境的一致性)
- **WSGI 服务器**: Gunicorn (作为容器内的 Web 服务器网关接口)
- **反向代理**: Nginx (推荐用于处理 HTTPS、静态资源缓存和负载均衡)

## 开发工具
- **版本控制**: Git
- **依赖管理**: pip (通过 `requirements.txt` 或 `pyproject.toml` 管理)