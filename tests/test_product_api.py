import pytest

def test_get_subcategories(client):
    # Test for automation
    response = client.get('/product/api/subcategories/automation')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 4
    assert {'id': 'engine', 'name': '发动机'} in data

    # Test for non_standard
    response = client.get('/product/api/subcategories/non_standard')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0

    # Test for invalid category
    response = client.get('/product/api/subcategories/invalid')
    assert response.status_code == 200
    assert response.get_json() == []
