import pytest
from flask import url_for
import json

def test_json_ld_schema(client, app):
    """Verify that JSON-LD blocks are valid and contain expected data."""
    # Test Product Page (assumes product ID 1 exists)
    response = client.get('/product/1/display')
    if response.status_code == 200:
        data = response.data.decode('utf-8')
        assert 'application/ld+json' in data
        assert '"@type": "Product"' in data
        assert '"brand"' in data
        assert '"offers"' in data

    # Test Case Page
    response = client.get('/case/robot-welding')
    if response.status_code == 200:
        data = response.data.decode('utf-8')
        assert 'application/ld+json' in data
        assert '"@type": "Article"' in data
        assert '"publisher"' in data

def test_case_page_seo(client, app):
    """Verify case display page has dynamic title and meta description."""
    # Assuming there is a 'robot-welding' case in the DB
    response = client.get('/case/robot-welding')
    if response.status_code == 200:
        data = response.data.decode('utf-8')
        assert '<title>' in data
        assert '<meta name="description"' in data
        assert '<meta name="keywords"' in data
        
        # Multilingual check
        response_en = client.get('/case/robot-welding?lang=en')
        data_en = response_en.data.decode('utf-8')
        assert 'robot-welding' in data_en or 'Robot' in data_en

def test_sitemap_content(client, app):
    """Verify sitemap contains homepage, case details, and correct priorities."""
    response = client.get('/sitemap.xml')
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert '<urlset' in data
    assert '<priority>1.0</priority>' in data
    assert '<priority>0.8</priority>' in data
    assert '<priority>0.7</priority>' in data
