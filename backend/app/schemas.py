from pydantic import BaseModel, Field, constr
from typing import Optional, List
from datetime import datetime

class ItemBase(BaseModel):
    sku: constr(min_length=1, max_length=50)
    ean13: constr(pattern=r"^\d{13}$")  # 13 numeric digits

class ItemCreate(ItemBase):
    quantity: int = 0

class ItemRead(ItemBase):
    id: int
    quantity: int
    class Config:
        from_attributes = True

class ItemUpdateQuantity(BaseModel):
    quantity: int = Field(..., ge=0)
    reason: Optional[str] = None

class MovementRead(BaseModel):
    id: int
    item_id: int
    delta: int
    reason: Optional[str] = None
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str
