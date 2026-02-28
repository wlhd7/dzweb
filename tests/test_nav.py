import pytest

def test_user_home_link_in_nav(client, auth):
    auth.admin_login()
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '管理后台' in html

def test_add_new_product_link_in_sidebar(client, auth):
    auth.admin_login()
    response = client.get('/product/fixture')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'href="/product/create"' in html
    assert '新增' in html
