import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

server = os.getenv("MAIL_SERVER")
port = int(os.getenv("MAIL_PORT"))
user = os.getenv("MAIL_USERNAME")
pwd = os.getenv("MAIL_PASSWORD")
use_tls = os.getenv("MAIL_USE_TLS").lower() in ('true', '1')

print(f"Diagnostics: Server={server}, Port={port}, User={user}, TLS={use_tls}")

try:
    print("Connecting...")
    smtp = smtplib.SMTP(server, port, timeout=10)
    if use_tls:
        print("Starting TLS...")
        smtp.starttls()
    print("Logging in...")
    smtp.login(user, pwd)
    print("Login SUCCESS!")
    
    msg = MIMEText("This is a diagnostic email from your website.")
    msg["Subject"] = "Diagnostic Test"
    msg["From"] = user
    msg["To"] = user
    
    smtp.sendmail(user, [user], msg.as_string())
    print("Email sent successfully!")
    smtp.quit()
except Exception as e:
    print(f"ERROR: {str(e)}")
