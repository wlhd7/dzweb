# dzweb SEO 配置与设置指南 (SEO Setup Guide)

本项目集成了针对百度、Bing 和 Google 的全方位 SEO 优化功能。为了使这些功能生效，您无需修改任何代码或 HTML 模板，只需在环境变量或 `.env` 文件中配置相应的标识符。

---

## 1. 关键参数配置 (Key Parameters)

请在您的 `.env` 文件中添加以下参数。系统在启动时会自动将这些值注入到页面元数据和脚本中。

| 平台 | 参数名称 | 环境变量 (Env Variable) | 说明 |
| :--- | :--- | :--- | :--- |
| **百度搜索资源平台** | 站点验证码 | `BAIDU_SITE_VERIFICATION` | 对应 `<meta name="baidu-site-verification">` |
| **百度搜索资源平台** | 推送令牌 | `BAIDU_PUSH_TOKEN` | 用于 API 自动提交新页面 URL |
| **百度统计** | 统计 ID | `BAIDU_TONGJI_ID` | 对应 `hm.js?` 后的哈希串 |
| **Bing Webmaster** | 站点验证码 | `BING_SITE_VERIFICATION` | 对应 `<meta name="msvalidate.01">` |
| **Google Console** | 站点验证码 | `GOOGLE_SITE_VERIFICATION` | 对应 `<meta name="google-site-verification">` |

---

## 2. 获取路径说明

### A. 百度搜索资源平台 (Baidu)
1.  **站点验证**：登录 [百度搜索资源平台](https://ziyuan.baidu.com/)，添加站点后选择“HTML标签验证”，复制 `content` 属性中的值。
2.  **自动推送**：进入“普通收录” -> “API提交”，在接口地址中获取 `token=xxxxxx`。

### B. 百度统计 (Baidu Tongji)
1.  登录 [百度统计](https://tongji.baidu.com/)，在“代码获取”中找到脚本地址 `hm.js?xxxxxxxx`，记录该 ID。

### C. Bing & Google
- **Bing**: 在 [Bing Webmaster Tools](https://www.bing.com/webmasters/) 中获取验证 Meta 标签的值。
- **Google**: 在 [Google Search Console](https://search.google.com/search-console) 中获取 `google-site-verification` 的值。

---

## 3. 自动化 SEO 功能

系统已默认启用以下功能，无需额外配置：

1.  **动态 Sitemap**: 访问 `/sitemap.xml` 即可获取全站（含多语言版本）的最新 URL 地图。
2.  **主动提交**: 管理员在后台每新增一个产品，系统会立即自动调用百度推送接口，提交该产品的三个语言版本（中、英、日）URL。
3.  **结构化数据 (JSON-LD)**: 全站自动生成符合 Schema.org 标准的 Organization 和 WebSite 结构化数据，提升搜索结果展现效果。
4.  **多语言关联**: 自动在 `<head>` 中插入 `hreflang` 标签，引导搜索引擎正确索引各语言版本。

---

## 4. 验证与排查

配置完成后，您可以：
1.  **查看源码**: 检查页面头部是否已正确填充对应的验证码和统计 ID。
2.  **检查日志**: 在后台新增产品后，查看服务器日志确认“Baidu Push Response”是否返回成功。
