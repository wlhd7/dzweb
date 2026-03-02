from dzweb import create_app
import os

app = create_app({
    'TESTING': True,
    'MAIL_SERVER': 'invalid.host.xyz', # Force failure
    'MAIL_ADMIN': 'test@test.com'
})

with app.test_client() as client:
    response = client.post('/contact/mailbox', data={
        'title': 'Test',
        'content': 'Test',
        'liaison': 'Test',
        'unit': 'Test',
        'mail': 'test@test.com'
    })
    print(f"Status: {response.status_code}")
    if response.status_code == 500:
        print("DETECTED 500 ERROR")
    else:
        print("Success (No 500)")
