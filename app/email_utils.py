import smtplib
from email.message import EmailMessage
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

def send_confirmation_email(to_email):
    msg = EmailMessage()
    msg["Subject"] = "Confirmación de registro"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content("Gracias por registrarte. ¡Tu información fue recibida!")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)