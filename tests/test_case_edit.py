import pytest
from dzweb.db import get_db, create_case_module, get_case_module_by_slug, add_case_content, get_case_contents
import os
import io

def login_as_admin(client):
    with client.session_transaction() as sess:
        sess['is_admin'] = True

def test_update_case_module_title_and_slug_api(client, app):
    login_as_admin(client)
    with app.app_context():
        create_case_module('old-slug', '旧标题')
        module = get_case_module_by_slug('old-slug')
        module_id = module['id']
    
    # Update title to something that results in a new slug
    response = client.post(f'/case/api/module/{module_id}/update', data={
        'title_zh': '新的测试案例'
    }, follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert 'slug' in data
    
    with app.app_context():
        db = get_db()
        updated_module = db.execute('SELECT * FROM case_modules WHERE id = ?', (module_id,)).fetchone()
        assert updated_module['title_zh'] == '新的测试案例'
        # Check if slug is different (not 'old-slug')
        assert updated_module['slug'] != 'old-slug'
        assert updated_module['slug'] == data['slug']

def test_update_case_text_content_api(client, app):
    login_as_admin(client)
    with app.app_context():
        create_case_module('text-edit-test', '内容编辑测试')
        module = get_case_module_by_slug('text-edit-test')
        module_id = module['id']
        add_case_content(module_id, 'text', content_zh='原文字', sort_order=1)
        content_id = get_case_contents(module_id)[0]['id']
    
    # Update text content
    response = client.post(f'/case/api/content/{content_id}/update', data={
        'content_zh': '新文字'
    }, follow_redirects=True)
    # This should fail because the route doesn't exist yet
    assert response.status_code == 200
    
    with app.app_context():
        contents = get_case_contents(module_id)
        assert contents[0]['content_zh'] == '新文字'

def test_update_case_image_content_api_cleanup(client, app):
    login_as_admin(client)
    from dzweb.db import create_case_module, get_case_module_by_slug, add_case_content, get_case_contents
    with app.app_context():
        create_case_module('img-cleanup-test', '图片清理测试')
        module = get_case_module_by_slug('img-cleanup-test')
        module_id = module['id']
        old_filename = 'old-case.jpg'
        add_case_content(module_id, 'image', filename=old_filename, sort_order=1)
        content_id = get_case_contents(module_id)[0]['id']
        
        # Create dummy old files
        old_path = os.path.join(app.config['UPLOAD_FOLDER'], old_filename)
        old_webp = os.path.join(app.config['UPLOAD_FOLDER'], 'old-case.webp')
        os.makedirs(os.path.dirname(old_path), exist_ok=True)
        with open(old_path, 'w') as f: f.write('old')
        with open(old_webp, 'w') as f: f.write('old')
        assert os.path.exists(old_path)

    # Update image
    data = {
        'file': (io.BytesIO(b"new image data"), 'new-case.jpg'),
    }
    response = client.post(f'/case/api/content/{content_id}/update', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    
    assert not os.path.exists(old_path)
    assert not os.path.exists(old_webp)
    
    with app.app_context():
        contents = get_case_contents(module_id)
        assert contents[0]['filename'] != old_filename

def test_case_edit_permission_required(client, app):
    # Ensure non-admin cannot access update API
    with app.app_context():
        create_case_module('auth-test', '未授权测试')
        module = get_case_module_by_slug('auth-test')
        module_id = module['id']
    
    response = client.post(f'/case/api/module/{module_id}/update', data={'title_zh': '尝试更新'})
    # Should redirect to login
    assert response.status_code == 302
    assert '/admin/login' in response.location
    
    # Try updating content
    response = client.post('/case/api/content/1/update', data={'content_zh': '尝试更新'})
    assert response.status_code == 302
