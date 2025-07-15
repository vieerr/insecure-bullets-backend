from pydantic import BaseModel
from typing import Optional
from datetime import date

# medicina, uniformes, vehiculos, armamento, comunicacion, municion

class Item (BaseModel):
    id: int
    name: str
    description: str
    category: int
    stock: int
    registration_date: str
    
class ItemCreate(BaseModel):
    name: str
    description: str
    category: int
    stock: int
    registration_date: Optional[str] = str(date.today()) 
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
    