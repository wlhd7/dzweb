from flask import Blueprint, render_template, redirect, url_for, session, flash, g, request, current_app
from dzweb.db import get_db
from functools import wraps
import bcrypt
from flask_babel import _


bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('is_admin'):
            flash(_('请先登录管理员账号'))

            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    if session.get('is_admin'):
        # Create a mock admin user object
        g.user = {'username': 'Administrator', 'id': 0}
    else:
        g.pop('user', None)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        admin_password = current_app.config.get('DZWEB_ADMIN_PASSWORD')

        if not admin_password:
            flash(_('系统未配置管理员密码，请联系技术支持。'))
            return render_template('auth/login.html')

        if g.get('user'):
            flash(_('管理员已登录'))
            return redirect(url_for('admin.userhome'))

        if password == admin_password:
            session.clear()
            session['is_admin'] = True
            return redirect(url_for('admin.userhome'))
        else:
            flash(_('密码错误.'))

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    g.pop('user', None)

    if request.args.get('next', None):
        return redirect(request.args.get('next'))
    else:
        return redirect(url_for('home.index'))
