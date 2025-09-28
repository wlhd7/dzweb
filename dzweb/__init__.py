from flask import Flask, current_app
import os
from .routes import bps, init_app
from .lang import init_lang
from .db import init_db
from .logging import setup_logging


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'dzweb.sqlite'),
            BABEL_DEFAUTL_LOCALE='zh',
            UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads')
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

    setup_logging(app)

    for bp in bps:
        app.register_blueprint(bp.bp)

    init_lang(app)

    init_db(app)

    init_app(app)

    app.add_url_rule('/', endpoint='home.main')

    return app
