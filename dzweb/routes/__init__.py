from flask import send_from_directory, render_template
from . import home, auth, product, case, service, human, contact, message, user
import os
from dzweb.db import get_db

bps = [home, auth, product, case, service, human, contact, message, user]

def init_app(app):
    @app.route('/instance-files/<filename>')
    def instance_files(filename):
        return send_from_directory(app.instance_path + '/uploads', filename)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')