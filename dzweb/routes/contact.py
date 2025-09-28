from flask import Blueprint, render_template

bp = Blueprint('contact', __name__, url_prefix='/contact')


@bp.route('/')
def contact_us():
    return render_template('contact/contact-us.html')


@bp.route('/location')
def location():
    return render_template('contact/location.html')
