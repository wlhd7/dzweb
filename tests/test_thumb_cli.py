import os
import pytest
from PIL import Image
import time

def test_generate_thumbs_command_products(app, runner):
    """Test generate-thumbs command for products with --force flag."""
    # 1. Setup: Create a product in DB and its image
    with app.app_context():
        from dzweb.db import get_db
        db = get_db()
        # Find next ID or just use what we get
        cursor = db.execute(
            'INSERT INTO products (productname, brief, category, filename) VALUES (?, ?, ?, ?)',
            ('Test Prod', 'Brief', 'automation', 'test_prod.jpg')
        )
        product_id = cursor.lastrowid
        db.commit()
        
    upload_folder = app.config['UPLOAD_FOLDER']
    thumb_folder = app.config['THUMBNAIL_FOLDER']
    
    source_file = os.path.join(upload_folder, 'test_prod.jpg')
    img = Image.new('RGB', (800, 200), color='red')
    img.save(source_file, 'JPEG')
    
    # 2. Action: Run the command (first time)
    result = runner.invoke(args=['generate-thumbs'])
    
    # 3. Assert: Thumbnail generated
    assert f'Generated thumbnail for product_{product_id}' in result.output
    thumb_file = os.path.join(thumb_folder, 'test_prod.jpg')
    assert os.path.exists(thumb_file)
    
    # 4. Action: Run again without force (should skip)
    result = runner.invoke(args=['generate-thumbs'])
    # Might be more than 1 skip if there are other products in DB
    assert 'Skipped:' in result.output
    
    # 5. Action: Run with --force
    original_mtime = os.path.getmtime(thumb_file)
    time.sleep(0.1)
    
    result = runner.invoke(args=['generate-thumbs', '--force'])
    
    # 6. Assert: Regenerated
    assert f'Generated thumbnail for product_{product_id}' in result.output
    assert 'Skipped: 0' in result.output

def test_generate_thumbs_command_cases(app, runner):
    """Test generate-thumbs command for case images."""
    with app.app_context():
        from dzweb.db import get_db
        db = get_db()
        db.execute(
            'INSERT INTO case_modules (slug, title_zh) VALUES (?, ?)',
            ('test-case', '测试案例')
        )
        cursor = db.execute(
            'INSERT INTO case_contents (case_id, type, filename, sort_order) VALUES (?, ?, ?, ?)',
            (1, 'image', 'case_image.jpg', 1)
        )
        content_id = cursor.lastrowid
        db.commit()
        
    upload_folder = app.config['UPLOAD_FOLDER']
    thumb_folder = app.config['THUMBNAIL_FOLDER']
    
    source_file = os.path.join(upload_folder, 'case_image.jpg')
    img = Image.new('RGB', (200, 800), color='blue')
    img.save(source_file, 'JPEG')
    
    # Action
    result = runner.invoke(args=['generate-thumbs'])
    
    # Assert
    assert f'Generated thumbnail for case_content_{content_id}' in result.output
    assert os.path.exists(os.path.join(thumb_folder, 'case_image.jpg'))

def test_cleanup_images_includes_cases(app, runner):
    """Test that cleanup-images does NOT delete case images."""
    with app.app_context():
        from dzweb.db import get_db
        db = get_db()
        db.execute('INSERT INTO case_modules (slug, title_zh) VALUES (?, ?)', ('c1', 'C1'))
        db.execute(
            'INSERT INTO case_contents (case_id, type, filename, sort_order) VALUES (?, ?, ?, ?)', 
            (1, 'image', 'keep_me.jpg', 1)
        )
        db.commit()
        
    upload_folder = app.config['UPLOAD_FOLDER']
    keep_file = os.path.join(upload_folder, 'keep_me.jpg')
    orphan_file = os.path.join(upload_folder, 'delete_me.jpg')
    
    Image.new('RGB', (10, 10)).save(keep_file)
    Image.new('RGB', (10, 10)).save(orphan_file)
    
    # Action
    result = runner.invoke(args=['cleanup-images'])
    
    # Assert
    assert 'Deleted' in result.output
    assert os.path.exists(keep_file)
    assert not os.path.exists(orphan_file)
