import pytest

def test_login_failure_shows_p_tag_no_flash(client, auth, app):
    """
    Test that login failure shows the inline <p> tag and NOT a flash message.
    """
    # 1. POST with wrong password
    response = auth.admin_login(password='wrong_password')
    
    # Check that we are still on the login page (status 200)
    assert response.status_code == 200
    
    # 2. Check for the inline <p> tag with error message
    # Note: Using decode() to check the HTML content
    html_content = response.data.decode('utf-8')
    assert '管理员密码错误' in html_content
    assert '<p>' in html_content
    
    # 3. Verify Flash related CSS classes are NOT present (redundant check)
    assert 'class="flash"' not in html_content
    assert 'alert-info' not in html_content

def test_login_page_initially_no_error(client, auth, app):
    """
    Verify that the login page initially does not show the error message.
    """
    response = client.get('/admin/login')
    html_content = response.data.decode('utf-8')
    assert '管理员密码错误' not in html_content
