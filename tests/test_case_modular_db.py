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
