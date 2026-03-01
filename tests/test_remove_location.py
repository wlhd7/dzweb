import pytest

def test_location_route_currently_works(client):
    """验证 /contact/location 路由当前返回 200 OK。"""
    response = client.get('/contact/location')
    assert response.status_code == 200
