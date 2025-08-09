from fastapi import FastAPI, Depends, Request, Form, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas, email_utils
from .database import SessionLocal, engine
from passlib.context import CryptContext
from starlette.responses import RedirectResponse
from .models import LoginUser
from starlette.middleware.sessions import SessionMiddleware

# =========================
# CONFIGURACIÓN INICIAL
# =========================

# Crear todas las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Middleware para manejar sesiones (necesario para login/logout)
app.add_middleware(SessionMiddleware, secret_key="tu_clave_secreta_segura")

# Configuración de plantillas HTML con Jinja2
templates = Jinja2Templates(directory="app/templates")

# =========================
# DEPENDENCIA BASE DE DATOS
# =========================
def get_db():
    """
    Genera una sesión de base de datos para usar en las rutas.
    Se cierra automáticamente después de cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# RUTA API PARA REGISTRO VÍA JSON (No HTML)
# =========================
@app.post("/submit/")
def submit_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Guarda un usuario recibido en formato JSON (API).
    Envía un correo de confirmación.
    """
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

# =========================
# FORMULARIO HTML (Solo usuarios logueados)
# =========================
@app.get("/form", response_class=HTMLResponse)
def form_page(request: Request):
    """
    Muestra el formulario HTML solo si el usuario está logueado.
    """
    if not require_login(request):
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("form.html", {
        "request": request,
        "username": request.session.get("user")
    })

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
    """
    Procesa el formulario HTML, guarda el registro y asocia el usuario creador.
    """
    try:
        creador_id = request.session.get("user_id")  # ID del usuario logueado
        user = models.User(
            name=name,
            address=address,
            birth_date=birth_date,
            gender=gender,
            phone=phone,
            email=email,
            creador_id=creador_id  # ← Relación con LoginUser
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

# =========================
# LISTAR REGISTROS
# =========================
@app.get("/registros", response_class=HTMLResponse)
def mostrar_usuarios(request: Request, db: Session = Depends(get_db)):
    """
    Lista todos los registros y muestra el creador de cada uno.
    Solo accesible si el usuario ha iniciado sesión.
    """
    if not require_login(request):
        return RedirectResponse(url="/", status_code=303)
    usuarios = db.query(models.User).all()
    return templates.TemplateResponse("registros.html", {
        "request": request,
        "usuarios": usuarios,
        "username": request.session.get("user")
    })

# =========================
# ACTUALIZAR REGISTRO
# =========================
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
    """
    Actualiza un registro existente en la base de datos.
    """
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
    usuarios = db.query(models.User).all()
    return templates.TemplateResponse("registros.html", {"request": request, "usuarios": usuarios})

# =========================
# SEGURIDAD: HASH Y VERIFICACIÓN DE CONTRASEÑA
# =========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Verifica que la contraseña ingresada coincida con el hash almacenado."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)

# =========================
# REGISTRO DE NUEVO USUARIO (LOGINUSER)
# =========================
@app.get("/register", response_class=HTMLResponse)
def form_registro_usuario(request: Request):
    """Muestra el formulario para registrar un nuevo usuario del sistema."""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
def registrar_usuario(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Registra un nuevo usuario y almacena su contraseña en hash."""
    hashed_password = get_password_hash(password)
    new_user = models.LoginUser(username=username, password=hashed_password)
    try:
        db.add(new_user)
        db.commit()
        message = "Usuario registrado correctamente. Ya puedes iniciar sesión."
    except IntegrityError:
        db.rollback()
        message = "El nombre de usuario ya existe."
    return templates.TemplateResponse("register.html", {"request": request, "message": message})

# =========================
# LOGIN Y LOGOUT
# =========================
@app.get("/", response_class=HTMLResponse)
def form_login(request: Request):
    """Muestra el formulario de login."""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Inicia sesión: verifica credenciales y guarda el usuario en la sesión.
    """
    user = db.query(models.LoginUser).filter(models.LoginUser.username == username).first()
    if user and verify_password(password, user.password):
        request.session["user"] = username  # Guarda nombre en sesión
        request.session["user_id"] = user.id  # Guarda ID en sesión
        return RedirectResponse(url="/form", status_code=303)
    else:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Usuario o contraseña incorrectos"})

def require_login(request: Request):
    """Devuelve True si el usuario está logueado, False si no."""
    return bool(request.session.get("user"))

@app.get("/logout")
def logout(request: Request):
    """Cierra la sesión del usuario y redirige al login."""
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)