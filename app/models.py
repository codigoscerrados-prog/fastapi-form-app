from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Time, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime

class LoginUser(Base):
    __tablename__ = "login_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    password = Column(String(10))