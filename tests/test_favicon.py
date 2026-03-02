def test_favicon_in_html_head(client):
    """
    Test that the HTML head contains the correct favicon tags.
    """
    response = client.get('/')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '<link rel="icon" href="/static/favicon.ico" type="image/x-icon">' in html
    assert '<link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon">' in html

def test_favicon_route_cache(client):
    """
    Test that the /favicon.ico route returns a 200 status code
    and has a max-age Cache-Control header.
    """
    response = client.get('/favicon.ico')
    assert response.status_code == 200
    
    # Check if Cache-Control is present and contains max-age
    cache_control = response.headers.get('Cache-Control', '')
    assert 'max-age=31536000' in cache_control
    assert 'public' in cache_control
