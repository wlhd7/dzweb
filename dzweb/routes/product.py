from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from dzweb.db import get_db
import uuid
import os
from flask_babel import _
from dzweb.routes.auth import login_required
from werkzeug.exceptions import abort
import math


bp = Blueprint('product', __name__, url_prefix='/product')


ALLOWED_EXTENSIONS = {'png', 'jpg'}


def allowed_file(filename) -> bool:
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def generate_random_filename(original_filename) -> str:
    ext = os.path.splitext(original_filename)[1]
    random_name = f'{uuid.uuid4().hex}{ext}'

    return random_name

def edit_product_permission_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        pass


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        productname = request.form['productname']
        brief = request.form['brief']
        category = request.form['category']
        file = request.files['file']

        if allowed_file(file.filename):
            random_filename = generate_random_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], random_filename))
            db = get_db()

            db.execute(
                    'INSERT INTO products (productname, brief, category, filename) VALUES (?, ?, ?, ?)',
                    (productname, brief, category, random_filename)
                )
            db.commit()
        else:
            flash(_('抱歉，图片格式限制，请上传文件扩展名为 jpg 或 png 的图片'))

        return redirect(url_for(f'product.{category}'))

    return render_template('product/create.html')


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    db = get_db()

    if request.method == 'POST':
        productname = request.form['productname']
        brief = request.form['brief']
        category = request.form['category']

        db.execute(
                'UPDATE products SET productname = ?, brief = ?, category = ? WHERE id = ?',
                (productname, brief, category, id)
            )
        db.commit()

        return redirect(request.args.get('next'))

    product = db.execute(
            'SELECT id, productname, brief, created, category FROM products'
            ' WHERE id = ?',
            (id,)
        ).fetchone()

    if product is None:
        abort(404, f"Product id {id} doesn't exist")

    return render_template('product/update.html', product=product)


@bp.route('/<int:id>/delete')
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM products WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('product.equipment'))


@bp.route('/<int:id>/display')
def display(id):
    product = get_db().execute(
            'SELECT * FROM products WHERE id = ?',
            (id,)
        ).fetchone()

    if product is None:
        abort(404, f"Product id {id} doesn't exist")

    path = os.path.join(current_app.config['UPLOAD_FOLDER'], product['filename'])

    return render_template('product/display.html', product=product, path=path)


def get_page(category):
    all_products = get_db().execute(
            'SELECT id, productname, filename FROM products WHERE category = ?'
            ' ORDER BY created DESC',
            (category,)
        ).fetchall()

    page = request.args.get('page', 1, type=int)
    per_page = 9

    total_products = len(all_products)
    total_pages = math.ceil(total_products / per_page)

    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    products = all_products[start_idx:end_idx]

    return render_template(
            f'product/{category}.html',
            products=products,
            path=current_app.config['UPLOAD_FOLDER'],
            page=page,
            total_pages=total_pages
        )



@bp.route('/equipment')
def equipment():
    return get_page('equipment')


@bp.route('/fixture')
def fixture():
    return get_page('fixture')


@bp.route('/automation')
def automation():
    return get_page('automation')


@bp.route('/non-standard')
def non_standard():
    return get_page('non-standard')


@bp.route('/robotics')
def robotics():
    return get_page('robotics')
