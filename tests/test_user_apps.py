import pytest
from dzweb.db import get_db

def test_all_apps_shown_in_sidebar_automatically(client, auth, app):
    auth.admin_login()
    # Access a user page (e.g., userhome)
    response = client.get('/user/')
    assert response.status_code == 200
    
    # Currently, this should FAIL to find the apps if applist is empty
    # Since the requirement is that ALL apps are shown automatically,
    # our goal is to make this PASS eventually.
    html = response.data.decode('utf-8')
    assert 'App 1' in html
    assert 'App 2' in html
def test_add_app_route_is_removed(client, auth):
    auth.admin_login()
    response = client.get('/user/add-app')
    assert response.status_code == 404

def test_index_page_renders(client):
    response = client.get('/')
    assert response.status_code == 200

def test_sidebar_links_are_correct(client, auth):
    auth.admin_login()
    response = client.get('/user/')
    html = response.data.decode('utf-8')
    assert 'href="/user/"' in html
    assert 'href="/user/edit-product"' in html

def test_userhome_form_is_removed(client, auth):
    auth.admin_login()
    response = client.get('/user/')
    html = response.data.decode('utf-8')
    assert 'name="number"' not in html
    assert 'name="password"' not in html
    assert '欢迎回来' in html
