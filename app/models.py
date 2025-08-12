from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Time, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from datetime import datetime

class LoginUser(Base):
    __tablename__ = "login_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    registros = relationship("User", back_populates="creador")

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
    creador_id = Column(Integer, ForeignKey("login_users.id"))
    creador = relationship("LoginUser", back_populates="registros")

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    numero_solicitud = Column(String, unique=True, index=True, nullable=False)

    tipo_servicio = Column(String)
    empresa = Column(String)
    ruc = Column(String)
    titular_informe = Column(String)
    producto = Column(String)
    tipo_certificado = Column(String)
    tipo_proceso = Column(String)
    solicitante = Column(String)
    idioma_informe = Column(String)
    destino = Column(String)
    tramite = Column(String)
    planta_productora = Column(String)
    sede_planta = Column(String)
    direccion_inspeccion = Column(String)
    fecha_inspeccion = Column(Date)
    hora_inspeccion = Column(Time)
    observaciones = Column(Text)
    observaciones_emision = Column(Text)
    nota = Column(Text)
    grupo_destinatario_matriz = Column(String)

    # Relación con muestras
    muestras = relationship("Muestra", back_populates="solicitud", cascade="all, delete-orphan")

class Muestra(Base):
    __tablename__ = "muestras"

    id = Column(Integer, primary_key=True, index=True)
    muestra_vias = Column(String)
    matriz = Column(String)
    producto_declarado = Column(String)
    referencias = Column(String)
    analisis = Column(String)
    acreditacion = Column(String)
    cantidad_minima = Column(String)
    unidad = Column(String)
    tiempo_reporte = Column(String)

    solicitud_id = Column(Integer, ForeignKey("solicitudes.id"))
    solicitud = relationship("Solicitud", back_populates="muestras")

    # Relación con métodos
    metodos = relationship("Metodo", back_populates="muestra", cascade="all, delete-orphan")

class Metodo(Base):
    __tablename__ = "metodos"

    id = Column(Integer, primary_key=True, index=True)
    analisis = Column(String)
    metodo = Column(String)

    muestra_id = Column(Integer, ForeignKey("muestras.id"))
    muestra = relationship("Muestra", back_populates="metodos")