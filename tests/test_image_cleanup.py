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
        
        # Verify database record is gone
        deleted_product = db.execute('SELECT id FROM products WHERE id = ?', (product_id,)).fetchone()
        assert deleted_product is None
        
        # Verify physical file is gone (This is expected to FAIL currently)
        assert not os.path.exists(file_path), f"File {file_path} should have been deleted"
