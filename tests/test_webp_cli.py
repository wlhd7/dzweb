import os
import pytest
from PIL import Image
from dzweb.utils.image import convert_to_webp

def test_convert_webp_command(app, runner):
    # Setup: Ensure a valid product exists and has an image
    upload_folder = app.config['UPLOAD_FOLDER']
    source_file = os.path.join(upload_folder, 'test.jpg')
    
    # Create a real image for PIL to process
    img = Image.new('RGB', (100, 100), color='red')
    img.save(source_file, 'JPEG')
    
    # Action: Run the command
    result = runner.invoke(args=['convert-webp'])
    
    # Assert: Check output and file existence
    assert 'WebP conversion complete' in result.output
    assert 'Generated WebP' in result.output
    
    webp_path = os.path.join(upload_folder, 'test.webp')
    assert os.path.exists(webp_path)
    
    # Verify it's a valid WebP
    with Image.open(webp_path) as webp_img:
        assert webp_img.format == 'WEBP'

def test_convert_webp_command_skips_existing(app, runner):
    upload_folder = app.config['UPLOAD_FOLDER']
    source_file = os.path.join(upload_folder, 'test.jpg')
    webp_file = os.path.join(upload_folder, 'test.webp')
    
    # Create both files
    img = Image.new('RGB', (100, 100), color='red')
    img.save(source_file, 'JPEG')
    img.save(webp_file, 'WEBP')
    
    # Get original mtime
    original_mtime = os.path.getmtime(webp_file)
    
    # Action: Run the command
    result = runner.invoke(args=['convert-webp'])
    
    # Assert: Should skip
    assert 'Skipped: 1' in result.output
    assert os.path.getmtime(webp_file) == original_mtime
