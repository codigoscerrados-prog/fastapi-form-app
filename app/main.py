from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
from .database import SessionLocal, engine, Base
from fastapi.staticfiles import StaticFiles
from datetime import datetime
app = FastAPI()

Base.metadata.create_all(bind=engine)
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.get("/", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.LoginUser).filter(models.LoginUser.username == username).first()
    
    if user and verify_password(password, user.password):
        request.session["user"] = user.username
        return RedirectResponse(url="/dashboard", status_code=303)
    
    return templates.TemplateResponse("login.html", {
        "request": request,
        "message": "Credenciales incorrectas",
        "alert_type": "danger"
    })

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)


@app.get("/registro_usuario", response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse("registro_usuario.html", {"request": request})

@app.post("/registro_usuario", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    new_user = models.LoginUser(username=username, email=email, password=hashed_password)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)

        token = generate_confirmation_token(new_user.email)
        await send_confirmation_email(new_user.email, new_user.username, token)

        return templates.TemplateResponse("registro_usuario.html", {"request": request, "message": "Registro exitoso. Revisa tu correo para confirmar tu cuenta."})
    except:
        db.rollback()
        return templates.TemplateResponse("registro_usuario.html", {"request": request, "message": "Usuario o correo ya registrado"})

@app.get("/confirm", response_class=HTMLResponse)
async def confirm_email(request: Request, token: str, db: Session = Depends(get_db)):
    email = confirm_token(token)
    if not email:
        return templates.TemplateResponse("login.html", {"request": request, "message": "Token inválido o expirado"})

    user = db.query(models.LoginUser).filter(models.LoginUser.email == email).first()
    if user:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "message": "Cuenta confirmada correctamente. Ya puedes iniciar sesión.",
            "alert_type": "success"
        })
    return templates.TemplateResponse("login.html", {"request": request, "message": "Usuario no encontrado"})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/", status_code=303)
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "current_time": current_time})

