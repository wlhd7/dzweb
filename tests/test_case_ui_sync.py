import pytest
from dzweb.db import get_db

def test_case_sidebar_normalization(client, app):
    """验证案例侧边栏包含图标和 hr 分隔线"""
    # 确保至少有一个案例
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO case_modules (title_zh, slug) VALUES ('Test Case', 'test-case')")
        db.commit()

    response = client.get('/case/', follow_redirects=True)
    html = response.data.decode('utf-8')
    
    # 验证是否包含虚线箭头图标
    assert 'arrow-narrow-right-dashed.svg' in html
    assert 'class="nav-top-icon-dashed"' in html
    
    # 验证是否包含 hr 分隔线
    assert '<hr>' in html
    
    # 验证是否移除了内联样式 (一部分)
    assert 'style="list-style: none; padding: 10px; margin: 0;"' not in html

def test_case_display_sidebar_normalization(client, app):
    """验证案例详情页侧边栏包含图标和 hr 分隔线"""
    # 确保至少有一个案例
    with app.app_context():
        db = get_db()
        db.execute("INSERT INTO case_modules (title_zh, slug) VALUES ('Test Case 2', 'test-case-2')")
        db.commit()

    response = client.get('/case/test-case-2', follow_redirects=True)
    html = response.data.decode('utf-8')
    
    assert 'arrow-narrow-right-dashed.svg' in html
    assert 'class="nav-top-icon-dashed"' in html
    assert '<hr>' in html
