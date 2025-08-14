from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=150)
    email: EmailStr
    password: constr(min_length=6, max_length=255)

class UserLogin(BaseModel):
    username: str
    password: str