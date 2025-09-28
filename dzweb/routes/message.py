from flask import Blueprint, render_template, request, redirect, url_for, g
from dzweb.db import get_db
from flask_babel import _

bp = Blueprint('message', __name__, url_prefix='/message')


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        message = request.form['message']
        author_id = g.user['id'] if 'user' in g else 0
        db = get_db()

        db.execute(
                'INSERT INTO messages (message, author_id) VALUES (?, ?)',
                (message, author_id)
            )
        db.commit()

        return redirect(url_for('message.message_board'))

    return render_template('message/create.html')


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    db = get_db()

    if request.method == 'POST':
        message = request.form['message']

        db.execute(
                'UPDATE messages SET message = ? WHERE id = ?',
                (message, id)
            )
        db.commit()

        return redirect(url_for('message.message_board'))

    message = db.execute(
            'SELECT * FROM messages WHERE id = ?',
            (id,)
        ).fetchone()

    return render_template('message/update.html', message=message)


@bp.route('/<int:id>/delete')
def delete(id):
    db = get_db()
    db.execute(
            'DELETE FROM messages WHERE id = ?',
            (id,)
        )
    db.commit()

    return redirect(url_for('message.message_board'))


@bp.route('/message-board', methods=['GET', 'POST'])
def message_board():
    messages = get_db().execute(
            'SELECT message, m.id, COALESCE(u.username, ?) as username, created, color'
            ' FROM messages m LEFT JOIN users u ON m.author_id = u.id'
            ' ORDER BY created DESC',
            (_('匿名'),)
        ).fetchall()

    return render_template('message/message-board.html', messages=messages)


@bp.route('/', methods=['GET', 'POST'])
def mailbox():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        liaison = request.form['liaison']
        unit = request.form['unit']
        address = request.form['address']
        telephone = request.form['telephone']
        mobilephone = request.form['mobilephone']
        mail = request.form['mail']

        return redirect(url_for('message.mailbox'))

    return render_template('message/mailbox.html')
