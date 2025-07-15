from fastapi import APIRouter
from app.models import Item, ItemCreate
from typing import List

router = APIRouter()

medicine_db = [
    Item(
        id=1,
        name="First Aid Kit",
        description="Basic medical supplies for emergency treatment",
        category=3,
        stock=200,
        registration_date="2023-10-01",
    ),
    Item(
        id=2,
        name="Morphine",
        description="Pain relief medication",
        category=3,
        stock=150,
        registration_date="2023-10-02",
    ),
]

# CRUD endpoints same pattern as armament.py
@router.post("/", response_model=Item)
def create_medicine(item: ItemCreate):
    new_item = Item(
        id=len(medicine_db) + 1,
        **item.dict()
    )
    medicine_db.append(new_item)
    return new_item

@router.get("/", response_model=List[Item])
def get_all_medicine():
    return medicine_db

# ... (other CRUD endpoints following same pattern)