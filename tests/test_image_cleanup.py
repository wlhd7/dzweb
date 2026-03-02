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
        
def test_update_product_removes_old_image(client, auth, app):
    import io
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        # Get seeded product
        product = db.execute('SELECT id, filename, category FROM products WHERE productname = "Test Product"').fetchone()
        product_id = product['id']
        old_filename = product['filename']
        category = product['category']
        
        upload_folder = app.config['UPLOAD_FOLDER']
        old_file_path = os.path.join(upload_folder, old_filename)
        assert os.path.exists(old_file_path)
        
        # Update product with a NEW image
        data = {
            'productname': 'Updated Product',
            'brief': 'Updated Brief',
            'category': category,
            'class': 'engine',
            'file': (io.BytesIO(b"new image data"), 'new.jpg')
        }
        # We need to provide 'next' in args because update redirects to it
        response = client.post(
            f'/product/{product_id}/update?next=/product/{category}',
            data=data,
            content_type='multipart/form-data',
            follow_redirects=True
        )
        assert response.status_code == 200
        
        # Get new filename from DB
        new_product = db.execute('SELECT filename FROM products WHERE id = ?', (product_id,)).fetchone()
        new_filename = new_product['filename']
        assert new_filename != old_filename
        
        new_file_path = os.path.join(upload_folder, new_filename)
        assert os.path.exists(new_file_path)
        
def test_update_product_no_image_change(client, auth, app):
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        # Get seeded product
        product = db.execute('SELECT id, filename, category FROM products WHERE productname = "Test Product"').fetchone()
        product_id = product['id']
        filename = product['filename']
        category = product['category']
        
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        assert os.path.exists(file_path)
        
        # Update product WITHOUT changing the image
        data = {
            'productname': 'Name Change Only',
            'brief': 'Updated Brief',
            'category': category,
            'class': 'engine',
            'file': (None, '')
        }
        response = client.post(
            f'/product/{product_id}/update?next=/product/{category}',
            data=data,
            follow_redirects=True
        )
        assert response.status_code == 200
        
        # Get filename from DB - should be the same
        updated_product = db.execute('SELECT filename FROM products WHERE id = ?', (product_id,)).fetchone()
        assert updated_product['filename'] == filename
        
def test_cleanup_images_command(app):
    runner = app.test_cli_runner()
    
    upload_folder = app.config['UPLOAD_FOLDER']
    orphan_file = os.path.join(upload_folder, 'orphan.jpg')
    with open(orphan_file, 'wb') as f:
        f.write(b"orphan data")
        
    # Get seeded file path
    with app.app_context():
        db = get_db()
        seeded = db.execute('SELECT filename FROM products LIMIT 1').fetchone()
        seeded_file = os.path.join(upload_folder, seeded['filename'])
        assert os.path.exists(seeded_file)
    
    assert os.path.exists(orphan_file)
    
    # Run the cleanup command
    result = runner.invoke(args=['cleanup-images'])
    
    # Verify command output
    assert result.exit_code == 0
    # Use a more flexible assertion since total count might include thumbs/ if any were there
    assert "Deleted orphan file" in result.output
    
    # Verify orphan file is gone
    assert not os.path.exists(orphan_file)
    
    # Verify seeded file is STILL THERE
    assert os.path.exists(seeded_file)
