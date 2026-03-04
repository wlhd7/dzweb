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
    return redirect(url_for('.contact_us'), code=301)


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
                return render_template('contact/mailbox.html')
            
            # 验证邮箱格式
            if '@' not in mail_address:
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
                return render_template('contact/mailbox.html', success=True)
            else:
                # Silently handle email sending failure
                current_app.logger.error(f"Failed to send feedback email from {mail_address}.")
                # Log actual app config for debugging (be careful with passwords in real prod)
                current_app.logger.debug(f"Current MAIL_SERVER: {current_app.config.get('MAIL_SERVER')}")
                current_app.logger.debug(f"Current MAIL_PORT: {current_app.config.get('MAIL_PORT')}")

            
        except Exception as e:
            current_app.logger.error(f"处理反馈表单失败: {str(e)}", exc_info=True)
            # System error is handled silently on UI as requested
        
        return render_template('contact/mailbox.html')
    
    return render_template('contact/mailbox.html')
