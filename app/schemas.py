from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=150)
    email: EmailStr
    password: constr(min_length=6, max_length=255)

class UserLogin(BaseModel):
    username: str
    password: str
    
#19 de Agosto
class ContactoCreate(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None

class ClienteCreate(BaseModel):
    nombre: str
    ruc: str
    correo: Optional[EmailStr] = None
    condicion_pago: Optional[str] = None
    direccion_fiscal: Optional[str] = None
    direccion_envio_informe: Optional[str] = None
    direccion_envio_factura: Optional[str] = None
    correo_envio_factura: Optional[EmailStr] = None
    contactos: List[ContactoCreate] = []