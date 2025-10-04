from flask_mail import Mail, Message
from flask import current_app
from datetime import datetime

mail = Mail()


def init_mail(app):
	mail.init_app(app)
	app.logger.info("邮件扩展初始化完成")


def send_email(subject, recipients, body, html=None, reply_to=None, cc=None, bcc=None):
    """发送邮件的工具函数"""
    try:
        if not current_app.config.get('MAIL_SERVER'):
            current_app.logger.error("邮件服务器未配置")
            return False
        
        msg = Message(
            subject=subject,
            recipients=recipients,
            body=body,
            html=html,
            sender=current_app.config.get('MAIL_DEFAULT_SENDER')
        )
        
        if reply_to:
            msg.reply_to = reply_to
        if cc:
            msg.cc = cc
        if bcc:
            msg.bcc = bcc
            
        mail.send(msg)
        current_app.logger.info(f"邮件发送成功: {subject} -> {recipients}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"发送邮件失败: {str(e)}", exc_info=True)
        return False

def send_feedback_email(title, content, liaison, unit, address, telephone, mobilephone, mail_address):
    """发送反馈邮件"""
    # 构建邮件内容
    email_body = f"""
新的客户反馈信息：

主题：{title}

内容：
{content}

联系人信息：
- 联系人：{liaison}
- 单位：{unit}
- 地址：{address or '未填写'}
- 电话：{telephone or '未填写'}
- 手机：{mobilephone or '未填写'}
- 邮箱：{mail_address}

收到时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # HTML格式内容
    email_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>客户反馈</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .section {{ margin-bottom: 15px; }}
        .label {{ font-weight: bold; }}
        .content {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h2>新的客户反馈信息</h2>
    
    <div class="section">
        <div class="label">主题：</div>
        <div class="content">{title}</div>
    </div>
    
    <div class="section">
        <div class="label">内容：</div>
        <div class="content" style="white-space: pre-wrap; background: #f5f5f5; padding: 10px; border-radius: 5px;">{content}</div>
    </div>
    
    <div class="section">
        <h3>联系人信息</h3>
        <p><strong>联系人：</strong>{liaison}</p>
        <p><strong>单位：</strong>{unit}</p>
        <p><strong>地址：</strong>{address or '未填写'}</p>
        <p><strong>电话：</strong>{telephone or '未填写'}</p>
        <p><strong>手机：</strong>{mobilephone or '未填写'}</p>
        <p><strong>邮箱：</strong>{mail_address}</p>
    </div>
    
    <div class="section">
        <p><em>收到时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    </div>
</body>
</html>
"""
    
    # 获取收件人
    recipients = current_app.config.get('MAIL_ADMINS', [])
    if not recipients:
        admin_email = current_app.config.get('MAIL_ADMIN')
        if admin_email:
            recipients = [admin_email]
        else:
            current_app.logger.error("未配置管理员邮箱")
            return False
    
    return send_email(
        subject=f"网站反馈 - {title}",
        recipients=recipients,
        body=email_body,
        html=email_html,
        reply_to=mail_address
    )
