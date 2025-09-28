from flask import Blueprint, render_template


bp = Blueprint('service', __name__, url_prefix='/service')


@bp.route('/')
def service():
    return render_template('service/service.html')

