import pytest
import os

def test_admin_login_success(client, auth, app):
    # This should fail initially because the login route still expects username
    response = auth.admin_login(password='test_admin_password')
    assert response.headers['Location'] == '/admin/'

def test_admin_login_fail(client, auth, app):
    response = auth.admin_login(password='wrong_password')
    assert response.status_code == 200 # Returns to login page with error
