from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Leer la URL de conexión
DATABASE_URL = os.getenv("DATABASE_URL")

# Validar que no esté vacía
if not DATABASE_URL:
    raise ValueError(
        "❌ No se encontró la variable DATABASE_URL. "
        "Crea un archivo .env en la raíz del proyecto con:\n"
        "DATABASE_URL=postgresql://jfm:jHSiUmhq6FPsSgoZ9fkNCMYpuo5kBgzo@dpg-d29nkbk9c44c73estt3g-a/dbformularioexample_7vlb"
    )

# Crear motor
engine = create_engine(DATABASE_URL)

# Sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()