import pytest

def test_company_name_localization(client):
    """验证不同语言下公司名称的正确性"""
    
    # 1. 验证中文 (zh)
    response = client.get('/?lang=zh')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '广州东振机电设备有限公司' in html
    
    # 2. 验证英文 (en)
    response = client.get('/?lang=en')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'GuangZhou DongZhen M&E Equipment Co., Ltd' in html
    
    # 3. 验证日文 (ja)
    response = client.get('/?lang=ja')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '広州東振機電設備有限公司' in html

def test_company_name_in_meta_tags(client):
    """验证 Meta 标签中的公司名称"""
    response = client.get('/?lang=zh')
    html = response.data.decode('utf-8')
    # 检查 Title
    assert '广州东振机电设备有限公司' in html
    # 检查 Description
    assert '广州东振机电设备有限公司' in html
    # 检查 JSON-LD
    assert '"name": "广州东振机电设备有限公司"' in html
