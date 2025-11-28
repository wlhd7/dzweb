from flask import Blueprint, render_template, request, redirect, url_for, g, current_app, flash
from dzweb.db import get_db
from flask_babel import _
from dzweb.mail import send_feedback_email


bp = Blueprint('contact', __name__, url_prefix='/contact')


@bp.route('/')
def contact_us():
    return render_template('contact/contact-us.html')


@bp.route('/location')
def location():
    return render_template('contact/location.html')


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        message = request.form['message']
        author_id = g.user['id'] if 'user' in g else 0
        db = get_db()

        db.execute(
                'INSERT INTO messages (message, author_id) VALUES (?, ?)',
                (message, author_id)
            )
        db.commit()

        return redirect(url_for('contact.message_board'))

    return render_template('contact/create.html')


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    db = get_db()

    if request.method == 'POST':
        message = request.form['message']

        db.execute(
                'UPDATE messages SET message = ? WHERE id = ?',
                (message, id)
            )
        db.commit()

        return redirect(url_for('contact.message_board'))

    message = db.execute(
            'SELECT * FROM messages WHERE id = ?',
            (id,)
        ).fetchone()

    return render_template('contact/update.html', message=message)


@bp.route('/<int:id>/delete')
def delete(id):
    db = get_db()
    db.execute(
            'DELETE FROM messages WHERE id = ?',
            (id,)
        )
    db.commit()

    return redirect(url_for('contact.message_board'))


@bp.route('/message-board', methods=['GET', 'POST'])
def message_board():
    messages = get_db().execute(
            'SELECT message, m.id, COALESCE(u.username, ?) as username, created, color'
            ' FROM messages m LEFT JOIN users u ON m.author_id = u.id'
            ' ORDER BY created DESC',
            (_('匿名'),)
        ).fetchall()

    return render_template('contact/message-board.html', messages=messages)


@bp.route('/mailbox', methods=['GET', 'POST'])
def mailbox():
    if request.method == 'POST':
        try:
            # 获取表单数据
            title = request.form.get('title', '').strip()
            content = request.form.get('content', '').strip()
            liaison = request.form.get('liaison', '').strip()
            unit = request.form.get('unit', '').strip()
            address = request.form.get('address', '').strip()
            telephone = request.form.get('telephone', '').strip()
            mobilephone = request.form.get('mobilephone', '').strip()
            mail_address = request.form.get('mail', '').strip()
            
            current_app.logger.info(f"收到反馈表单: {title}, 联系人: {liaison}, 邮箱: {mail_address}")
            
            # 验证必填字段
            if not all([title, content, liaison, unit, mail_address]):
                flash('请填写所有必填字段', 'error')
                return render_template('contact/mailbox.html')
            
            # 验证邮箱格式
            if '@' not in mail_address:
                flash('请输入有效的邮箱地址', 'error')
                return render_template('contact/mailbox.html')
            
            # 发送邮件
            success = send_feedback_email(
                title=title,
                content=content,
                liaison=liaison,
                unit=unit,
                address=address,
                telephone=telephone,
                mobilephone=mobilephone,
                mail_address=mail_address
            )
            
            if success:
                flash('感谢您的反馈，我们会尽快处理！', 'success')
            else:
                flash('邮件发送失败，请稍后重试或联系管理员', 'error')
            
        except Exception as e:
            current_app.logger.error(f"处理反馈表单失败: {str(e)}", exc_info=True)
            flash('系统错误，请稍后重试', 'error')
        
        return render_template('contact/mailbox.html')
    
    return render_template('contact/mailbox.html')
