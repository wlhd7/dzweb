import pytest
from flask import url_for

def test_sitemap_route(client, app):
    """Verify that the /sitemap.xml route returns 200 and XML content."""
    with app.test_request_context():
        response = client.get(url_for('home.sitemap'))
    
    assert response.status_code == 200
    assert response.mimetype == 'application/xml'
    assert b'<urlset' in response.data
    assert b'<loc>' in response.data
