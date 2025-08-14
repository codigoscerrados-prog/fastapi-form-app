# app/utils/email_utils.py
import os
from email.message import EmailMessage
import aiosmtplib

async def send_confirmation_email(to_email: str, username: str, token: str):
    try:
        message = EmailMessage()
        message["From"] = os.getenv("SMTP_USER")
        message["To"] = to_email
        message["Subject"] = "Confirma tu cuenta"

        # Enlace de confirmación
        link = f"https://{os.getenv('RENDER_EXTERNAL_URL')}/confirm?token={token}"

        # Contenido HTML del correo
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Hola {username},</h2>
            <p>Gracias por registrarte. Haz clic en el botón para confirmar tu cuenta:</p>
            <a href="{link}" style="padding: 10px 20px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px;">Confirmar cuenta</a>
            <p style="margin-top: 20px; font-size: 12px; color: #888;">Si no solicitaste este registro, puedes ignorar este mensaje.</p>
        </body>
        </html>
        """

        # Versión de texto plano (por si el cliente no soporta HTML)
        message.set_content(f"Hola {username}, confirma tu cuenta aquí: {link}")
        message.add_alternative(html_content, subtype="html")

        # Envío del correo
        await aiosmtplib.send(
            message,
            hostname=os.getenv("SMTP_HOST"),
            port=int(os.getenv("SMTP_PORT")),
            username=os.getenv("SMTP_USER"),
            password=os.getenv("SMTP_PASSWORD"),
            start_tls=True,
        )
        print("✅ Correo enviado correctamente a", to_email)

    except Exception as e:
        print("❌ Error al enviar correo:", e)