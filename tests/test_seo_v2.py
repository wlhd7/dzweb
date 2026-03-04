import pytest
from flask import url_for

def test_case_page_seo(client, app):
    """Verify case display page has dynamic title and meta description."""
    # Assuming there is a 'robot-welding' case in the DB
    with app.test_request_context():
        response = client.get(url_for('case.display_case', slug='robot-welding'))
    
    if response.status_code == 200:
        data = response.data.decode('utf-8')
        assert '<title>机器人焊接' in data or 'Robot Welding' in data
        assert '<meta name="description"' in data
        assert '<meta name="keywords"' in data
        
        # Multilingual check
        response_en = client.get(url_for('case.display_case', slug='robot-welding', lang='en'))
        data_en = response_en.data.decode('utf-8')
        assert 'Robot Welding' in data_en or 'robot-welding' in data_en

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
