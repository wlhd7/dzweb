import pytest
from dzweb.db import get_db

def test_all_apps_shown_in_sidebar_automatically(client, auth, app):
    auth.login()
    # Access a user page (e.g., userhome)
    response = client.get('/user/set-color')
    assert response.status_code == 200
    
    # Currently, this should FAIL to find the apps if applist is empty
    # Since the requirement is that ALL apps are shown automatically,
    # our goal is to make this PASS eventually.
    html = response.data.decode('utf-8')
    assert 'App 1' in html
    assert 'App 2' in html
