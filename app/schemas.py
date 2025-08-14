from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=150)
    password: constr(min_length=10, max_length=10)
    email: EmailStr
