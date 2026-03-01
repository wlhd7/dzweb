# Track Specification - icp_filing_20260301

## Overview
This track involves adding the required ICP filing information (粤ICP备2026001637号) to the official website of Guangzhou Dongzhen Industrial Automation Co., Ltd. (dongzhen.cn). This is a regulatory requirement for all websites operating in mainland China.

## Functional Requirements
- **Display ICP Number**: Show "粤ICP备2026001637号" in the global footer of the website.
- **Hyperlink**: The ICP number must be clickable and link to the official MIIT website: https://beian.miit.gov.cn/.
- **Visibility**: The information must be visible on all pages, typically within the `base.html` template.
- **I18n**: Support translation for "粤ICP备2026001637号" if required, though the number itself is usually in Chinese. The label (if any) should be translatable.

## Non-Functional Requirements
- **Compliance**: Adhere to the Ministry of Industry and Information Technology (MIIT) regulations for website filing display.
- **Style**: Match the existing industrial/professional aesthetic of the site (as defined in `dzweb/static/css/base.css`).

## Acceptance Criteria
- [ ] "粤ICP备2026001637号" is clearly displayed in the footer of every page.
- [ ] Clicking the ICP number opens https://beian.miit.gov.cn/ in a new tab or the same tab.
- [ ] The footer layout remains consistent and responsive.
- [ ] The change is verified in both English and Japanese versions (if labels are added).

## Out of Scope
- Adding Public Security Filing (PSB) information (unless requested later).
- Redesigning the footer.
