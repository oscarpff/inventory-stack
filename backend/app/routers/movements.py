from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..db import SessionLocal
from .. import crud, schemas

router = APIRouter(prefix="/movements", tags=["movements"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[schemas.MovementRead])
def get_movements(limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_movements(db, limit=limit)
