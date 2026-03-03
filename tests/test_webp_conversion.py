import os
import pytest
from PIL import Image
from dzweb.utils.image import convert_to_webp

def test_convert_to_webp_success(tmp_path):
    # Setup: Create a temporary JPG image
    source_dir = tmp_path / "uploads"
    source_dir.mkdir()
    source_file = source_dir / "test.jpg"
    
    # Create a simple RGB image and save as JPG
    img = Image.new("RGB", (100, 100), color="red")
    img.save(source_file, "JPEG")
    
    # Action: Convert to WebP
    webp_path = convert_to_webp(str(source_file), quality=80)
    
    # Assert: Check if WebP file exists and has correct extension
    assert webp_path.endswith(".webp")
    assert os.path.exists(webp_path)
    
    # Assert: Verify it's a valid WebP image
    with Image.open(webp_path) as webp_img:
        assert webp_img.format == "WEBP"

def test_convert_to_webp_file_not_found():
    # Action & Assert: Should raise FileNotFoundError if source doesn't exist
    with pytest.raises(FileNotFoundError):
        convert_to_webp("non_existent_file.jpg")
