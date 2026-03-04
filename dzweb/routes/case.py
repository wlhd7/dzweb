from flask import Blueprint, render_template, request, jsonify, redirect, url_for, g
from dzweb.db import (
    get_case_modules, get_case_module_by_slug, create_case_module,
    update_case_module, delete_case_module, get_case_contents,
    add_case_content, update_case_content, delete_case_content,
    get_db
)
from dzweb.routes.admin import login_required
from dzweb.utils.image import generate_thumbnail, convert_to_webp
import os
import uuid
from flask import current_app
from deep_translator import GoogleTranslator
import re

bp = Blueprint('case', __name__, url_prefix='/case')

def auto_translate(text, target_lang):
    if not text:
        return ""
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        current_app.logger.error(f"Translation error ({target_lang}): {str(e)}")
        return text

def slugify(text):
    # Convert to lowercase and replace non-alphanumeric characters with dashes
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename) -> bool:
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_random_filename(original_filename) -> str:
    ext = os.path.splitext(original_filename)[1]
    return f'{uuid.uuid4().hex}{ext}'

def _delete_case_image_files(filename):
    if not filename:
        return
    
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], filename)
    base_name = os.path.splitext(filename)[0]
    webp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{base_name}.webp")
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(thumb_path):
            os.remove(thumb_path)
        if os.path.exists(webp_path):
            os.remove(webp_path)
    except Exception as e:
        current_app.logger.error(f"Error deleting case image files for {filename}: {str(e)}")

@bp.route('/')
def main():
    """主经典案例页面，自动重定向到第一个案例。"""
    modules = get_case_modules()
    if modules:
        return redirect(url_for('case.display_case', slug=modules[0]['slug']))
    return render_template('case/main.html', modules=modules)

@bp.route('/<slug>')
def display_case(slug):
    module = get_case_module_by_slug(slug)
    if not module:
        abort(404)
        
    modules = get_case_modules()
    contents = get_case_contents(module['id'])
    return render_template('case/display.html', module=module, modules=modules, contents=contents)

# --- Management API ---

@bp.route('/api/module', methods=['POST'])
@login_required
def api_create_module():
    title_zh = request.form.get('title_zh')
    if not title_zh:
        return jsonify({'error': 'Missing title'}), 400

    slug = request.form.get('slug')
    if not slug:
        # 1. Translate Chinese title to English
        english_title = auto_translate(title_zh, 'en')
        # 2. Format as standard slug
        slug = slugify(english_title)
        
        # 3. Handle collision or empty slug (if translation failed or resulted in no alphanumeric)
        if not slug or get_case_module_by_slug(slug):
            import time
            slug = f"{slug or 'case'}-{int(time.time())}"
        
    create_case_module(slug, title_zh, None, None)
    return jsonify({'status': 'success'})

@bp.route('/api/module/<int:id>/delete', methods=['POST'])
@login_required
def api_delete_module(id):
    # Fetch all contents of this module to cleanup physical files
    contents = get_case_contents(id)
    for content in contents:
        if content['type'] == 'image':
            _delete_case_image_files(content['filename'])
            
    delete_case_module(id)
    return jsonify({'status': 'success'})

@bp.route('/api/module/<int:case_id>/content', methods=['POST'])
@login_required
def api_add_content(case_id):
    content_type = request.form.get('type')
    content_zh = request.form.get('content_zh')
    sort_order = request.form.get('sort_order', 0)
    
    filename = None
    if content_type == 'image':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            filename = generate_random_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Generate thumbnail
            thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], filename)
            try:
                generate_thumbnail(file_path, thumb_path)
            except Exception as e:
                current_app.logger.error(f"Failed to generate thumbnail for case image {filename}: {str(e)}")

            # Generate WebP version
            try:
                convert_to_webp(file_path, quality=80)
            except Exception as e:
                current_app.logger.error(f"Failed to generate WebP for case image {filename}: {str(e)}")
        else:
            return jsonify({'error': 'Invalid file type or no file uploaded'}), 400
    
    add_case_content(case_id, content_type, content_zh, None, None, filename, sort_order)
    return jsonify({'status': 'success'})

@bp.route('/api/content/<int:id>/delete', methods=['POST'])
@login_required
def api_delete_content(id):
    db = get_db()
    content = db.execute('SELECT * FROM case_contents WHERE id = ?', (id,)).fetchone()
    if content and content['type'] == 'image':
        _delete_case_image_files(content['filename'])
        
    delete_case_content(id)
    return jsonify({'status': 'success'})

@bp.route('/api/content/<int:id>/move/<direction>', methods=['POST'])
@login_required
def api_move_content(id, direction):
    db = get_db()
    content = db.execute('SELECT * FROM case_contents WHERE id = ?', (id,)).fetchone()
    if not content:
        return jsonify({'error': 'Content not found'}), 404
        
    case_id = content['case_id']
    current_order = content['sort_order']
    
    if direction == 'up':
        neighbor = db.execute(
            'SELECT * FROM case_contents WHERE case_id = ? AND sort_order < ? ORDER BY sort_order DESC LIMIT 1',
            (case_id, current_order)
        ).fetchone()
    else:
        neighbor = db.execute(
            'SELECT * FROM case_contents WHERE case_id = ? AND sort_order > ? ORDER BY sort_order ASC LIMIT 1',
            (case_id, current_order)
        ).fetchone()
        
    if neighbor:
        db.execute('UPDATE case_contents SET sort_order = ? WHERE id = ?', (neighbor['sort_order'], content['id']))
        db.execute('UPDATE case_contents SET sort_order = ? WHERE id = ?', (current_order, neighbor['id']))
        db.commit()
        
    return jsonify({'status': 'success'})

@bp.route('/api/module/<int:id>/update', methods=['POST'])
@login_required
def api_update_module(id):
    title_zh = request.form.get('title_zh')
    if not title_zh:
        return jsonify({'error': 'Missing title'}), 400
        
    db = get_db()
    db.execute('UPDATE case_modules SET title_zh = ? WHERE id = ?', (title_zh, id))
    db.commit()
    return jsonify({'status': 'success'})

@bp.route('/api/content/<int:id>/update', methods=['POST'])
@login_required
def api_update_content(id):
    db = get_db()
    content = db.execute('SELECT * FROM case_contents WHERE id = ?', (id,)).fetchone()
    if not content:
        return jsonify({'error': 'Content not found'}), 404
        
    content_type = content['type']
    
    if content_type == 'text':
        content_zh = request.form.get('content_zh')
        db.execute('UPDATE case_contents SET content_zh = ? WHERE id = ?', (content_zh, id))
        db.commit()
    elif content_type == 'image':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            # 1. Save new image
            new_filename = generate_random_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            
            # 2. Generate thumbnail and webp for new image
            thumb_path = os.path.join(current_app.config['THUMBNAIL_FOLDER'], new_filename)
            try:
                generate_thumbnail(file_path, thumb_path)
                convert_to_webp(file_path, quality=80)
            except Exception as e:
                current_app.logger.error(f"Image processing error during update: {str(e)}")
            
            # 3. Delete old physical files
            _delete_case_image_files(content['filename'])
            
            # 4. Update database
            db.execute('UPDATE case_contents SET filename = ? WHERE id = ?', (new_filename, id))
            db.commit()
        else:
            return jsonify({'error': 'No valid file uploaded'}), 400
            
    return jsonify({'status': 'success'})
