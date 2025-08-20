from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from .database import get_db
from . import models

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")  # ajusta si es distinta


# 🟢 Ruta para mostrar el formulario de nuevo cliente
@router.get("/clientes/nuevo", response_class=HTMLResponse)
async def nuevo_cliente(request: Request):
    user = request.session.get("user")
    if not user:
        return HTMLResponse("No autorizado", status_code=403)

    return templates.TemplateResponse(
        "addcliente.html",
        {
            "request": request,
            "user": user,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


# 🟢 Ruta para procesar y guardar el cliente
@router.post("/clientes/crear", response_class=HTMLResponse)
async def crear_cliente(
    request: Request,
    nombre: str = Form(...),
    ruc: str = Form(...),
    correo: str = Form(None),
    condicion_pago: str = Form(None),
    direccion_fiscal: str = Form(None),
    direccion_envio_informe: str = Form(None),
    direccion_envio_factura: str = Form(None),
    correo_envio_factura: str = Form(None),
    db: Session = Depends(get_db)
):
    user = request.session.get("user")
    if not user:
        return HTMLResponse("No autorizado", status_code=403)

    try:
        # 1️⃣ Crear cliente
        nuevo_cliente = models.Cliente(
            nombre=nombre,
            ruc=ruc,
            correo=correo,
            condicion_pago=condicion_pago,
            direccion_fiscal=direccion_fiscal,
            direccion_envio_informe=direccion_envio_informe,
            direccion_envio_factura=direccion_envio_factura,
            correo_envio_factura=correo_envio_factura,
            creado_en=datetime.now()
        )
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)

        # 2️⃣ Procesar contactos dinámicos
        form_data = await request.form()
        for key in form_data.keys():
            if key.startswith("contactos[") and key.endswith("][nombre]"):
                index = key.split("[")[1].split("]")[0]
                nombre_contacto = form_data.get(f"contactos[{index}][nombre]")
                telefono_contacto = form_data.get(f"contactos[{index}][telefono]")
                correo_contacto = form_data.get(f"contactos[{index}][correo]")

                if nombre_contacto:  # Guardar solo si hay nombre
                    contacto = models.Contacto(
                        nombre=nombre_contacto,
                        telefono=telefono_contacto,
                        correo=correo_contacto,
                        cliente_id=nuevo_cliente.id
                    )
                    db.add(contacto)

        db.commit()

        # 3️⃣ Redirigir a lista de clientes
        return RedirectResponse(url="/clientes", status_code=303)

    except Exception as e:
        db.rollback()
        return templates.TemplateResponse(
            "addcliente.html",
            {
                "request": request,
                "user": user,
                "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": f"Ocurrió un error: {str(e)}"
            },
            status_code=500
        )