from app.utils.token_utils import confirm_token

@router.get("/confirm")
def confirm_email(token: str, db: Session = Depends(get_db)):
    email = confirm_token(token)
    if not email:
        return {"error": "Token inválido o expirado"}

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"error": "Usuario no encontrado"}

    user.is_confirmed = True
    db.commit()
    return {"message": "Cuenta confirmada correctamente"}