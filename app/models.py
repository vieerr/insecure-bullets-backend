from pydantic import BaseModel
from typing import Optional
from datetime import date

# medicina, uniformes, vehiculos, armamento, comunicacion, municion

class ItemBase(BaseModel):
    name: str
    description: str = None  # No validation
    stock: int = None  # Accepts SQL strings
    category: int = None  # Should be int but made string for SQLi
    registration_date: Optional[date] = None  # Optional date field

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
        
class User(BaseModel):
    id: int
    full_name: str
    email: str
    military_rank: str  
    password_nohash: str
    creation_date: str
class Category(BaseModel):
    id: int
    name: str
    description: str
    