from flask import Blueprint, render_template, request, session, g, redirect, url_for, flash, make_response, jsonify, current_app
from dzweb.db import get_db, get_all_apps
from functools import wraps
from flask_babel import _
import json
from datetime import datetime, timedelta

bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    if session.get('is_admin'):
        # Create a mock admin user object
        g.user = {'username': 'Administrator', 'id': 0}
    else:
        g.user = None


@bp.before_request
def load_added_apps():
    # Only load apps if the user is an admin
    if session.get('is_admin'):
        # Fetch all apps from the database
        apps = get_all_apps()
        # Store all apps in the context for sidebar rendering
        g.appname_appurl_dict = {app['appname']: app['appurl'] for app in apps}
    else:
        g.appname_appurl_dict = {}


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        admin_password = current_app.config.get('DZWEB_ADMIN_PASSWORD')

        if not admin_password:
            return render_template('admin/login.html')

        if g.get('user'):
            return redirect(url_for('admin.userhome'))

        if password == admin_password:
            session.clear()
            session['is_admin'] = True
            return redirect(url_for('admin.userhome'))
        else:
            # Silent failure as per user's preference for removing all flash messages
            pass

    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    g.user = None

    if request.args.get('next', None):
        return redirect(request.args.get('next'))
    else:
        return redirect(url_for('home.index'))


@bp.route('/')
@login_required
def userhome():
    apps = get_all_apps()
    return render_template('user/userhome.html', apps=apps)


@bp.route('/edit-product')
@login_required
def edit_product():
    return render_template('user/edit-product-permission.html')


@bp.route('/edit-hire')
@login_required
def edit_hire():
    return render_template('user/edit-hire-permission.html')
