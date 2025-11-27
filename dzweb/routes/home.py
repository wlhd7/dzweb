from flask import Blueprint, render_template, redirect, url_for, request
from dzweb.db import get_db


bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    products = get_db().execute(
        'SELECT id, productname, filename FROM products'
        ' ORDER BY id DESC LIMIT 16',
    ).fetchall()

    return render_template('home/index.html', products=products)


@bp.route('/introduction')
def introduction():
    return render_template('home/introduction.html')


@bp.route('/history')
def history():
    return render_template('home/history.html')


@bp.route('/organization')
def organization():
    return render_template('home/organization.html')


@bp.route('/strategy')
def strategy():
    return render_template('home/strategy.html')


@bp.route('/performance')
def performance():
    return render_template('home/performance.html')


@bp.route('/style')
def style():
    return render_template('home/style.html')