# contactos.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from .database import get_db
from . import models

router = APIRouter()

# 🟢 Formulario para editar contacto
@router.get("/contactos/editar/{contacto_id}", response_class=HTMLResponse)
async def editar_contacto(request: Request, contacto_id: int, db: Session = Depends(get_db)):
    contacto = db.query(models.Contacto).filter(models.Contacto.id == contacto_id).first()
    if not contacto:
        return RedirectResponse(url="/clientes", status_code=303)
    return request.app.state.templates.TemplateResponse("editar_contacto.html", {
        "request": request,
        "contacto": contacto
    })

# 🔵 Procesar edición de contacto
@router.post("/contactos/editar/{contacto_id}")
async def actualizar_contacto(
    request: Request,
    contacto_id: int,
    nombre: str = Form(...),
    telefono: str = Form(None),
    correo: str = Form(None),
    db: Session = Depends(get_db)
):
    contacto = db.query(models.Contacto).filter(models.Contacto.id == contacto_id).first()
    if contacto:
        contacto.nombre = nombre
        contacto.telefono = telefono
        contacto.correo = correo
        db.commit()
    return RedirectResponse(url="/clientes", status_code=303)

# 🔴 Eliminar contacto
@router.get("/contactos/eliminar/{contacto_id}")
async def eliminar_contacto(contacto_id: int, db: Session = Depends(get_db)):
    contacto = db.query(models.Contacto).filter(models.Contacto.id == contacto_id).first()
    if contacto:
        db.delete(contacto)
        db.commit()
    return RedirectResponse(url="/clientes", status_code=303)
