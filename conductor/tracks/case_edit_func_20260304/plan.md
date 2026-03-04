# Implementation Plan: Classic Case Edit Functionality

## Phase 1: Backend API Enhancement [checkpoint: b782c79]
- [x] Task: 实现 `api_update_module` 接口用于更新模块标题。 [2d490f7]
    - 在 `dzweb/routes/case.py` 中增加 `/api/module/<int:id>/update` 路由。
    - 使用 `@login_required`。
    - 仅更新 `title_zh`。（后更新为同时更新 `slug` [088b85e]）
- [x] Task: 实现 `api_update_content` 接口用于更新文案或图片。 [2d490f7]
    - 在 `dzweb/routes/case.py` 中增加 `/api/content/<int:id>/update` 路由。
    - 使用 `@login_required`。
    - 如果 `type='text'`，更新 `content_zh`。
    - 如果 `type='image'` 且上传了新文件：
        - 保存新图，生成缩略图和 WebP。
        - 物理删除旧文件（原图、缩略图、WebP）。
        - 更新 `filename`。
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md) [b782c79]

## Phase 2: Frontend UI Implementation [checkpoint: 5e804de]
- [x] Task: 在案例标题位置增加“编辑”功能。 [c5f9652]
    - 修改 `dzweb/templates/case/display.html`。
    - 添加 `edit-case-title-btn`。
    - 添加 `edit-case-title-modal`。
    - 编写对应 JS 提交逻辑。（后更新为支持新 Slug 重定向 [088b85e]）
- [x] Task: 为每个内容项（Text/Image）增加“编辑”功能。 [c5f9652]
    - 修改 `dzweb/templates/case/display.html`。
    - 在 `case-item-controls` 中添加 `edit-content-btn`。
    - 添加 `edit-text-modal` 和 `edit-image-modal`。
    - 编写对应 JS 逻辑：点击时将内容填充进 Modal，并处理表单提交。
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md) [5e804de]

## Phase 3: Final Verification & Cleanup [checkpoint: 3014f55]
- [x] Task: 编写自动化测试验证更新和文件清理逻辑。 [3014f55]
    - 创建 `tests/test_case_edit.py`。
    - 测试模块标题更新。
    - 测试文字内容更新。
    - 测试图片更新（重点验证物理文件是否被清理）。
- [x] Task: 运行所有现有测试并确保无回归。 [3014f55]
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md) [3014f55]
