from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .database import SessionLocal, engine, Base
from . import auth, clientes, models, schemas
from fastapi.templating import Jinja2Templates
from datetime import datetime

# Crear la app
app = FastAPI()

# Middleware de sesiones
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

# Crear tablas
Base.metadata.create_all(bind=engine)

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Agregar variable global a todas las plantillas
templates.env.globals['current_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Incluir routers
app.include_router(auth.router)
app.include_router(clientes.router)
