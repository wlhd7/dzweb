import io
from unittest.mock import patch, MagicMock

import pytest
from flask import url_for

def test_seo_tags_in_base_template(client):
    """验证 base.html 中包含基本的 SEO 标签"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # 验证 canonical 标签
    assert 'rel="canonical"' in html
    
    # 验证 hreflang 标签
    assert 'rel="alternate" hreflang="zh"' in html
    assert 'rel="alternate" hreflang="en"' in html
    assert 'rel="alternate" hreflang="ja"' in html
    assert 'rel="alternate" hreflang="x-default"' in html

def test_seo_tdk_in_base_template(client):
    """验证 base.html 中包含 TDK 标签"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    assert '<title>' in html
    assert '<meta name="description"' in html
    assert '<meta name="keywords"' in html

def test_seo_baidu_tongji_in_base_template(client):
    """验证 base.html 中包含百度统计脚本"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    assert 'hm.baidu.com/hm.js' in html

def test_seo_verification_tags(client):
    """验证 base.html 中包含站长验证标签"""
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # 百度验证
    assert 'name="baidu-site-verification"' in html
    # Bing 验证
    assert 'name="msvalidate.01"' in html

def test_mobile_seo_meta_tags(client):
    """验证包含移动端 SEO 相关的 meta 标签"""
    response = client.get('/')
    html = response.data.decode('utf-8')
    
    assert 'name="viewport"' in html
    assert 'content="width=device-width, initial-scale=1.0"' in html
    # 百度移动适配
    assert 'name="applicable-device"' in html or 'handheld' in html or 'mobile' in html or 'format-detection' in html

def test_sitemap_xml(client):
    """验证 sitemap.xml 路由存在且内容正确"""
    response = client.get('/sitemap.xml')
    assert response.status_code == 200
    assert response.mimetype == 'application/xml'
    html = response.data.decode('utf-8')
    
    assert '<urlset' in html
    assert '<loc>' in html
    # 首页
    assert '/</loc>' in html or 'localhost' in html
    # 产品页
    assert '/product/' in html
    # 案例页
    assert '/case/' in html

@patch('dzweb.routes.product.push_to_baidu')
def test_baidu_push_on_product_create(mock_push, client, auth):
    """验证创建产品时触发百度推送"""
    # Create a dummy image
    img = (io.BytesIO(b"dummy image data"), 'test.jpg')
    
    auth.admin_login()
    
    data = {
        'productname': 'New SEO Product',
        'brief': 'SEO Brief',
        'category': 'automation',
        'file': img
    }
    
    # We need to simulate the file upload correctly
    response = client.post('/product/create', data=data, content_type='multipart/form-data')
    assert response.status_code == 302 # Redirect to category page
    
    assert mock_push.called
    urls = mock_push.call_args[0][0]
    # Check if any URL contains /product/ and lang=en/ja
    found_en = False
    found_ja = False
    for url in urls:
        if '/product/' in url and 'lang=en' in url:
            found_en = True
        if '/product/' in url and 'lang=ja' in url:
            found_ja = True
    assert found_en
    assert found_ja

def test_page_specific_tdk_home(client):
    """验证首页有特定的 TDK"""
    response = client.get('/')
    html = response.data.decode('utf-8')
    assert '首页' in html or 'Home' in html
    assert '工业自动化' in html

def test_page_specific_tdk_introduction(client):
    """验证公司简介页有特定的 TDK"""
    response = client.get('/introduction')
    html = response.data.decode('utf-8')
    assert '公司简介' in html or 'Introduction' in html
    assert '广州东振' in html

def test_page_specific_tdk_product_display(client):
    """验证产品详情页动态生成 TDK"""
    # Test Product was added in conftest.py
    response = client.get('/product/1/display')
    html = response.data.decode('utf-8')
    assert 'Test Product' in html
    assert 'Test Brief' in html
