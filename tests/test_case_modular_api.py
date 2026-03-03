import pytest
from flask import url_for, session

def login_as_admin(client, app):
    with client.session_transaction() as sess:
        sess['is_admin'] = True

def test_create_case_module_api(client, app):
    login_as_admin(client, app)
    response = client.post('/case/api/module', data={
        'slug': 'api-test',
        'title_zh': 'API测试',
        'title_en': 'API Test',
        'title_ja': 'APIテスト'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    from dzweb.db import get_case_module_by_slug
    with app.app_context():
        module = get_case_module_by_slug('api-test')
        assert module is not None
        assert module['title_zh'] == 'API测试'

def test_delete_case_module_api(client, app):
    login_as_admin(client, app)
    from dzweb.db import create_case_module, get_case_module_by_slug
    with app.app_context():
        create_case_module('to-delete', '删除测试')
        module = get_case_module_by_slug('to-delete')
        module_id = module['id']
    
    response = client.post(f'/case/api/module/{module_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        assert get_case_module_by_slug('to-delete') is None

def test_add_text_content_api(client, app):
    login_as_admin(client, app)
    from dzweb.db import create_case_module, get_case_module_by_slug, get_case_contents
    with app.app_context():
        create_case_module('content-test', '内容测试')
        module = get_case_module_by_slug('content-test')
        module_id = module['id']
    
    response = client.post(f'/case/api/module/{module_id}/content', data={
        'type': 'text',
        'content_zh': '一些测试文本',
        'sort_order': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        contents = get_case_contents(module_id)
        assert len(contents) == 1
        assert contents[0]['content_zh'] == '一些测试文本'

def test_reorder_content_api(client, app):
    login_as_admin(client, app)
    from dzweb.db import create_case_module, get_case_module_by_slug, add_case_content, get_case_contents
    with app.app_context():
        create_case_module('order-test', '排序测试')
        module = get_case_module_by_slug('order-test')
        module_id = module['id']
        add_case_content(module_id, 'text', content_zh='1', sort_order=1)
        add_case_content(module_id, 'text', content_zh='2', sort_order=2)
        contents = get_case_contents(module_id)
        c1_id = contents[0]['id']
        c2_id = contents[1]['id']
    
    # Swap orders: c1 down, c2 up
    response = client.post(f'/case/api/content/{c1_id}/move/down', follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        contents = get_case_contents(module_id)
        assert contents[0]['id'] == c2_id
        assert contents[1]['id'] == c1_id
