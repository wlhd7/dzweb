import os
import pytest
from PIL import Image
from dzweb.utils.image import generate_thumbnail

def test_generate_thumbnail_contain_strategy(tmp_path):
    """
    Test that generate_thumbnail uses a 'Contain' strategy:
    - No cropping.
    - White padding for different aspect ratios.
    """
    # Create a 800x200 red image (aspect ratio 4:1)
    img_path = tmp_path / "test_wide.jpg"
    thumb_path = tmp_path / "thumb_wide.jpg"
    
    # Original color is red
    original_color = (255, 0, 0)
    img = Image.new('RGB', (800, 200), color=original_color)
    img.save(img_path)
    
    # Target size 400x300 (aspect ratio 4:3)
    target_size = (400, 300)
    
    # Generate thumbnail
    generate_thumbnail(str(img_path), str(thumb_path), target_size)
    
    # Assert thumbnail exists
    assert os.path.exists(thumb_path)
    
    # Assert thumbnail size is exactly 400x300
    with Image.open(thumb_path) as thumb:
        assert thumb.size == target_size
        
        # In a 'Contain' strategy for 800x200 -> 400x300:
        # Scale is 0.5 (800*0.5=400, 200*0.5=100)
        # Content is 400x100, centered vertically.
        # Padding should be 100px at top and 100px at bottom.
        
        # Check pixel at (0, 0) - should be white padding (255, 255, 255)
        # Current logic (fit) will have red here because it crops to 4:3
        pixel_top_left = thumb.getpixel((0, 0))
        assert pixel_top_left == (255, 255, 255), f"Expected white padding at (0,0), got {pixel_top_left}"
        
        # Check pixel at (200, 150) - center, should be red
        pixel_center = thumb.getpixel((200, 150))
        assert pixel_center == original_color, f"Expected red at center (200,150), got {pixel_center}"

def test_generate_thumbnail_contain_tall(tmp_path):
    """Test with a tall image (aspect ratio 1:4)."""
    img_path = tmp_path / "test_tall.jpg"
    thumb_path = tmp_path / "thumb_tall.jpg"
    
    # 200x800 blue image
    original_color = (0, 0, 255)
    img = Image.new('RGB', (200, 800), color=original_color)
    img.save(img_path)
    
    target_size = (400, 300)
    generate_thumbnail(str(img_path), str(thumb_path), target_size)
    
    with Image.open(thumb_path) as thumb:
        assert thumb.size == target_size
        # 200x800 -> 400x300
        # Height 800 -> 300 (scale 300/800 = 0.375)
        # Width 200 -> 200*0.375 = 75
        # Content 75x300, centered horizontally.
        
        # (0, 0) should be white
        pixel_top_left = thumb.getpixel((0, 0))
        assert pixel_top_left == (255, 255, 255), f"Expected white padding at (0,0), got {pixel_top_left}"
        
        # Center should be blue
        pixel_center = thumb.getpixel((200, 150))
        assert pixel_center == original_color
