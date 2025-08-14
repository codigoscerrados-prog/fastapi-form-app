from app.utils.email_utils import send_confirmation_email
from app.utils.token_utils import generate_confirmation_token

@router.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Validación y creación del usuario
    new_user = User(**user_data.dict(), is_confirmed=False)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = generate_confirmation_token(new_user.email)
    await send_confirmation_email(new_user.email, new_user.username, token)

    return {"message": "Usuario creado. Revisa tu correo para confirmar tu cuenta."}