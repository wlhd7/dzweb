from flask import send_from_directory, render_template
from . import home, product, case, service, human, contact, admin
import os

bps = [home, product, case, service, human, contact, admin]

def init_app(app):
    product.init_app(app)

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404