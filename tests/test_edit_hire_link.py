import pytest

def test_edit_hire_page_link(client, auth):
    # Login to access admin pages if necessary (though the current implementation might not strictly require it for this specific page)
    auth.admin_login()
    response = client.get('/admin/edit-hire')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    
    # Check for the correct link target
    assert 'href="/human/create-position"' in html
    
    # Check for the updated text (assuming Chinese as default in test environment)
    assert '点击此处新增职位' in html
    
    # Check for the updated title
    assert '新增招聘职位' in html
