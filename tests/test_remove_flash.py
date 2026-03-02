import pytest
from unittest.mock import patch

def test_mailbox_post_failure_no_flash(client, app):
    """
    Test that when mail sending fails, no Flash message is shown.
    """
    # Simulate send_feedback_email returning False
    with patch('dzweb.routes.contact.send_feedback_email', return_value=False):
        response = client.post('/contact/mailbox', data={
            'title': 'Test Title',
            'content': 'Test Content',
            'liaison': 'Test Person',
            'unit': 'Test Unit',
            'address': 'Test Address',
            'telephone': '12345678',
            'mobilephone': '13800138000',
            'mail': 'test@example.com'
        }, follow_redirects=True)

        # Assert that "邮件发送失败" (in flash div) is NOT present in the HTML response
        assert b'flash' not in response.data
        assert b'\xe9\x82\xae\xe4\xbb\xb6\xe5\x8f\x91\xe9\x80\x81\xe5\xa4\xb1\xe8\xb4\xa5' not in response.data
