# dzweb SEO 配置与设置指南 (SEO Setup Guide)

本项目已集成了针对百度、Bing 和 Google 的 SEO 优化功能。为了使这些功能完全生效，您需要登录各平台获取相应的标识符（ID）和令牌（Token），并按照以下说明进行配置。

---

## 1. 关键参数概览 (Key Parameters)

请核对以下参数，并根据实际获取的值替换代码中的占位符。

| 平台 | 参数名称 | 代码中的位置 | 当前状态/值 |
| :--- | :--- | :--- | :--- |
| **百度搜索资源平台** | 站点验证 (Verification) | `dzweb/templates/base.html` | `codeva-itXnARhqFg` |
| **百度搜索资源平台** | 主动推送 Token (Push Token) | 环境变量 `BAIDU_PUSH_TOKEN` | 待配置 |
| **百度统计** | 统计 ID (Tongji ID) | `dzweb/templates/base.html` | `4D6C42588102B9D9E16C829B2783F992` |
| **Bing Webmaster** | 站点验证 (Verification) | `dzweb/templates/base.html` | `4D6C42588102B9D9E16C829B2783F992` |
| **Google Console** | 站点验证 (Verification) | `dzweb/templates/base.html` | `lHyC4DgQqSdtHbM0WgYfWyxVpKyDvFq5DnE8DtjlL4k` |

---

## 2. 获取路径与操作说明

### A. 百度搜索资源平台 (Baidu Search Resource Platform)
1.  **站点验证**：
    - 登录 [百度搜索资源平台](https://ziyuan.baidu.com/)。
    - 进入“用户中心” -> “站点管理” -> 添加 `https://www.dongzhen.cn`。
    - 选择“HTML标签验证”，复制 `content` 属性中的字符串，替换 `base.html` 中的验证代码。
2.  **主动推送 API**：
    - 进入“资源运营” -> “普通收录” -> “资源提交” -> “API提交”。
    - 在接口调用地址中找到 `token=xxxxxx`，这个 `xxxxxx` 就是您的 **BAIDU_PUSH_TOKEN**。

### B. 百度统计 (Baidu Tongji)
1.  登录 [百度统计](https://tongji.baidu.com/)。
2.  进入“管理” -> “代码获取”。
3.  找到代码中的 `hm.js?xxxxxxxx`，`xxxxxxxx` 后的字符串即为统计 ID。
4.  更新 `base.html` 结尾处的脚本 ID。

### C. Bing & Google 站长工具
- **Bing**: 登录 [Bing Webmaster Tools](https://www.bing.com/webmasters/) 获取 `msvalidate.01`。
- **Google**: 登录 [Google Search Console](https://search.google.com/search-console) 获取 `google-site-verification`。

---

## 3. 安全配置建议

### 环境变量设置 (Environment Variables)
为了安全起见，**主动推送 Token** 不应直接写在代码中。请在生产服务器的环境变量或 `.env` 文件中添加：

```bash
BAIDU_PUSH_TOKEN=您的百度推送Token
```

程序会自动通过 `os.environ.get('BAIDU_PUSH_TOKEN')` 读取该值。如果未配置此变量，程序会自动跳过推送步骤并记录警告日志，不会导致系统崩溃。

---

## 4. 已完成的自动化功能
- **动态 Sitemap**: 访问 `/sitemap.xml` 自动生成包含全站 URL（含中、英、日多语言版本）的地图。
- **自动推送**: 每次在后台“新增产品”成功后，系统会自动调用百度 API 推送该产品的 3 个语言版本 URL。
- **Hreflang 关联**: 全站页面已自动添加 `rel="alternate"` 标签，帮助搜索引擎识别多语言对应关系。
