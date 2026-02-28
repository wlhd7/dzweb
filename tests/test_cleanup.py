import pytest

def test_set_color_is_removed(client, auth):
    auth.admin_login()
    response = client.get('/user/set-color')
    assert response.status_code == 404

def test_weekend_overtime_is_removed(client, auth):
    auth.admin_login()
    response = client.get('/user/weekend-overtime')
    assert response.status_code == 404
