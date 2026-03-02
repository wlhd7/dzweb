import os
import pytest
from dzweb.db import get_db

def test_delete_product_removes_image(client, auth, app):
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        # Get the seeded product from conftest.py
        product = db.execute('SELECT id, filename FROM products WHERE productname = "Test Product"').fetchone()
        assert product is not None
        product_id = product['id']
        filename = product['filename']
        
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        # Verify file exists initially (created in conftest.py)
        assert os.path.exists(file_path)
        
        # Delete the product
        response = client.get(f'/product/{product_id}/delete', follow_redirects=True)
        assert response.status_code == 200
        assert "产品及其图片已成功删除。" in response.data.decode('utf-8')
        
        # Verify database record is gone
        deleted_product = db.execute('SELECT id FROM products WHERE id = ?', (product_id,)).fetchone()
        assert deleted_product is None
        
        # Verify physical file is gone
        assert not os.path.exists(file_path)

def test_delete_product_missing_file(client, auth, app):
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        # Add a new test product WITHOUT creating the physical file
        db.execute(
            "INSERT INTO products (productname, brief, category, filename, class) VALUES (?, ?, ?, ?, ?)",
            ('Missing File Product', 'Brief', 'automation', 'missing.jpg', 'engine')
        )
        product_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.commit()
        
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, 'missing.jpg')
        assert not os.path.exists(file_path)
        
        # Delete the product
        response = client.get(f'/product/{product_id}/delete', follow_redirects=True)
        assert response.status_code == 200
        
        # Verify database record is gone (it should still delete the DB record if file is already missing)
        deleted_product = db.execute('SELECT id FROM products WHERE id = ?', (product_id,)).fetchone()
        assert deleted_product is None

def test_delete_product_file_error(client, auth, app, monkeypatch):
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO products (productname, brief, category, filename, class) VALUES (?, ?, ?, ?, ?)",
            ('Error File Product', 'Brief', 'automation', 'error.jpg', 'engine')
        )
        product_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
        db.commit()
        
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, 'error.jpg')
        with open(file_path, 'wb') as f:
            f.write(b"data")
        
        # Mock os.remove to raise an exception
        def mock_remove(path):
            raise OSError("Permission denied")
        monkeypatch.setattr(os, "remove", mock_remove)
        
        # Delete the product
        response = client.get(f'/product/{product_id}/delete', follow_redirects=True)
        assert response.status_code == 200
        assert "删除图片文件失败，操作已取消。" in response.data.decode('utf-8')
        
        # Verify database record is STILL THERE
        product = db.execute('SELECT id FROM products WHERE id = ?', (product_id,)).fetchone()
        assert product is not None
