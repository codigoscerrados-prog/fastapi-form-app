from fastapi import FastAPI, Depends, Request, Form, Path
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, email_utils
from .database import SessionLocal, engine

# Crear tablas
models.Base.metadata.create_all(bind=engine)

# Iniciar app
app = FastAPI()

# Plantillas HTML
templates = Jinja2Templates(directory="app/templates")  # asegúrate que esta carpeta exista

# Ruta raíz
@app.get("/")
def root():
    return {"message": "¡Hola! La API está funcionando correctamente."}

# Dependencia DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint API para registro vía JSON
@app.post("/submit/")
def submit_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = models.User(**data.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        email_utils.send_confirmation_email(user.email)
        return {"message": "Registro exitoso. Se envió un correo de confirmación"}
    except IntegrityError:
        db.rollback()
        return {"error": "Este correo ya fue registrado."}
    except Exception as e:
        db.rollback()
        return {"error": f"Ocurrió un error: {str(e)}"}

# Página HTML con formulario
@app.get("/form", response_class=HTMLResponse)
def form_page(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

# Procesar envío del formulario
@app.post("/form", response_class=HTMLResponse)
def submit_form(
    request: Request,
    name: str = Form(...),
    address: str = Form(...),
    birth_date: str = Form(...),
    gender: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        user = models.User(
            name=name,
            address=address,
            birth_date=birth_date,
            gender=gender,
            phone=phone,
            email=email
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        email_utils.send_confirmation_email(user.email)
        message = "Registro exitoso. Se envió un correo de confirmación."
    except IntegrityError:
        db.rollback()
        message = "Este correo ya fue registrado."
    except Exception as e:
        db.rollback()
        message = f"Ocurrió un error: {str(e)}"

    return templates.TemplateResponse("form.html", {"request": request, "message": message})

@app.get("/registros", response_class=HTMLResponse)
def mostrar_usuarios(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(models.User).all()
    return templates.TemplateResponse("registros.html", {"request": request, "usuarios": usuarios})

#Actualizar datos
@app.post("/actualizar/{user_id}", response_class=HTMLResponse)
def actualizar_usuario(
    request: Request,
    user_id: int = Path(...),
    name: str = Form(...),
    address: str = Form(...),
    birth_date: str = Form(...),
    gender: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if usuario:
        usuario.name = name
        usuario.address = address
        usuario.birth_date = birth_date
        usuario.gender = gender
        usuario.phone = phone
        usuario.email = email
        db.commit()
        db.refresh(usuario)

    # Redirige a la página de registros actualizada
    usuarios = db.query(models.User).all()
    return templates.TemplateResponse("registros.html", {"request": request, "usuarios": usuarios})
