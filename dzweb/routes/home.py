from flask import Blueprint, render_template, redirect, url_for, session
from dzweb.db import get_db


bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/')
def main():
    products = get_db().execute(
            'SELECT id, productname, filename FROM products'
            ' ORDER BY id DESC LIMIT 8',
        ).fetchall()

    return render_template('home/main.html', products=products)



