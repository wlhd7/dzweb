import pytest

def test_user_home_link_in_nav(client, auth):
    auth.login()
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '主页' in html
