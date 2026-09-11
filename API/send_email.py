import os 
from fastapi_mail import FastMail , MessageSchema , ConnectionConfig
from dotenv import load_dotenv

from schemas import User

load_dotenv()

class Envs:
    MAIL_USERNAME =os.getenv("MAIL_USERNAME" , "")
    MAIL_PASSWORD =os.getenv("MAIL_PASSWORD" , "")
    MAIL_FROM =os.getenv("MAIL_FROM" , "")
    MAIL_PORT =os.getenv("MAIL_PORT" , "")
    MAIL_SERVER =os.getenv("MAIL_SERVER" , "")
    MAIL_FROM_NAME =os.getenv("MAIL_FROM_NAME" , "")

conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=Envs.MAIL_PORT,
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_FROM_NAME=Envs.MAIL_FROM_NAME,

    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,

    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="templates"
)

async def send_registeration_mail(subject : str , email_to : str , body : dict):
    print("📧 Starting email sending...")
    print("To:", email_to)
    print("From:", Envs.MAIL_FROM)
    message = MessageSchema(
        subject=subject , 
        recipients=[email_to] ,
        template_body=body,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message=message , template_name="email.html")

    print("✅ Email sent successfully!")


