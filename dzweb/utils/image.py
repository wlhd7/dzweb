from PIL import Image, ImageOps
import os

def generate_thumbnail(file_path, thumb_path, size=(400, 300)):
    """
    Generate a thumbnail from a source image using Pillow.
    Uses ImageOps.fit to crop and resize proportionally to the target size.
    """
    try:
        # Open source image
        with Image.open(file_path) as img:
            # ImageOps.fit crops and resizes according to aspect ratio
            # method=Image.Resampling.LANCZOS provides high-quality downsampling
            thumb = ImageOps.fit(img, size, method=Image.Resampling.LANCZOS)
            
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
