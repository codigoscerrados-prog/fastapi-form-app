from pydantic import BaseModel, EmailStr
from datetime import date

class LoginUserCreate(BaseModel):
    username: str
    password: str