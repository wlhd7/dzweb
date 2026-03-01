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
