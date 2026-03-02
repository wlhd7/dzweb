import os
import pytest
from PIL import Image
from dzweb.utils.image import generate_thumbnail

def test_generate_thumbnail(tmp_path):
    # Create a dummy image
    img_path = tmp_path / "test.jpg"
    thumb_path = tmp_path / "thumb.jpg"
    
    # Create a 800x800 red square image
    img = Image.new('RGB', (800, 800), color='red')
    img.save(img_path)
    
    # Generate thumbnail
    size = (400, 300)
    generate_thumbnail(str(img_path), str(thumb_path), size)
    
    # Assert thumbnail exists
    assert os.path.exists(thumb_path)
    
    # Assert thumbnail size
    with Image.open(thumb_path) as thumb:
        assert thumb.size == size
