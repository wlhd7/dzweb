import pytest
from dzweb.db import get_db

def test_hire_links_not_visible_for_guest(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO positions (position, salary, requirement) VALUES (?, ?, ?)",
            ('Test Position', 'Test Salary', 'Test Requirement')
        )
        db.commit()

    response = client.get('/human/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '编辑' not in html
    assert '删除' not in html

def test_hire_links_visible_for_admin(client, auth, app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO positions (position, salary, requirement) VALUES (?, ?, ?)",
            ('Test Position', 'Test Salary', 'Test Requirement')
        )
        db.commit()

    # Login as admin
    auth.admin_login()
    
    response = client.get('/human/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '编辑' in html
    assert '删除' in html
    assert 'href="/human/1/update-position"' in html
    assert 'href="/human/1/delete-position"' in html
