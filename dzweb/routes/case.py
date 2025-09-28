from flask import Blueprint, render_template


bp = Blueprint('case', __name__, url_prefix='/case')


@bp.route('/')
def extruder():
    return render_template('case/extruder.html')


@bp.route('/assembly-line')
def assembly_line():
    return render_template('case/assembly-line.html')


@bp.route('/ass')
def ass():
    return render_template('case/ass.html')


@bp.route('/robot-welding')
def robot_welding():
    return render_template('case/robot-welding.html')
