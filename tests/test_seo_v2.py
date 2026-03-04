import pytest
from flask import url_for

def test_sitemap_content(client, app):
    """Verify sitemap contains homepage, case details, and correct priorities."""
    with app.test_request_context():
        response = client.get(url_for('home.sitemap'))
    
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert '<urlset' in data
    
    # Check Homepage (priority 1.0)
    assert '<loc>https://www.dongzhen.cn/</loc>' in data or '<loc>http://localhost/</loc>' in data
    assert '<priority>1.0</priority>' in data
    
    # Check Case detail (slug based)
    # Note: This assumes at least one case exists in the DB if running with production DB, 
    # or we need to mock it. The current sitemap route uses get_case_modules().
    assert '/case/' in data
    
    # Check Priorities
    assert '<priority>0.8</priority>' in data
    assert '<priority>0.7</priority>' in data
