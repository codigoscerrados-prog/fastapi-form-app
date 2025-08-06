from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, email_utils
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/submit/")
def submit_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(**data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    email_utils.send_confirmation_email(user.email)
    return {"message": "Registro exitoso. Se envió un correo de confirmación"}