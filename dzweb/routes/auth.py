from flask import Blueprint, render_template, redirect, url_for, session, flash, g, request
from dzweb.db import get_db
from functools import wraps
import bcrypt
from flask_babel import _


bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash(_('请先登陆用户'))

            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id', None)

    if user_id is None:
        g.pop('user', None)
    else:
        g.user = get_db().execute(
                'SELECT * FROM users WHERE id = ?',
                (user_id,)
            ).fetchone()


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        try:
            salt = bcrypt.gensalt(rounds=12)
            hashed_password = bcrypt.hashpw(
                    password.encode('utf-8'),
                    salt
                ).decode('utf-8')

            db.execute(
                    'INSERT INTO users (username, password) VALUES (?, ?)',
                    (username, hashed_password)
                )
            db.commit()
        except db.IntegrityError:
            flash(_(f'用户 {username} 已经被注册，请使用不同的用户名.'))
        else:
            flash(f'用户 {username} 注册成功。')

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        user = db.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()

        if 'user' in g:
            flash(_('用户已登陆, 请查看右上角'))

            return redirect(url_for('auth.login'))

        if user is None:
            flash(_('用户不存在.'))
        elif not bcrypt.checkpw(
                password.encode('utf-8'),
                user['password'].encode('utf-8')
            ):
            flash(_('密码错误.'))
        else:
            session['user_id'] = user['id']

            return redirect(url_for('user.add_app'))

    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    g.pop('user', None)

    if request.args.get('next', None):
        return redirect(request.args.get('next'))
    else:
        return redirect(url_for('home.main'))
