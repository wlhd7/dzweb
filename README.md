# dzweb: Guangzhou Dongzhen Official Website

广州东振机电设备有限公司官方网站 (GuangZhou DongZhen M&E Equipment Co., Ltd.).

## Overview (项目概览)
本项目基于 Flask 框架开发，旨在为广州东振提供一站式的内外部门户解决方案。系统涵盖了产品展示（支持自动缩略图生成）、人才招聘、多语言国际化支持、图片资源自动清理以及内部办公应用集成。

## Project Structure (项目结构)
```text
dzweb/
├── routes/          # API & Web 路由模块 (Blueprints)
├── static/          # 静态资源 (CSS, Images, Uploads)
│   └── uploads/
│       └── thumbs/  # Generated product thumbnails
├── templates/       # Jinja2 HTML 模板
├── utils/           # 图像处理与通用工具
├── translations/    # I18n 翻译文件 (zh/en/ja)
├── db.py            # SQLite 数据库操作
├── lang.py          # 语言选择逻辑
└── schema.sql       # 数据库初始结构
instance/            # 配置文件与数据库持久化
tests/               # 自动化测试用例
docker-compose.yml   # 容器编排配置
```

## Tech Stack (技术栈)
- **Framework**: Flask 3.1.2 (Python)
- **Database**: SQLite (Users, Products, Messages, Positions)
- **Frontend**: Jinja2 + Vanilla CSS + SVG Icons
- **Image Processing**: Pillow (Resizing & Optimization)
- **I18n**: Flask-Babel (Supports Chinese, English, Japanese)
- **Infrastructure**: Docker + Gunicorn + Nginx

## Getting Started (快速开始)

### Production Startup (生产环境启动 - 推荐)
在服务器上部署时，请遵循以下完整步骤：

1. **克隆项目并进入目录**:
   ```bash
   git clone <repository_url>
   cd dzweb
   ```

2. **配置环境变量**:
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，设置 SECRET_KEY, DZWEB_ADMIN_PASSWORD 及邮件/SEO 参数
   nano .env 
   ```

3. **构建并启动容器**:
   ```bash
   docker compose up -d --build
   ```

4. **初始化数据库 (关键步骤)**:
   首次启动或重置环境时必须执行，否则会返回 500 错误：
   ```bash
   docker exec -it dzweb-web-1 flask init-db
   ```

5. **编译翻译文件**:
   确保多语言功能正常显示：
   ```bash
   docker exec -it dzweb-web-1 pybabel compile -d dzweb/translations
   ```

6. **访问应用**:
   - 访问地址: `http://<your-server-ip>:5000`

### Development Setup (开发环境配置)
... (保持原有内容或微调)
1. **Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Run Server**:
   ```bash
   flask --app dzweb run --debug
   ```

## Key Commands
- **I18n Update**:
  ```bash
  pybabel extract -F babel.cfg -k _l -o messages.pot .
  pybabel update -i messages.pot -d dzweb/translations
  pybabel compile -d dzweb/translations
  ```

- **Maintenance CLI (运维指令)**:
  Clean up orphan image files:
  ```bash
  flask cleanup-images
  ```

- **SEO Tools**:
  - `dzweb/static/sitemap.xml`: Auto-generated sitemap.
  - `dzweb/static/robots.txt`: Search engine indexing control.

## License
Refer to `LICENSE.txt` for details.
