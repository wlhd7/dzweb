import pytest

def test_footer_icp_info(client):
    """验证页脚包含正确的 ICP 备案号和链接"""
    response = client.get('/')
    assert response.status_code == 200
    
    # 验证备案号文本
    assert b'\xe7\xb2\xa4ICP\xe5\xa4\x872026001637\xe5\x8f\xb7' in response.data # "粤ICP备2026001637号"
    
    # 验证工信部链接
    assert b'https://beian.miit.gov.cn/' in response.data
