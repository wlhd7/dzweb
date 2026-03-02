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
    upload_dir = tempfile.mkdtemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'UPLOAD_FOLDER': upload_dir,
        'SECRET_KEY': 'test_secret_key',
        'DZWEB_ADMIN_PASSWORD': 'test_admin_password',
        'BAIDU_PUSH_TOKEN': 'test_token',
        'BAIDU_SITE_VERIFICATION': 'test_baidu_ver',
        'BAIDU_TONGJI_ID': 'test_tongji_id',
        'BING_SITE_VERIFICATION': 'test_bing_ver',
        'GOOGLE_SITE_VERIFICATION': 'test_google_ver',
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
            ('App 1', 'admin.userhome')
        )
        db.execute(
            "INSERT INTO apps (appname, appurl) VALUES (?, ?)",
            ('App 2', 'admin.edit_product')
        )
        # Add a test product
        db.execute(
            "INSERT INTO products (productname, brief, category, filename, class) VALUES (?, ?, ?, ?, ?)",
            ('Test Product', 'Test Brief', 'automation', 'test.jpg', 'engine')
        )
        # Create the dummy test.jpg
        with open(os.path.join(upload_dir, 'test.jpg'), 'wb') as f:
            f.write(b"dummy image data")

        db.commit()

    yield app

    os.close(db_fd)
    os.unlink(db_path)
    # Cleanup upload dir
    import shutil
    shutil.rmtree(upload_dir)


@pytest.fixture
def client(app):
    return app.test_client()

class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username='test_user', password='test_password'):
        return self._client.post(
            '/admin/login',
            data={'username': username, 'password': password}
        )

    def admin_login(self, password='test_admin_password'):
        return self._client.post(
            '/admin/login',
            data={'password': password}
        )

    def logout(self):
        return self._client.get('/admin/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)
