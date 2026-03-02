from flask import send_from_directory, render_template
from . import home, product, case, service, human, contact, admin
import os

bps = [home, product, case, service, human, contact, admin]

def init_app(app):
    product.init_app(app)
    @app.route('/instance-files/<filename>')
    def instance_files(filename):
        return send_from_directory(app.instance_path + '/uploads', filename)

    @app.route('/thumbnail-files/<filename>')
    def thumbnail_files(filename):
        return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404