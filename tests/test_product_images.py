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

def test_delete_product_removes_thumbnail(client, auth, app):
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        # 1. Create a product
        test_img = create_test_image()
        client.post('/product/create', data={
            'productname': 'Delete Test',
            'brief': 'Delete me',
            'category': 'automation',
            'class': 'engine',
            'file': (test_img, 'del.jpg')
        }, content_type='multipart/form-data')
        
        product = db.execute('SELECT id, filename FROM products WHERE productname = "Delete Test"').fetchone()
        product_id = product['id']
        filename = product['filename']
        thumb_path = os.path.join(app.config['THUMBNAIL_FOLDER'], filename)
        assert os.path.exists(thumb_path)
        
        # 2. Delete the product
        client.get(f'/product/{product_id}/delete', follow_redirects=True)
        
        # Verify thumbnail is DELETED
        # This is expected to FAIL until implemented
        assert not os.path.exists(thumb_path)

def test_cleanup_images_removes_orphan_thumbnails(client, app):
    runner = app.test_cli_runner()
    
    thumb_folder = app.config['THUMBNAIL_FOLDER']
    os.makedirs(thumb_folder, exist_ok=True)
    
    # 1. Create an orphan thumbnail
    orphan_thumb = os.path.join(thumb_folder, 'orphan_thumb.jpg')
    with open(orphan_thumb, 'wb') as f:
        f.write(b"orphan thumb data")
        
    # 2. Ensure a referenced thumbnail exists
    with app.app_context():
        db = get_db()
        seeded = db.execute('SELECT filename FROM products LIMIT 1').fetchone()
        referenced_thumb = os.path.join(thumb_folder, seeded['filename'])
        with open(referenced_thumb, 'wb') as f:
            f.write(b"referenced thumb data")
            
    assert os.path.exists(orphan_thumb)
    assert os.path.exists(referenced_thumb)
    
    # 3. Run cleanup
    result = runner.invoke(args=['cleanup-images'])
    assert result.exit_code == 0
    
    # 4. Verify
    assert not os.path.exists(orphan_thumb)
    assert os.path.exists(referenced_thumb)

def test_homepage_uses_thumbnail_route(client, app):
    # Ensure there's at least one product
    with app.app_context():
        db = get_db()
        product = db.execute('SELECT filename FROM products LIMIT 1').fetchone()
        filename = product['filename']
    
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert f'/thumbnail-files/{filename}' in html
    assert f'/instance-files/{filename}' not in html # For the showcase part

def test_product_list_uses_thumbnail_route(client, app):
    # Ensure there's at least one product
    with app.app_context():
        db = get_db()
        product = db.execute('SELECT filename, category FROM products LIMIT 1').fetchone()
        filename = product['filename']
        category = product['category']
    
    response = client.get(f'/product/{category}')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert f'/thumbnail-files/{filename}' in html

def test_search_results_use_thumbnail_route(client, app):
    # Ensure there's at least one product with a known name
    with app.app_context():
        db = get_db()
        product = db.execute('SELECT productname, filename FROM products LIMIT 1').fetchone()
        name = product['productname']
        filename = product['filename']
    
    response = client.get(f'/product/search?q={name}')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert f'/thumbnail-files/{filename}' in html

def test_generate_thumbs_command(app):
    runner = app.test_cli_runner()
    
    with app.app_context():
        # Ensure thumbnail directory exists
        thumb_folder = app.config['THUMBNAIL_FOLDER']
        os.makedirs(thumb_folder, exist_ok=True)
        
        # Ensure there's a real image for the seeded product 'test.jpg'
        upload_folder = app.config['UPLOAD_FOLDER']
        orig_path = os.path.join(upload_folder, 'test.jpg')
        img = Image.new('RGB', (100, 100), color='green')
        img.save(orig_path)
        
        # Ensure its thumbnail is GONE
        thumb_path = os.path.join(thumb_folder, 'test.jpg')
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
            
        assert not os.path.exists(thumb_path)
        
        # Run command
        result = runner.invoke(args=['generate-thumbs'])
        assert result.exit_code == 0
        assert "Generated thumbnail for product" in result.output
        
        # Verify
        assert os.path.exists(thumb_path)
