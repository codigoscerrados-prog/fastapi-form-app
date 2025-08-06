from pydantic import BaseModel, EmailStr
from datetime import date

class UserCreate(BaseModel):
    name: str
    address: str
    birth_date: date
    gender: str
    phone: str
    email: EmailStr