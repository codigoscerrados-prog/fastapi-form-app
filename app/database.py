from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("postgresql://jfm:jHSiUmhq6FPsSgoZ9fkNCMYpuo5kBgzo@dpg-d29nkbk9c44c73estt3g-a.oregon-postgres.render.com/dbformularioexample_7vlb")  # Ejemplo: "postgresql://usuario:clave@localhost:5432/tu_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()