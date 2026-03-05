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

def test_create_product_generates_webp(client, auth, app):
    auth.admin_login()
    
    test_img = create_test_image()
    data = {
        'productname': 'WebP Integration Test',
        'brief': 'Testing WebP generation on upload',
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
        product = db.execute('SELECT filename FROM products WHERE productname = "WebP Integration Test"').fetchone()
        assert product is not None
        filename = product['filename']
        
        # Verify original image exists
        orig_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        assert os.path.exists(orig_path)
        
        # Verify WebP exists
        base_name = os.path.splitext(filename)[0]
        webp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}.webp")
        assert os.path.exists(webp_path), f"WebP not found at {webp_path}"
        
        # Verify it's a valid WebP image
        with Image.open(webp_path) as webp_img:
            assert webp_img.format == "WEBP"

def test_update_product_generates_new_webp_and_removes_old(client, auth, app):
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        # 1. Create a product first
        test_img1 = create_test_image()
        client.post('/product/create', data={
            'productname': 'WebP Update Test',
            'brief': 'Initial',
            'category': 'automation',
            'class': 'engine',
            'file': (test_img1, 'img1.jpg')
        }, content_type='multipart/form-data')
        
        product = db.execute('SELECT id, filename FROM products WHERE productname = "WebP Update Test"').fetchone()
        product_id = product['id']
        old_filename = product['filename']
        
        base_old = os.path.splitext(old_filename)[0]
        old_webp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_old}.webp")
        # If the create hook worked, this should exist. But for now it might not.
        # We'll see it fail.
        
        # 2. Update with NEW image
        test_img2 = create_test_image()
        client.post(f'/product/{product_id}/update?next=/product/automation', data={
            'productname': 'WebP Update Test',
            'brief': 'Updated',
            'category': 'automation',
            'class': 'engine',
            'file': (test_img2, 'img2.jpg')
        }, content_type='multipart/form-data')
        
        new_product = db.execute('SELECT filename FROM products WHERE id = ?', (product_id,)).fetchone()
        new_filename = new_product['filename']
        assert new_filename != old_filename
        
        base_new = os.path.splitext(new_filename)[0]
        new_webp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_new}.webp")
        assert os.path.exists(new_webp_path)
        
        # Verify old WebP is DELETED
        assert not os.path.exists(old_webp_path)

def test_delete_product_removes_webp(client, auth, app):
    auth.admin_login()
    
    with app.app_context():
        db = get_db()
        # 1. Create a product
        test_img = create_test_image()
        client.post('/product/create', data={
            'productname': 'WebP Delete Test',
            'brief': 'Delete me',
            'category': 'automation',
            'class': 'engine',
            'file': (test_img, 'del.jpg')
        }, content_type='multipart/form-data')
        
        product = db.execute('SELECT id, filename FROM products WHERE productname = "WebP Delete Test"').fetchone()
        product_id = product['id']
        filename = product['filename']
        
        base_name = os.path.splitext(filename)[0]
        webp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}.webp")
        
        # 2. Delete the product
        client.get(f'/product/{product_id}/delete', follow_redirects=True)
        
        # Verify WebP is DELETED
        assert not os.path.exists(webp_path)

def test_cleanup_images_removes_orphan_webp(client, app):
    runner = app.test_cli_runner()
    
    upload_folder = app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # 1. Create an orphan WebP
    orphan_webp = os.path.join(upload_folder, 'orphan_thumb.webp')
    with open(orphan_webp, 'wb') as f:
        f.write(b"orphan webp data")
        
    # 2. Ensure a referenced WebP exists
    with app.app_context():
        db = get_db()
        seeded = db.execute('SELECT filename FROM products LIMIT 1').fetchone()
        filename = seeded['filename']
        base_name = os.path.splitext(filename)[0]
        referenced_webp = os.path.join(upload_folder, f"{base_name}.webp")
        with open(referenced_webp, 'wb') as f:
            f.write(b"referenced webp data")
            
    assert os.path.exists(orphan_webp)
    assert os.path.exists(referenced_webp)
    
    # 3. Run cleanup
    result = runner.invoke(args=['cleanup-images'])
    assert result.exit_code == 0
    
    # 4. Verify
    assert not os.path.exists(orphan_webp)
    assert os.path.exists(referenced_webp)

def test_product_display_page_uses_picture_tag(client, app):
    # Ensure there's at least one product
    with app.app_context():
        db = get_db()
        product = db.execute('SELECT id, filename FROM products LIMIT 1').fetchone()
        product_id = product['id']
        filename = product['filename']
        base_name = os.path.splitext(filename)[0]
    
    response = client.get(f'/product/{product_id}/display')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # Check for <picture> tag
    assert '<picture>' in html
    assert '</picture>' in html
    
    # Check for <source> with WebP
    assert f'type="image/webp"' in html
    assert f'srcset="/static/uploads/{base_name}.webp"' in html
    
    # Check for <img> fallback
    assert f'src="/static/uploads/{filename}"' in html
    assert 'class="product-image"' in html

def test_homepage_still_uses_thumbnails(client, app):
    # Ensure there's at least one product
    with app.app_context():
        db = get_db()
        product = db.execute('SELECT filename FROM products LIMIT 1').fetchone()
        filename = product['filename']
    
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # Verify it uses thumbnails and NOT <picture> tag for products
    assert f'/static/uploads/thumbs/{filename}' in html
    # The homepage shouldn't have been updated with <picture> for products
    # We check if there are ANY <picture> tags (unless the base.html uses it, which it doesn't seem to)
    assert '<picture>' not in html

def create_webp_image():
    file = io.BytesIO()
    image = Image.new('RGB', (100, 100), color='red')
    image.save(file, 'WEBP')
    file.seek(0)
    return file

def test_product_create_direct_webp(client, auth, app):
    auth.admin_login()
    
    test_img = create_webp_image()
    data = {
        'productname': 'Direct WebP Product',
        'brief': 'Test Direct WebP',
        'category': 'automation',
        'class': 'engine',
        'file': (test_img, 'test.webp')
    }
    
    response = client.post('/product/create', data=data, follow_redirects=True)
    assert response.status_code == 200
    
    with app.app_context():
        db = get_db()
        product = db.execute('SELECT * FROM products WHERE productname = ?', ('Direct WebP Product',)).fetchone()
        assert product is not None
        assert product['filename'].endswith('.webp')
        
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, product['filename'])
        assert os.path.exists(file_path)

def test_case_content_add_direct_webp(client, auth, app):
    auth.admin_login()
    
    case_id = None
    with app.app_context():
        # Create a module first
        db = get_db()
        db.execute("INSERT INTO case_modules (slug, title_zh) VALUES ('direct-webp-case', 'Direct WebP Case')")
        case_id = db.execute("SELECT id FROM case_modules WHERE slug = 'direct-webp-case'").fetchone()[0]
        db.commit()
    
    test_img = create_webp_image()
    data = {
        'type': 'image',
        'content_zh': 'Direct WebP Image',
        'sort_order': '1',
        'file': (test_img, 'test.webp')
    }
    
    response = client.post(f'/case/api/module/{case_id}/content', data=data)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    
    with app.app_context():
        db = get_db()
        content = db.execute('SELECT * FROM case_contents WHERE case_id = ?', (case_id,)).fetchone()
        assert content is not None
        assert content['filename'].endswith('.webp')
        
        upload_folder = app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, content['filename'])
        assert os.path.exists(file_path)
