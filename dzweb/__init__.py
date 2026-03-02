from flask import Flask, current_app
import os
from dotenv import load_dotenv
from .routes import bps, init_app
from .lang import init_lang
from .db import init_db
from .logging import setup_logging
from .mail import init_mail


def create_app(test_config=None):
    # Load environment variables from .env file
    load_dotenv()
    
    app = Flask(__name__, instance_relative_config=True)
    
    # Helper for boolean env vars
    def get_bool_env(name, default=False):
        val = os.environ.get(name, str(default)).lower()
        return val in ('true', '1', 'yes', 'on')

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        DATABASE=os.path.join(app.instance_path, 'dzweb.sqlite'),
        BABEL_DEFAULT_LOCALE='zh',
        UPLOAD_FOLDER=os.path.join(app.root_path, 'static', 'uploads'),
        THUMBNAIL_FOLDER=os.path.join(app.root_path, 'static', 'uploads', 'thumbs'),
        
        # Admin & Security
        DZWEB_ADMIN_PASSWORD=os.environ.get('DZWEB_ADMIN_PASSWORD'),
        
        # Mail Configuration
        MAIL_SERVER=os.environ.get('MAIL_SERVER'),
        MAIL_PORT=int(os.environ.get('MAIL_PORT', 465)),
        MAIL_USE_TLS=get_bool_env('MAIL_USE_TLS', False),
        MAIL_USE_SSL=get_bool_env('MAIL_USE_SSL', True),
        MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
        MAIL_DEFAULT_SENDER=os.environ.get('MAIL_DEFAULT_SENDER'),
        MAIL_ADMINS=[os.environ.get('MAIL_ADMIN')] if os.environ.get('MAIL_ADMIN') else [],
        
        # SEO & Verification
        BAIDU_PUSH_TOKEN=os.environ.get('BAIDU_PUSH_TOKEN'),
        BAIDU_SITE_VERIFICATION=os.environ.get('BAIDU_SITE_VERIFICATION'),
        BAIDU_TONGJI_ID=os.environ.get('BAIDU_TONGJI_ID'),
        BING_SITE_VERIFICATION=os.environ.get('BING_SITE_VERIFICATION'),
        GOOGLE_SITE_VERIFICATION=os.environ.get('GOOGLE_SITE_VERIFICATION'),
        
        SEND_FILE_MAX_AGE_DEFAULT=31536000
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except OSError:
        pass

    try:
        os.makedirs(app.config['THUMBNAIL_FOLDER'])
    except OSError:
        pass

    if not app.testing:
        setup_logging(app)

    for bp in bps:
        app.register_blueprint(bp.bp)

    init_lang(app)

    init_db(app)

    init_app(app)

    init_mail(app)

    app.add_url_rule('/', endpoint='index')

    return app
