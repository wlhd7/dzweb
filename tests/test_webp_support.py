import pytest
from PIL import Image, features

def test_pillow_installed():
    import PIL
    assert PIL.__version__

def test_webp_support():
    assert features.check('webp'), "Pillow must be compiled with WebP support"

def test_requirements_file():
    with open('requirements.txt', 'r') as f:
        content = f.read()
        assert 'Pillow' in content
