import math
import os
import uuid
from functools import wraps

import requests
from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app, jsonify
from flask_babel import _
from werkzeug.exceptions import abort

from dzweb.db import get_db
from dzweb.routes.admin import login_required
from dzweb.utils.image import generate_thumbnail


def push_to_baidu(urls):
    """Baidu Active Push API helper."""
    token = current_app.config.get('BAIDU_PUSH_TOKEN')
    if not token or '您的' in token:
        current_app.logger.warning("BAIDU_PUSH_TOKEN not configured or still placeholder, skipping push.")
        return None
    
    api_url = f"http://data.zz.baidu.com/urls?site=https://www.dongzhen.cn&token={token}"
    try:
        response = requests.post(api_url, data="\n".join(urls), timeout=5)
        current_app.logger.info(f"Baidu Push Response: {response.text}")
        return response.json()
    except Exception as e:
        current_app.logger.error(f"Baidu Push Error: {str(e)}")
        return None


bp = Blueprint('product', __name__, url_prefix='/product')


ALLOWED_EXTENSIONS = {'png', 'jpg'}


SUBCATEGORIES = {
    'automation': [
        {'id': 'engine', 'name': '发动机'},
        {'id': 'transmission', 'name': '变速箱'},
        {'id': 'steeringGear', 'name': '转向系统'},
        {'id': 'automobileBearings', 'name': '汽车轴承'},
    ],
    'fixture': [
        {'id': 'engine', 'name': '发动机'},
        {'id': 'transmission', 'name': '变速箱'},
        {'id': 'steeringKnuckle', 'name': '转向节'},
        {'id': 'assemblyShop', 'name': '总装车间'},
    ],
    'non_standard': [],
    'robotics': [],
}


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
        # Placeholder for future permission logic
        return view(**kwargs)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        productname = request.form['productname'].strip()
        brief = request.form['brief']
        category = request.form['category']
        product_class = request.form.get('class', '')
        file = request.files['file']

        if allowed_file(file.filename):
            random_filename = generate_random_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], random_filename)
            file.save(file_path)
            
            # Generate thumbnail
            thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], random_filename)
            try:
                generate_thumbnail(file_path, thumb_path)
            except Exception as e:
                current_app.logger.error(f"Failed to generate thumbnail for {random_filename}: {str(e)}")

            db = get_db()

            db.execute(
                    'INSERT INTO products (productname, brief, category, filename, "class") VALUES (?, ?, ?, ?, ?)',
                    (productname, brief, category, random_filename, product_class)
                )
            # Fetch the just inserted ID to push its URL
            product_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
            db.commit()

            # Baidu Active Push
            product_url = url_for('product.display', id=product_id, _external=True)
            push_to_baidu([
                product_url,
                f"{product_url}?lang=en",
                f"{product_url}?lang=ja"
            ])
        else:
            flash('抱歉，图片格式限制，请上传文件扩展名为 jpg 或 png 的图片')

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
        product_class = request.form.get('class', '')
        file = request.files['file']
        # fetch existing product to preserve filename when no new file is provided
        existing = db.execute('SELECT filename FROM products WHERE id = ?', (id,)).fetchone()
        if existing is None:
            abort(404, f"Product id {id} doesn't exist")

        filename_to_use = existing['filename']
        old_filename = existing['filename']

        # if a new file was uploaded and has an allowed extension, save it and use new filename
        if file and file.filename:
            if allowed_file(file.filename):
                random_filename = generate_random_filename(file.filename)
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], random_filename)
                file.save(file_path)
                
                # Generate new thumbnail
                thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], random_filename)
                try:
                    generate_thumbnail(file_path, thumb_path)
                except Exception as e:
                    current_app.logger.error(f"Failed to generate thumbnail for {random_filename} during update: {str(e)}")
                
                filename_to_use = random_filename
            else:
                flash(_('抱歉，图片格式限制，请上传文件扩展名为 jpg 或 png 的图片'))
                return redirect(request.url)

        db.execute(
                'UPDATE products SET productname = ?, brief = ?, category = ?, filename = ?, "class" = ? WHERE id = ?',
                (productname, brief, category, filename_to_use, product_class, id)
            )
        db.commit()

        # If a new file was saved successfully, remove the old file
        if filename_to_use != old_filename:
            old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_filename)
            old_thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], old_filename)
            try:
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
                if os.path.exists(old_thumb_path):
                    os.remove(old_thumb_path)
            except Exception as e:
                current_app.logger.error(f"Error deleting old files for product {id} during update: {str(e)}")

        flash(_('产品已成功更新。'))
        return redirect(request.args.get('next'))

    product = db.execute(
            'SELECT id, productname, brief, created, category, "class" FROM products'
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
    product = db.execute('SELECT category, filename FROM products WHERE id = ?', (id,)).fetchone()
    
    if product:
        category = product['category']
        filename = product['filename']
        
        if filename:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], filename)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)
            except Exception as e:
                current_app.logger.error(f"Error deleting files for product {id}: {str(e)}")
                flash(_('删除图片文件失败，操作已取消。'))
                return redirect(url_for(f'product.{category}'))

        db.execute('DELETE FROM products WHERE id = ?', (id,))
        db.commit()
        flash(_('产品及其图片已成功删除。'))
        return redirect(url_for(f'product.{category}'))
    
    return redirect(url_for('home.index'))


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
    current_class = request.args.get('class', None)

    if current_class:
        all_products = get_db().execute(
            'SELECT id, productname, filename, "class" FROM products WHERE category = ? AND "class" = ? '
            'ORDER BY created DESC',
            (category, current_class)
        ).fetchall()
    else:
        all_products = get_db().execute(
            'SELECT id, productname, filename, "class" FROM products WHERE category = ? '
            'ORDER BY created DESC',
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
            total_pages=total_pages,
            current_class=current_class
        )



@bp.route('/fixture')
def fixture():
    return get_page('fixture')


@bp.route('/automation')
def automation():
    return get_page('automation')


@bp.route('/non_standard')
def non_standard():
    return get_page('non_standard')


@bp.route('/robotics')
def robotics():
    return get_page('robotics')


@bp.route('/search')
def search():
    """Simple product search by name or brief. Query with ?q=keyword."""
    q = request.args.get('q', '').strip()
    results = []
    if q:
        like = f"%{q}%"
        results = get_db().execute(
            'SELECT id, productname, filename, brief FROM products '
            'WHERE productname LIKE ? OR brief LIKE ? '
            'ORDER BY id DESC LIMIT 50',
            (like, like)
        ).fetchall()

    return render_template('product/search.html', q=q, results=results)


@bp.route('/api/subcategories/<category>')
def get_subcategories(category):
    subcategories = SUBCATEGORIES.get(category, [])
    return jsonify(subcategories)


import click
from flask.cli import with_appcontext

@click.command('cleanup-images')
@with_appcontext
def cleanup_images_command():
    """Remove image files that are not referenced in the database."""
    db = get_db()
    # Get all filenames referenced in the database
    products = db.execute('SELECT filename FROM products').fetchall()
    referenced_filenames = {p['filename'] for p in products if p['filename']}
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    thumb_folder = current_app.config['THUMBNAIL_FOLDER']
    deleted_count = 0
    
    def cleanup_dir(directory):
        nonlocal deleted_count
        if not os.path.exists(directory):
            click.echo(f"Directory {directory} does not exist, skipping.")
            return

        files_in_folder = os.listdir(directory)
        for filename in files_in_folder:
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                if filename not in referenced_filenames:
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                        click.echo(f"Deleted orphan file: {file_path}")
                    except Exception as e:
                        current_app.logger.error(f"Failed to delete orphan file {file_path}: {str(e)}")
                        click.echo(f"Error deleting {filename}: {str(e)}", err=True)

    cleanup_dir(upload_folder)
    cleanup_dir(thumb_folder)

    click.echo(f"Deleted {deleted_count} orphan files.")

@click.command('generate-thumbs')
@with_appcontext
def generate_thumbs_command():
    """Generate thumbnails for all existing products if they don't exist."""
    db = get_db()
    products = db.execute('SELECT id, productname, filename FROM products').fetchall()
    
    upload_folder = current_app.config['UPLOAD_FOLDER']
    thumb_folder = current_app.config['THUMBNAIL_FOLDER']
    
    os.makedirs(thumb_folder, exist_ok=True)
    
    generated_count = 0
    skipped_count = 0
    error_count = 0
    
    for p in products:
        filename = p['filename']
        if not filename:
            continue
            
        file_path = os.path.join(upload_folder, filename)
        thumb_path = os.path.join(thumb_folder, filename)
        
        if not os.path.exists(file_path):
            click.echo(f"Original image missing for product {p['id']} ({p['productname']}): {filename}", err=True)
            skipped_count += 1
            continue
            
        if os.path.exists(thumb_path):
            # click.echo(f"Thumbnail already exists for product {p['id']}: {filename}")
            skipped_count += 1
            continue
            
        try:
            generate_thumbnail(file_path, thumb_path)
            generated_count += 1
            click.echo(f"Generated thumbnail for product {p['id']}: {filename}")
        except Exception as e:
            current_app.logger.error(f"Failed to generate thumbnail for product {p['id']}: {str(e)}")
            click.echo(f"Error generating thumbnail for {filename}: {str(e)}", err=True)
            error_count += 1

    click.echo(f"Thumbnails processing complete. Generated: {generated_count}, Skipped: {skipped_count}, Errors: {error_count}")

def init_app(app):
    app.cli.add_command(cleanup_images_command)
    app.cli.add_command(generate_thumbs_command)
