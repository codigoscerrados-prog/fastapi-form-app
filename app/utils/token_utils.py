# app/utils/token_utils.py
from itsdangerous import URLSafeTimedSerializer
import os

def generate_confirmation_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    return serializer.dumps(email, salt="email-confirm")

def confirm_token(token: str, expiration=3600):
    serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
    try:
        return serializer.loads(token, salt="email-confirm", max_age=expiration)
    except Exception:
        return None