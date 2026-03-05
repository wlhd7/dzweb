import pytest
from flask import url_for

def login_as_admin(client):
    with client.session_transaction() as sess:
        sess['is_admin'] = True

def test_admin_home_with_deprecated_case_endpoint(client, app):
    login_as_admin(client)
    
    # Mocking the apps database records including the problematic one
    from dzweb.db import get_db
    with app.app_context():
        db = get_db()
        # Clean up apps table for a clean test
        db.execute('DELETE FROM apps')
        db.execute('INSERT INTO apps (appname, appurl) VALUES (?, ?)', ('编辑案例', 'admin.edit_case'))
        db.commit()
    
    # This should NOT raise BuildError and should return 200 OK
    response = client.get('/admin/', follow_redirects=True)
    assert response.status_code == 200
    # Ensure the content is rendered
    assert b'\xe7\xbc\x96\xe8\xbe\x91\xe6\xa1\x88\xe4\xbe\x8b' in response.data # "编辑案例" in UTF-8
    
def test_admin_edit_case_redirect(client, app):
    login_as_admin(client)
    
    # Accessing the deprecated endpoint should redirect to case.main
    response = client.get('/admin/edit-case', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/case/')
