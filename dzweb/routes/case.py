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

bp = Blueprint('case', __name__, url_prefix='/case')

def auto_translate(text, target_lang):
    if not text:
        return ""
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        current_app.logger.error(f"Translation error ({target_lang}): {str(e)}")
        return text # Fallback

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
    """主经典案例页面，目前合并为单一空白页。"""
    modules = get_case_modules()
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
    # If slug is not provided, generate from title_zh (using simple UUID for now as placeholder or slugify if we had it)
    # The requirement says 'automatic generate', I will try a simple slug from title_zh
    # Actually, many systems just use the ID or a uuid if no slug is provided.
    slug = request.form.get('slug')
    if not slug:
        import uuid
        slug = f"case-{uuid.uuid4().hex[:8]}"
        
    title_en = request.form.get('title_en') or auto_translate(title_zh, 'en')
    title_ja = request.form.get('title_ja') or auto_translate(title_zh, 'ja')
    
    if not title_zh:
        return jsonify({'error': 'Missing title'}), 400
        
    create_case_module(slug, title_zh, title_en, title_ja)
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
    # Use auto_translate for missing translations
    content_en = request.form.get('content_en') or (auto_translate(content_zh, 'en') if content_type == 'text' else None)
    content_ja = request.form.get('content_ja') or (auto_translate(content_zh, 'ja') if content_type == 'text' else None)
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
    
    add_case_content(case_id, content_type, content_zh, content_en, content_ja, filename, sort_order)
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
