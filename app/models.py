# models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base

class LoginUser(Base):
    __tablename__ = "login_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    email = Column(String(150), unique=True, index=True)
    password = Column(String(255))
    is_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())