# Implementation Plan: Restore Mailbox Success <p> Tag

## Phase 1: Implement Success Rendering Logic
- [ ] Task: 在 `dzweb/routes/contact.py` 的 `mailbox` 函数中，当邮件发送成功后（`if success:`），将 `render_template` 的返回值更新为 `render_template('contact/mailbox.html', success=True)`。
- [ ] Task: 修改 `dzweb/templates/contact/mailbox.html`，在 `</form>` 标签下方插入以下逻辑：
  ```html
  {% if success %}
  <p>{{ _('感谢您的反馈，我们会尽快处理！') }}</p>
  {% endif %}
  ```
- [ ] Task: 检查并提取翻译。运行 `pybabel extract` 和 `pybabel update`（如需要），确保新标签支持多语言显示。

## Phase 2: Verification
- [ ] Task: 更新现有测试 `tests/test_contact.py`，添加一个验证成功提交后，响应内容中包含“感谢您的反馈，我们会尽快处理！”且不使用 Flash 的断言。
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)
