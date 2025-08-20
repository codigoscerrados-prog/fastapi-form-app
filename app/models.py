# models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship


class LoginUser(Base):
    __tablename__ = "login_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True)
    email = Column(String(150), unique=True, index=True)
    password = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
#19 DE AGOSTO 
class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    ruc = Column(String(20), unique=True, nullable=False)
    correo = Column(String(150))
    condicion_pago = Column(String(20))
    direccion_fiscal = Column(Text)
    direccion_envio_informe = Column(Text)
    direccion_envio_factura = Column(Text)
    correo_envio_factura = Column(String(150))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(PERU_TZ))
    updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(PERU_TZ))
    
    contactos = relationship("Contacto", back_populates="cliente", cascade="all, delete")
    tipo_documento_id = Column(Integer, ForeignKey("tipo_documento.id"))
    tipo_documento = relationship("TipoDocumento")

class Contacto(Base):
    __tablename__ = "contactos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    telefono = Column(String)
    correo = Column(String)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(PERU_TZ))
    updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(PERU_TZ))
    
    cliente = relationship("Cliente", back_populates="contactos")

class TipoDocumento(Base):
    __tablename__ = "tipo_documento"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(PERU_TZ))
    updated_at = Column(DateTime(timezone=True), onupdate=lambda: datetime.now(PERU_TZ))
