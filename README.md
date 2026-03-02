# dzweb: Guangzhou Dongzhen Official Website

广州东振机电设备有限公司官方网站。

## Overview (项目概览)
本项目基于 Flask 框架开发，旨在为广州东振提供一站式的内外部门户解决方案。系统涵盖了产品展示、人才招聘、多语言国际化支持、图片资源自动清理以及内部办公应用集成。

## Tech Stack (技术栈)
- **Framework**: Flask 3.1.2 (Python)
- **Database**: SQLite (Relational storage for users, products, and messages)
- **Frontend**: Jinja2 Templates + Vanilla CSS + SVG Icons
- **I18n**: Flask-Babel (Supports Chinese, English, Japanese)
- **Infrastructure**: Gunicorn (WSGI Server) + Nginx (Production Proxy)

## Getting Started (快速开始)

### Prerequisites
- Python >= 3.8
- Virtual Environment (recommended)

### Installation
1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd dzweb
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Local Development

#### Using Docker (Recommended)
We use Docker and Docker Compose to provide a consistent development environment.

1. **Start the environment**:
   ```bash
   docker compose up -d
   ```

2. **Access the application**:
   The application will be available at [http://localhost:5000](http://localhost:5000).

3. **Hot-Reloading**:
   The code is mounted as a volume. Any changes made to the source code will automatically trigger a reload within the container.

4. **Stop the environment**:
   ```bash
   docker compose down
   ```

#### Traditional Installation (Legacy)
1. **Environment Config**:
   The app uses `instance/config.py` for sensitive settings (Mail, Secret Keys). Ensure `instance/` directory exists.

2. **Run the server**:
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
  Clean up orphan image files that are no longer referenced in the database:
  ```bash
  flask cleanup-images
  ```

## License
Refer to `LICENSE.txt` for details.
