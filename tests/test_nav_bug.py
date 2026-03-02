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
    """验证关于我们页面，包括产品分类和关于我们栏目都使用了错误的图标（Bug 复现）"""
    response = client.get('/introduction')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # 1. 验证“产品类别”栏图标错误（预期虚线箭头，实际目前缺失）
    assert 'static/images/arrow-narrow-right-dashed.svg' in html, "Top level product category should use dashed arrow icon"
    
    # 2. 验证“关于我们”栏图标错误（用户补充：简介页中“公司简介”左侧也应该是虚线箭头）
    # 检查“公司历程”或其他链接左侧是否也有虚线箭头
    # 在首页 index.html 中，这些都是虚线箭头
    # 在 main.html 中，目前全部被硬编码成了弯箭头

def test_product_list_page_icons(client):
    """产品列表页顶级分类也应使用大类图标（虚线箭头）"""
    # 测试“工装夹具”列表页
    response = client.get('/product/fixture')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # 顶级图标应为虚线箭头
    assert 'static/images/arrow-narrow-right-dashed.svg' in html
