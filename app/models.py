from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    address = Column(String)
    birth_date = Column(Date)
    gender = Column(String)
    phone = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Relación con el usuario que creó el registro
    creador_id = Column(Integer, ForeignKey("login_users.id"))
    creador = relationship("LoginUser", back_populates="registros")


class LoginUser(Base):
    __tablename__ = "login_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    # Relación inversa
    registros = relationship("User", back_populates="creador")