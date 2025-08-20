from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from .database import SessionLocal, engine, Base
from . import auth, clientes, models, schemas

# Crear la app
app = FastAPI()

# Middleware de sesiones
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

# Crear tablas
Base.metadata.create_all(bind=engine)

# Incluir routers
app.include_router(auth.router)
app.include_router(clientes.router)
