import os
import io
import pytest
from PIL import Image
from dzweb.db import get_db

def create_test_image():
    file = io.BytesIO()
    image = Image.new('RGB', (800, 600), color='blue')
    image.save(file, 'jpeg')
    file.name = 'test.jpg'
    file.seek(0)
    return file

def test_create_product_generates_thumbnail(client, auth, app):
    auth.admin_login()
    
    test_img = create_test_image()
    data = {
        'productname': 'Thumbnail Test Product',
        'brief': 'Testing thumbnail generation',
        'category': 'automation',
        'class': 'engine',
        'file': (test_img, 'test.jpg')
    }
    
    response = client.post(
        '/product/create',
        data=data,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    assert response.status_code == 200
    
    with app.app_context():
        db = get_db()
        product = db.execute('SELECT filename FROM products WHERE productname = "Thumbnail Test Product"').fetchone()
        assert product is not None
        filename = product['filename']
        
        # Verify original image exists
        orig_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        assert os.path.exists(orig_path)
        
        # Verify thumbnail exists
        thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
        # This is expected to FAIL until implemented
        assert os.path.exists(thumb_path), f"Thumbnail not found at {thumb_path}"
        
        # Verify thumbnail size
        with Image.open(thumb_path) as thumb:
            assert thumb.size == (400, 300)

def test_update_product_generates_new_thumbnail_and_removes_old(client, auth, app):
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        # 1. Create a product first
        test_img1 = create_test_image()
        client.post('/product/create', data={
            'productname': 'Update Test',
            'brief': 'Initial',
            'category': 'automation',
            'class': 'engine',
            'file': (test_img1, 'img1.jpg')
        }, content_type='multipart/form-data')
        
        product = db.execute('SELECT id, filename FROM products WHERE productname = "Update Test"').fetchone()
        product_id = product['id']
        old_filename = product['filename']
        old_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], old_filename)
        assert os.path.exists(old_thumb_path)
        
        # 2. Update with NEW image
        test_img2 = create_test_image()
        client.post(f'/product/{product_id}/update?next=/product/automation', data={
            'productname': 'Update Test',
            'brief': 'Updated',
            'category': 'automation',
            'class': 'engine',
            'file': (test_img2, 'img2.jpg')
        }, content_type='multipart/form-data')
        
        new_product = db.execute('SELECT filename FROM products WHERE id = ?', (product_id,)).fetchone()
        new_filename = new_product['filename']
        assert new_filename != old_filename
        
        new_thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], new_filename)
        # This is expected to FAIL until implemented
        assert os.path.exists(new_thumb_path)
        
        # Verify old thumbnail is DELETED
        assert not os.path.exists(old_thumb_path)
