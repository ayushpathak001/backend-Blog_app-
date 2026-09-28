import os
from pathlib import Path
from typing import Dict 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

load_dotenv()

class Envs:
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")   # Your ahssejebe@gmail.com
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")   # Your 16-character Google App Password
    MAIL_FROM = os.getenv("MAIL_FROM", "")           # Your ahssejebe@gmail.com
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Blog App")

# Set up Jinja2 templates folder mapping
BASE_DIR = Path(__file__).resolve().parent
templates_dir = BASE_DIR / "templates"
jinja_env = Environment(loader=FileSystemLoader(templates_dir))

def render_template(template_name: str, context: dict) -> str:
    """Compiles HTML template files with Python dictionary contexts."""
    template = jinja_env.get_template(template_name)
    return template.render(context)

def send_ssl_email(subject: str, email_to: str, html_content: str):
    """Sends emails via Gmail using Port 465 (SSL) which bypasses Render's firewall."""
    
    # 1. Setup email headers and content structures
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = f"{Envs.MAIL_FROM_NAME} <{Envs.MAIL_FROM}>"
    message["To"] = email_to

    # Turn the template HTML into a sendable mime part
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    # 2. Open an SSL Connection to Gmail (Port 465 is open on Render!)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(Envs.MAIL_USERNAME, Envs.MAIL_PASSWORD)
            server.sendmail(Envs.MAIL_FROM, email_to, message.as_string())
        print(f"✅ Email successfully delivered to {email_to} via Gmail SSL!")
    except Exception as e:
        print(f"❌ Gmail Connection Failure: {e}")
        raise e

async def send_registeration_mail(subject: str, email_to: str, body: dict):
    print(f"📧 Launching registration template email to {email_to}...")
    html_content = render_template("email.html", body)
    send_ssl_email(subject, email_to, html_content)

async def password_reset(subject: str, email_to: str, body: Dict):
    print(f"📧 Launching password reset template email to {email_to}...")
    html_content = render_template("password_reset.html", body)
    send_ssl_email(subject, email_to, html_content)
