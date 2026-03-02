# 生产环境部署与运维手册 (Production Deployment & Operations)

本手册整合了 **广州东振机电设备有限公司** 官网 (dzweb) 在生产环境下所需的所有配置、环境变量及运维指令。

---

## 1. 环境变量配置 (Environment Variables)

本项目支持通过项目根目录下的 `.env` 文件自动加载环境变量。

### 1.1 快速开始
1.  复制模板：`cp .env.example .env`
2.  修改 `.env` 中的参数：
    ```bash
    nano .env
    ```

### 1.2 核心基础配置 (Core)
| 变量名 | 说明 | 示例值 |
| :--- | :--- | :--- |
| `FLASK_APP` | Flask 入口模块 | `dzweb` |
| `FLASK_DEBUG` | 调试模式 (生产环境必须为 0) | `0` |
| `SECRET_KEY` | Session 加密密钥 | `随机长字符串` |
| `DZWEB_ADMIN_PASSWORD` | 管理员登录唯一密码 | `******` |

### 1.2 邮件服务器配置 (SMTP - 用于客户反馈)
| 变量名 | 说明 | 示例值 |
| :--- | :--- | :--- |
| `MAIL_SERVER` | SMTP 服务器地址 | `smtp.exmail.qq.com` |
| `MAIL_PORT` | SMTP 端口 (通常 465 或 587) | `465` |
| `MAIL_USE_TLS` | 是否使用 TLS | `False` |
| `MAIL_USE_SSL` | 是否使用 SSL | `True` |
| `MAIL_USERNAME` | 发件箱账号 | `noreply@dongzhen.cn` |
| `MAIL_PASSWORD` | 发件箱授权码/密码 | `******` |
| `MAIL_DEFAULT_SENDER` | 默认发件人名称 | `广州东振官网 <noreply@dongzhen.cn>` |
| `MAIL_ADMIN` | 接收反馈的管理员邮箱 | `info@dongzhen.cn` |

### 1.3 SEO 增强配置 (SEO)
| 变量名 | 说明 | 示例值 |
| :--- | :--- | :--- |
| `BAIDU_PUSH_TOKEN` | 百度主动推送 API Token | `******` |
| `BAIDU_SITE_VERIFICATION` | 百度站长工具验证码 | `code-123` |
| `BAIDU_TONGJI_ID` | 百度统计 ID | `hash-id` |
| `BING_SITE_VERIFICATION` | Bing Webmaster 验证码 | `ms-code-123` |
| `GOOGLE_SITE_VERIFICATION` | Google Search Console 验证码 | `google-code-123` |

---

## 2. 容器化部署 (Docker Deployment)

### 2.1 启动服务
使用 Docker Compose 启动生产环境：
```bash
# 构建并以后台模式启动
docker compose up -d --build
```

### 2.2 目录持久化 (Volumes)
确保宿主机上存在以下目录，以便在容器重启后保留数据：
- `./instance/`: 存放 SQLite 数据库 (`dzweb.sqlite`)。
- `./dzweb/static/uploads/`: 存放上传的产品原始图片及缩略图 (`thumbs/`)。

---

## 3. 核心运维指令 (Operations CLI)

所有指令需在 **容器内** 执行。使用 `docker exec -it <container_name> <command>` 运行：

### 3.1 资源维护 (Resource Management)
- **清理孤儿文件** (移除数据库中不存在的物理图片)：
  ```bash
  docker exec -it dzweb-web-1 flask cleanup-images
  ```
- **批量生成缩略图** (修复缺失的缩略图)：
  ```bash
  docker exec -it dzweb-web-1 flask generate-thumbs
  ```

### 3.2 国际化翻译 (I18n)
- **编译翻译文件** (更新 `.po` 后必须执行此命令方能生效)：
  ```bash
  docker exec -it dzweb-web-1 pybabel compile -d dzweb/translations
  ```

### 3.3 数据库初始化 (Database)
- **重置数据库** (仅在首次部署或清空数据时使用，**慎用**)：
  ```bash
  docker exec -it dzweb-web-1 flask init-db
  ```

---

## 4. 日志审计 (Logging)

- **查看实时日志**：
  ```bash
  docker compose logs -f web
  ```
- **持久化日志位置**：
  日志文件存储在 `instance/logs/` 目录下（如已挂载卷，可在宿主机查看）。

---

## 5. 验收清单 (Checklist)
- [ ] `FLASK_DEBUG` 已设为 `0`。
- [ ] 已在百度搜索资源平台验证站点并获取 `BAIDU_PUSH_TOKEN`。
- [ ] 通过联系页面发送测试留言，确认 `MAIL_ADMIN` 能收到邮件。
- [ ] 检查 `dzweb/static/sitemap.xml` 确认已包含所有产品页面。
