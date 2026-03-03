import pytest

def test_case_main_route(client):
    """验证主经典案例页面依然可用。"""
    response = client.get('/case/')
    assert response.status_code == 200

def test_case_sub_pages_removed(client):
    """验证子页面路由已失效。"""
    sub_pages = [
        '/case/extruder',
        '/case/assembly-line',
        '/case/ass',
        '/case/robot-welding'
    ]
    for page in sub_pages:
        response = client.get(page)
        # 目前这些页面还存在，所以测试应该在这里失败
        assert response.status_code == 404, f"Page {page} should be removed"

def test_case_nav_link(client):
    """验证导航栏中的经典案例链接已更新。"""
    response = client.get('/')
    assert response.status_code == 200
    # 期望链接指向 /case/，而不是 /case/extruder
    assert b'href="/case/"' in response.data
    assert b'href="/case/extruder"' not in response.data
