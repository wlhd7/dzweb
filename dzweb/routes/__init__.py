from flask import send_from_directory
from . import home, auth, about, product, case, service, human, contact, message, user
import os

bps = [home, auth, about, product, case, service, human, contact, message, user]

def init_app(app):
    @app.route('/instance-files/<filename>')
    def instance_files(filename):
        return send_from_directory(app.instance_path + '/uploads', filename)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
