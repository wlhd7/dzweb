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
        
        # Verify success message is in response and it's not a flash message
        assert "感谢您的反馈，我们会尽快处理！" in response.data.decode('utf-8')
        assert 'class="flash"' not in response.data.decode('utf-8')

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
        assert b'class="flash"' not in response.data
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
        assert b'class="flash"' not in response.data
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
    assert b'class="flash"' not in response.data
