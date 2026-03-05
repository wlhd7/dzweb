from PIL import Image, ImageOps
import os

def generate_thumbnail(file_path, thumb_path, size=(400, 300)):
    """
    Generate a thumbnail from a source image using Pillow.
    Uses ImageOps.pad to resize proportionally without cropping,
    adding white padding as needed to match the target size.
    """
    try:
        # Open source image
        with Image.open(file_path) as img:
            # Convert to RGB to ensure white padding works correctly for all modes
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # ImageOps.pad resizes without cropping and adds color padding
            # method=Image.Resampling.LANCZOS provides high-quality downsampling
            thumb = ImageOps.pad(img, size, method=Image.Resampling.LANCZOS, color=(255, 255, 255))
            
            # Ensure the output directory exists
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            
            # Save the thumbnail
            thumb.save(thumb_path, quality=85, optimize=True)
            
        return True
    except Exception as e:
        # Re-raise or handle as needed by spec
        # Spec says "log but don't disrupt product creation" but for the utility itself
        # we might want to let the caller handle it.
        raise e

def convert_to_webp(source_path, quality=80):
    """
    Convert a source image to WebP format.
    Returns the path to the generated WebP file.
    If the source file is already WebP, returns the same path.
    """
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")
        
    # Determine the target path by changing extension to .webp
    base_path, ext = os.path.splitext(source_path)
    if ext.lower() == '.webp':
        return source_path

    target_path = f"{base_path}.webp"
    
    try:
        with Image.open(source_path) as img:
            # Convert to RGB if necessary (e.g. for RGBA -> WebP if preferred, 
            # but WebP supports alpha, so we can keep it if it's there)
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            
            img.save(target_path, "WEBP", quality=quality, optimize=True)
            
        return target_path
    except Exception as e:
        raise e
