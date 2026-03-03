import pytest
from dzweb.db import get_db

def test_case_tables_exist(app):
    with app.app_context():
        db = get_db()
        # Check case_modules table
        cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='case_modules'")
        assert cursor.fetchone() is not None
        
        # Check case_contents table
        cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='case_contents'")
        assert cursor.fetchone() is not None

def test_case_modules_schema(app):
    with app.app_context():
        db = get_db()
        cursor = db.execute("PRAGMA table_info(case_modules)")
        columns = {row['name']: row['type'] for row in cursor.fetchall()}
        assert 'id' in columns
        assert 'slug' in columns
        assert 'title_zh' in columns
        assert 'title_en' in columns
        assert 'title_ja' in columns
        assert 'created' in columns

def test_case_contents_schema(app):
    with app.app_context():
        db = get_db()
        cursor = db.execute("PRAGMA table_info(case_contents)")
        columns = {row['name']: row['type'] for row in cursor.fetchall()}
        assert 'id' in columns
        assert 'case_id' in columns
        assert 'type' in columns
        assert 'content_zh' in columns
        assert 'content_en' in columns
        assert 'content_ja' in columns
        assert 'filename' in columns
        assert 'sort_order' in columns

from dzweb.db import (
    get_case_modules, get_case_module_by_slug, create_case_module,
    update_case_module, delete_case_module, get_case_contents,
    add_case_content, update_case_content, delete_case_content
)

def test_case_module_crud(app):
    with app.app_context():
        # Create
        create_case_module('test-slug', '测试标题', 'Test Title', 'テストタイトル')
        
        # Read (All)
        modules = get_case_modules()
        assert len(modules) >= 1
        assert any(m['slug'] == 'test-slug' for m in modules)
        
        # Read (By Slug)
        module = get_case_module_by_slug('test-slug')
        assert module['title_zh'] == '测试标题'
        module_id = module['id']
        
        # Update
        update_case_module(module_id, 'updated-slug', '更新标题')
        module = get_case_module_by_slug('updated-slug')
        assert module['title_zh'] == '更新标题'
        
        # Delete
        delete_case_module(module_id)
        assert get_case_module_by_slug('updated-slug') is None

def test_case_content_crud(app):
    with app.app_context():
        create_case_module('test-content', '测试内容')
        module = get_case_module_by_slug('test-content')
        module_id = module['id']
        
        # Add Text Content
        add_case_content(module_id, 'text', content_zh='测试文本', sort_order=1)
        # Add Image Content
        add_case_content(module_id, 'image', filename='test.jpg', sort_order=2)
        
        # Read
        contents = get_case_contents(module_id)
        assert len(contents) == 2
        assert contents[0]['type'] == 'text'
        assert contents[1]['type'] == 'image'
        
        content_id = contents[0]['id']
        # Update
        update_case_content(content_id, 'text', content_zh='更新文本', sort_order=1)
        contents = get_case_contents(module_id)
        assert contents[0]['content_zh'] == '更新文本'
        
        # Delete
        delete_case_content(content_id)
        contents = get_case_contents(module_id)
        assert len(contents) == 1
