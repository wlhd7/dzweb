from flask import Blueprint, render_template

bp = Blueprint('case', __name__, url_prefix='/case')

@bp.route('/')
def main():
    """主经典案例页面，目前合并为单一空白页。"""
    return render_template('case/main.html')
