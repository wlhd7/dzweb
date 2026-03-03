from flask import Blueprint, render_template, request, jsonify, redirect, url_for, g
from dzweb.db import (
    get_case_modules, get_case_module_by_slug, create_case_module,
    update_case_module, delete_case_module, get_case_contents,
    add_case_content, update_case_content, delete_case_content,
    get_db
)
from dzweb.routes.admin import login_required

bp = Blueprint('case', __name__, url_prefix='/case')

@bp.route('/')
def main():
    """主经典案例页面，目前合并为单一空白页。"""
    modules = get_case_modules()
    return render_template('case/main.html', modules=modules)

# --- Management API ---

@bp.route('/api/module', methods=['POST'])
@login_required
def api_create_module():
    slug = request.form.get('slug')
    title_zh = request.form.get('title_zh')
    title_en = request.form.get('title_en')
    title_ja = request.form.get('title_ja')
    
    if not slug or not title_zh:
        return jsonify({'error': 'Missing slug or title'}), 400
        
    create_case_module(slug, title_zh, title_en, title_ja)
    return jsonify({'status': 'success'})

@bp.route('/api/module/<int:id>/delete', methods=['POST'])
@login_required
def api_delete_module(id):
    delete_case_module(id)
    return jsonify({'status': 'success'})

@bp.route('/api/module/<int:case_id>/content', methods=['POST'])
@login_required
def api_add_content(case_id):
    content_type = request.form.get('type')
    content_zh = request.form.get('content_zh')
    content_en = request.form.get('content_en')
    content_ja = request.form.get('content_ja')
    sort_order = request.form.get('sort_order', 0)
    
    # Filename will be handled in the next task with WebP logic
    filename = request.form.get('filename')
    
    add_case_content(case_id, content_type, content_zh, content_en, content_ja, filename, sort_order)
    return jsonify({'status': 'success'})

@bp.route('/api/content/<int:id>/delete', methods=['POST'])
@login_required
def api_delete_content(id):
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
