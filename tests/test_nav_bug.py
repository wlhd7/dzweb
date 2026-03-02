import pytest

def test_index_page_icons(client):
    """首页顶级产品分类应使用大类图标（虚线箭头）"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # 检查首页“非标零件”图标
    assert 'static/images/arrow-narrow-right-dashed.svg' in html
    # 检查首页“子类别”图标
    assert 'static/images/corner-down-right.svg' in html

def test_about_page_icons_bug(client):
    """验证关于我们页面顶级产品分类使用了错误的图标（Bug 复现）"""
    response = client.get('/introduction')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # 我们期望顶级分类“非标零件”使用虚线箭头，但目前 main.html 硬编码了弯箭头
    # 修复前的测试：断言虚线箭头存在（这应该失败）
    assert 'static/images/arrow-narrow-right-dashed.svg' in html, "Top level category should use dashed arrow icon"
