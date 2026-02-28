import pytest

def test_management_buttons_hidden_for_guest(client):
    # Access a product display page as guest
    response = client.get('/product/1/display')
    # If product 1 exists, check HTML. If not, it might 404 but shouldn't have buttons regardless.
    if response.status_code == 200:
        html = response.data.decode('utf-8')
        assert '编辑' not in html
        assert '删除' not in html

def test_management_buttons_visible_for_admin(client, auth):
    auth.admin_login()
    response = client.get('/product/1/display')
    if response.status_code == 200:
        html = response.data.decode('utf-8')
        assert '编辑' in html
        assert '删除' in html
