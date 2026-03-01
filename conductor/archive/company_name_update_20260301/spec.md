# Track Specification: Global Company Name Update

## 概述 (Overview)
将全站的公司名称从“广州东振工业自动化有限公司”统一修改为“广州东振机电设备有限公司”，并同步更新对应的英文名称为“GuangZhou DongZhen M&E Equipment Co., Ltd”。此更改涉及前端显示、SEO 元数据、结构化数据以及内部项目文档。

## 功能需求 (Functional Requirements)

### 1. 全局名称替换 (Global Text Update)
- **中文名称**：广州东振机电设备有限公司
- **英文名称**：GuangZhou DongZhen M&E Equipment Co., Ltd
- **日文名称**：広州東振機電設備有限公司

### 2. 多语言支持 (i18n Implementation)
- 优先更新 `dzweb/translations/` 目录下的 `.po` 文件，确保 `{{ _('广州东振工业自动化有限公司') }}` 等调用指向新名称。
- 检查并替换模板中可能存在的硬编码公司名称字符串。

### 3. SEO 与元数据优化 (SEO & Meta Tags)
- 更新 `base.html` 中的 `meta description`、`keywords` 和 `og:title` 等包含公司名的字段。
- 更新 `instance/config.py`（如有）中的站点验证或相关配置。

### 4. 结构化数据更新 (Structured Data)
- 更新 `base.html` 中的 JSON-LD 脚本，确保 `Organization` 类型的 `name` 属性反映新公司名。

### 5. 项目文档同步 (Documentation Sync)
- 同步修改 `conductor/product.md`、`PRD.md` 以及 `SEO_SETUP_GUIDE.md` 等文档。

## 非功能需求 (Non-Functional Requirements)
- **一致性**：确保全站（中/英/日）在所有可见位置的名称高度统一。
- **不可破坏性**：更改不应影响现有的路由、功能逻辑或数据库结构。

## 验收标准 (Acceptance Criteria)
- [ ] 首页页脚（Footer）显示新公司名。
- [ ] 浏览器标签页标题（Title）显示新公司名。
- [ ] 源代码中的 Meta 标签及 JSON-LD 数据显示新公司名。
- [ ] 切换语言至英文时，显示“GuangZhou DongZhen M&E Equipment Co., Ltd”。
- [ ] 所有 Conductor 项目文档已完成同步。

## 超出范围 (Out of Scope)
- 包含旧名称的旧图片素材修改（如 Logo 内部文字）。
- 法律层面的工商变更登记或外部第三方平台的资料修改（由用户手动处理）。
