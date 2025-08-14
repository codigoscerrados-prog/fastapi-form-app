# app/utils/email_utils.py
from email.message import EmailMessage
import aiosmtplib
import os

async def send_confirmation_email(to_email: str, username: str, token: str):
    message = EmailMessage()
    message["From"] = os.getenv("SMTP_USER")
    message["To"] = to_email
    message["Subject"] = "Confirma tu cuenta"

    link = f"https://{os.getenv('RENDER_EXTERNAL_URL')}/confirm?token={token}"
    message.set_content(f"Hola {username}, confirma tu cuenta aquí: {link}")

    await aiosmtplib.send(
        message,
        hostname=os.getenv("SMTP_HOST"),
        port=int(os.getenv("SMTP_PORT")),
        username=os.getenv("SMTP_USER"),
        password=os.getenv("SMTP_PASSWORD"),
        start_tls=True,
    )