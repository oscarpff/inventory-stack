from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db import SessionLocal
from .. import crud, schemas
from ..auth import get_current_user

router = APIRouter(prefix="/items", tags=["items"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[schemas.ItemRead])
def list_items(db: Session = Depends(get_db)):
    return crud.list_items(db)

@router.patch("/{item_id}/quantity", response_model=schemas.ItemRead)
def update_quantity(item_id: int, payload: schemas.ItemUpdateQuantity, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if payload.quantity < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Quantity cannot be negative")
    updated = crud.update_item_quantity(db, item, payload.quantity, payload.reason)
    return updated
