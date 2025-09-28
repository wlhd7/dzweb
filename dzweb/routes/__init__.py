from flask import send_from_directory
from . import home, auth, about, product, case, service, human, contact, message, user

bps = [home, auth, about, product, case, service, human, contact, message, user]

def init_app(app):
    @app.route('/instance-files/<filename>')
    def instance_files(filename):
        return send_from_directory(app.instance_path + '/uploads', filename)
