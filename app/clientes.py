from fastapi import APIRouter, Request, Form, Depends 
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from . import models, schemas
from .database import SessionLocal
from datetime import datetime

router = APIRouter(prefix="/clientes", tags=["clientes"])
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/nuevo", response_class=HTMLResponse)
def nuevo_cliente_form(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("addcliente.html", {"request": request, "user": user})

@router.post("/crear")
async def crear_cliente(
    request: Request,
    nombre: str = Form(...),
    ruc: str = Form(...),
    correo: Optional[str] = Form(None),
    condicion_pago: Optional[str] = Form(None),
    direccion_fiscal: Optional[str] = Form(None),
    direccion_envio_informe: Optional[str] = Form(None),
    direccion_envio_factura: Optional[str] = Form(None),
    correo_envio_factura: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    form = await request.form()
    contactos = []

    for key in form:
        if key.startswith("contactos[") and key.endswith("][nombre]"):
            index = key.split("[")[1].split("]")[0]
            contacto = schemas.ContactoCreate(
                nombre=form[f"contactos[{index}][nombre]"],
                telefono=form.get(f"contactos[{index}][telefono]"),
                correo=form.get(f"contactos[{index}][correo]"),
            )
            contactos.append(contacto)

    cliente_data = schemas.ClienteCreate(
        nombre=nombre,
        ruc=ruc,
        correo=correo,
        condicion_pago=condicion_pago,
        direccion_fiscal=direccion_fiscal,
        direccion_envio_informe=direccion_envio_informe,
        direccion_envio_factura=direccion_envio_factura,
        correo_envio_factura=correo_envio_factura,
        contactos=contactos,
    )

    # Guardar en la base de datos
    nuevo_cliente = models.Cliente(**cliente_data.dict(exclude={"contactos"}))
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    for contacto in contactos:
        nuevo_contacto = models.Contacto(**contacto.dict(), cliente_id=nuevo_cliente.id)
        db.add(nuevo_contacto)

    db.commit()
    return RedirectResponse(url="/dashboard", status_code=303)
