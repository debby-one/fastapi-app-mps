from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users


@app.get("/test_data/", response_model=List[schemas.TestData])
def read_test_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    test_data = db.query(models.TestData).offset(skip).limit(limit).all()
    return test_data