import pytest
from flask import url_for
import unittest.mock as mock

def login_as_admin(client):
    with client.session_transaction() as sess:
        sess['is_admin'] = True

def test_create_module_without_slug_fallback(client, app):
    login_as_admin(client)
    
    # We want to ensure that even if slug is missing, it creates one.
    # Currently it would call auto_translate.
    # We will check if it still works after we remove the translator.
    response = client.post('/case/api/module', data={
        'title_zh': '新案例测试'
    })
    assert response.status_code == 200
    
    from dzweb.db import get_case_modules
    with app.app_context():
        modules = get_case_modules()
        # Find the one with title '新案例测试'
        module = next((m for m in modules if m['title_zh'] == '新案例测试'), None)
        assert module is not None
        # The slug should be generated from the title if not provided.
        # After our refactor, slugify('新案例测试') might result in '-' or similar if it only keeps a-z0-9.
        # But it should NOT be empty.
        assert module['slug'] != ''

def test_create_module_with_manual_slug(client, app):
    login_as_admin(client)
    
    response = client.post('/case/api/module', data={
        'title_zh': '手动Slug测试',
        'slug': 'manual-slug-123'
    })
    assert response.status_code == 200
    
    from dzweb.db import get_case_module_by_slug
    with app.app_context():
        module = get_case_module_by_slug('manual-slug-123')
        assert module is not None
        assert module['title_zh'] == '手动Slug测试'

def test_update_module_slug_manual(client, app):
    login_as_admin(client)
    
    from dzweb.db import create_case_module, get_case_module_by_slug
    with app.app_context():
        create_case_module('old-slug', '旧标题')
        module = get_case_module_by_slug('old-slug')
        module_id = module['id']
    
    # Update both title and slug
    response = client.post(f'/case/api/module/{module_id}/update', data={
        'title_zh': '新标题',
        'slug': 'new-slug-456'
    })
    assert response.status_code == 200
    
    with app.app_context():
        # Old slug should be gone or changed
        assert get_case_module_by_slug('old-slug') is None
        # New slug should exist
        module = get_case_module_by_slug('new-slug-456')
        assert module is not None
        assert module['title_zh'] == '新标题'
