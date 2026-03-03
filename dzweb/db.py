import sqlite3
from flask import current_app, g
import click
from datetime import datetime


def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
                current_app.config['DATABASE'],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
        g.db.row_factory=sqlite3.Row

    return g.db


def get_all_apps():
    db = get_db()
    return db.execute('SELECT * FROM apps').fetchall()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_database():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


@click.command('init-db')
def init_db_command():
    init_database()
    click.echo('Initialized the database')


sqlite3.register_converter('timestamp', lambda v: datetime.fromisoformat(v.decode()))


def init_db(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# Case Modular CRUD

def get_case_modules():
    db = get_db()
    return db.execute('SELECT * FROM case_modules ORDER BY created DESC').fetchall()


def get_case_module_by_slug(slug):
    db = get_db()
    return db.execute('SELECT * FROM case_modules WHERE slug = ?', (slug,)).fetchone()


def create_case_module(slug, title_zh, title_en=None, title_ja=None):
    db = get_db()
    db.execute(
        'INSERT INTO case_modules (slug, title_zh, title_en, title_ja) VALUES (?, ?, ?, ?)',
        (slug, title_zh, title_en, title_ja)
    )
    db.commit()


def update_case_module(id, slug, title_zh, title_en=None, title_ja=None):
    db = get_db()
    db.execute(
        'UPDATE case_modules SET slug = ?, title_zh = ?, title_en = ?, title_ja = ? WHERE id = ?',
        (slug, title_zh, title_en, title_ja, id)
    )
    db.commit()


def delete_case_module(id):
    db = get_db()
    db.execute('DELETE FROM case_modules WHERE id = ?', (id,))
    db.commit()


def get_case_contents(case_id):
    db = get_db()
    return db.execute('SELECT * FROM case_contents WHERE case_id = ? ORDER BY sort_order ASC', (case_id,)).fetchall()


def add_case_content(case_id, type, content_zh=None, content_en=None, content_ja=None, filename=None, sort_order=0):
    db = get_db()
    db.execute(
        'INSERT INTO case_contents (case_id, type, content_zh, content_en, content_ja, filename, sort_order) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (case_id, type, content_zh, content_en, content_ja, filename, sort_order)
    )
    db.commit()


def update_case_content(id, type, content_zh=None, content_en=None, content_ja=None, filename=None, sort_order=0):
    db = get_db()
    db.execute(
        'UPDATE case_contents SET type = ?, content_zh = ?, content_en = ?, content_ja = ?, filename = ?, sort_order = ? WHERE id = ?',
        (type, content_zh, content_en, content_ja, filename, sort_order, id)
    )
    db.commit()


def delete_case_content(id):
    db = get_db()
    db.execute('DELETE FROM case_contents WHERE id = ?', (id,))
    db.commit()
