import os
from app.utils.email_utils import send_confirmation_email
from app.utils.token_utils import generate_confirmation_token

@router.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Crear usuario
    new_user = User(**user_data.dict(), is_confirmed=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generar token
    token = generate_confirmation_token(new_user.email)

    # Construir link de confirmación
    base_url = os.getenv("RENDER_EXTERNAL_URL", "localhost:8000")
    link = f"https://{base_url}/confirm?token={token}"

    mensaje = ""
    try:
        await send_confirmation_email(new_user.email, new_user.username, token)
        mensaje = "Usuario creado y correo enviado"
    except Exception as e:
        print("❌ No se pudo enviar el correo:", e)
        mensaje = "Usuario creado, pero no se pudo enviar el correo"

    # Si estamos en desarrollo, devolver también el link
    if os.getenv("DEBUG", "false").lower() == "true" or base_url.startswith("localhost"):
        return {
            "message": mensaje,
            "confirmation_link": link
        }

    return {"message": mensaje}
