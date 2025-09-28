from flask import Blueprint, render_template, redirect, url_for, request


bp = Blueprint('about', __name__, url_prefix='/about')


@bp.route('/')
def introduction():
    return render_template('about/introduction.html')


@bp.route('/history')
def history():
    return render_template('about/history.html')


@bp.route('/organization')
def organization():
    return render_template('about/organization.html')


@bp.route('/strategy')
def strategy():
    return render_template('about/strategy.html')


@bp.route('/performance')
def performance():
    return render_template('about/performance.html')


@bp.route('/style')
def style():
    return render_template('about/style.html')
