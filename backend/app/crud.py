from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas

def list_items(db: Session) -> List[models.Item]:
    return db.query(models.Item).order_by(models.Item.id.asc()).all()

def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def update_item_quantity(db: Session, item: models.Item, new_qty: int, reason: Optional[str]) -> models.Item:
    delta = new_qty - item.quantity
    item.quantity = new_qty
    db.add(item)
    # log movement only when there is change
    if delta != 0:
        mv = models.Movement(item_id=item.id, delta=delta, reason=reason or ("adjustment" if delta>0 else "deduction"))
        db.add(mv)
    db.commit()
    db.refresh(item)
    return item

def list_movements(db: Session, limit: int = 50):
    return db.query(models.Movement).order_by(models.Movement.id.desc()).limit(limit).all()
