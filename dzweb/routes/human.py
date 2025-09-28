from flask import Blueprint, render_template, request, redirect, url_for
from dzweb.db import get_db


bp = Blueprint('human', __name__, url_prefix='/human')


@bp.route('/create-position', methods=['GET', 'POST'])
def create_position():
    if request.method == 'POST':
        position = request.form['position']
        salary = request.form['salary']
        requirement = request.form['requirement']
        db = get_db()

        db.execute(
                'INSERT INTO positions (position, salary, requirement) VALUES (?, ?, ?)',
                (position, salary, requirement)
            )
        db.commit()

        return redirect(url_for('human.hire'))

    return render_template('human/create.html')


@bp.route('/<int:id>/update-position', methods=['GET', 'POST'])
def update_position(id):
    db = get_db()

    if request.method == 'POST':
        position = request.form['position']
        salary = request.form['salary']
        requirement = request.form['requirement']

        db.execute(
                'UPDATE positions SET position = ?, salary = ?, requirement = ?'
                ' WHERE id = ?',
                (position, salary, requirement, id)
            )
        db.commit()

        return redirect(url_for('human.hire'))

    position = db.execute(
            'SELECT * FROM positions WHERE id = ?',
            (id,)
        ).fetchone()

    return render_template('human/update.html', position=position)


@bp.route('/<int:id>/delete-position')
def delete_position(id):
    db = get_db()
    db.execute(
            'DELETE FROM positions where id = ?',
            (id,)
        )
    db.commit()

    return redirect(url_for('human.hire'))



@bp.route('/')
def hire():
    positions = get_db().execute(
            'SELECT * FROM positions'
            ' ORDER BY created DESC',
        ).fetchall()

    return render_template('human/hire.html', positions=positions)


@bp.route('/idea')
def idea():
    return render_template('human/idea.html')
