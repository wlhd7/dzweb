import os
import tempfile
import pytest
from dzweb import create_app
from dzweb.db import get_db, init_database
import bcrypt

with open(os.path.join(os.path.dirname(__file__), '../dzweb/schema.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf-8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test_secret_key',
    })

    with app.app_context():
        init_database()
        db = get_db()
        # Add a test user
        password = bcrypt.hashpw(b'test_password', bcrypt.gensalt()).decode('utf-8')
        db.execute(
            "INSERT INTO users (username, password, applist) VALUES (?, ?, ?)",
            ('test_user', password, '[]')
        )
        # Add test apps
        db.execute(
            "INSERT INTO apps (appname, appurl) VALUES (?, ?)",
            ('App 1', 'user.userhome')
        )
        db.execute(
            "INSERT INTO apps (appname, appurl) VALUES (?, ?)",
            ('App 2', 'user.edit_product_permission')
        )
        db.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test_user', password='test_password'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
