from flask import send_from_directory, render_template
from . import home, auth, product, case, service, human, contact, user
import os

bps = [home, auth, product, case, service, human, contact, user]

def init_app(app):
    @app.route('/instance-files/<filename>')
    def instance_files(filename):
        return send_from_directory(app.instance_path + '/uploads', filename)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404