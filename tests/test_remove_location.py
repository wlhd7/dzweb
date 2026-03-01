import pytest
import os

def test_location_route_redirects_to_contact_us(client):
    """验证 /contact/location 路由返回 301 重定向到 /contact/。"""
    response = client.get('/contact/location', follow_redirects=False)
    assert response.status_code == 301
    assert response.headers['Location'].endswith('/contact/')

def test_location_route_followed_redirect_works(client):
    """验证跟随重定向后返回 200 OK。"""
    response = client.get('/contact/location', follow_redirects=True)
    assert response.status_code == 200
    assert '联系我们' in response.data.decode('utf-8') or 'Contact Us' in response.data.decode('utf-8') or 'お問い合わせ' in response.data.decode('utf-8')

def test_location_link_not_in_main_contact_page(client):
    """验证 contact 首页中不再包含指向 location 的链接。"""
    response = client.get('/contact/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'contact.location' not in html
    assert '/contact/location' not in html

def test_location_not_in_dynamic_sitemap(client):
    """验证动态生成的 sitemap.xml 中不再包含 /contact/location。"""
    response = client.get('/sitemap.xml')
    assert response.status_code == 200
    xml = response.data.decode('utf-8')
    assert '/contact/location' not in xml

def test_location_not_in_static_sitemap():
    """验证静态 static/sitemap.xml 中不再包含 /contact/location。"""
    sitemap_path = 'dzweb/static/sitemap.xml'
    with open(sitemap_path, 'r', encoding='utf-8') as f:
        xml = f.read()
    assert '/contact/location' not in xml
