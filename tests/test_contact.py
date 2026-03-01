import pytest
from dzweb.mail import mail

def test_mailbox_get(client):
    response = client.get('/contact/mailbox')
    assert response.status_code == 200
    assert b"<form method='POST'>" in response.data

def test_mailbox_post_success(client, app):
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_ADMINS'] = ['admin@example.com']
    app.config['MAIL_SERVER'] = 'localhost'
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'
    
    with mail.record_messages() as outbox:
        response = client.post('/contact/mailbox', data={
            'title': 'Test Title',
            'content': 'Test Content',
            'liaison': 'Test Person',
            'unit': 'Test Unit',
            'address': 'Test Address',
            'telephone': '12345678',
            'mobilephone': '13800138000',
            'mail': 'test@example.com'
        })
        
        assert response.status_code == 200
        assert len(outbox) == 1
        assert outbox[0].subject == '东振网站客户反馈 - Test Title'
        assert 'admin@example.com' in outbox[0].recipients
        assert 'Test Content' in outbox[0].body
        assert 'Test Person' in outbox[0].body
        assert 'test@example.com' in outbox[0].reply_to

def test_mailbox_post_invalid_data(client, app):
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_ADMINS'] = ['admin@example.com']
    app.config['MAIL_SERVER'] = 'localhost'
    
    with mail.record_messages() as outbox:
        # Missing required fields
        response = client.post('/contact/mailbox', data={
            'title': '',
            'content': 'Test Content',
            'liaison': 'Test Person',
            'unit': 'Test Unit',
            'mail': 'test@example.com'
        })
        assert b'\xe8\xaf\xb7\xe5\xa1\xab\xe5\x86\x99\xe6\x89\x80\xe6\x9c\x89\xe5\xbf\x85\xe5\xa1\xab\xe5\xad\x97\xe6\xae\xb5' in response.data # "请填写所有必填字段"
        assert len(outbox) == 0

def test_mailbox_post_invalid_email(client, app):
    app.config['MAIL_SUPPRESS_SEND'] = True
    app.config['MAIL_ADMINS'] = ['admin@example.com']
    app.config['MAIL_SERVER'] = 'localhost'
    
    with mail.record_messages() as outbox:
        # Invalid email (missing @)
        response = client.post('/contact/mailbox', data={
            'title': 'Test Title',
            'content': 'Test Content',
            'liaison': 'Test Person',
            'unit': 'Test Unit',
            'mail': 'invalid-email'
        })
        assert b'\xe8\xaf\xb7\xe8\xbe\x93\xe5\x85\xa5\xe6\x9c\x89\xe6\x95\x88\xe7\x9a\x84\xe9\x82\xae\xe7\xae\xb1\xe5\x9c\xb0\xe5\x9d\x80' in response.data # "请输入有效的邮箱地址"
        assert len(outbox) == 0

def test_mailbox_post_no_config(client, app):
    app.config['MAIL_SERVER'] = None # Explicitly set to None
    
    response = client.post('/contact/mailbox', data={
        'title': 'Test Title',
        'content': 'Test Content',
        'liaison': 'Test Person',
        'unit': 'Test Unit',
        'mail': 'test@example.com'
    })
    assert b'\xe9\x82\xae\xe4\xbb\xb6\xe5\x8f\x91\xe9\x80\x81\xe5\xa4\xb1\xe8\xb4\xa5' in response.data # "邮件发送失败"
