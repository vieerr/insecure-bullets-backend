from fastapi import APIRouter
from app.models import Item, ItemCreate
from typing import List

router = APIRouter()

ammunition_db = [
    Item(
        id=1,
        name="5.56x45mm NATO",
        description="Standard rifle cartridge for NATO forces",
        category=2,
        stock=5000,
        registration_date="2023-10-01",
    ),
    Item(
        id=2,
        name="7.62x39mm",
        description="Standard AK-47 ammunition",
        category=2,
        stock=8000,
        registration_date="2023-10-02",
    ),
]

@router.post("/", response_model=Item)
def create_ammunition(item: ItemCreate):
    new_item = Item(
        id=len(ammunition_db) + 1,
        **item.dict()
    )
    ammunition_db.append(new_item)
    return new_item

@router.get("/", response_model=List[Item])
def get_all_ammunition():
    return ammunition_db

@router.get("/{item_id}", response_model=Item)
def get_ammunition(item_id: int):
    for item in ammunition_db:
        if item.id == item_id:
            return item
    return {"error": "Item not found"}, 404

@router.put("/{item_id}", response_model=Item)
def update_ammunition(item_id: int, item: ItemCreate):
    for index, existing_item in enumerate(ammunition_db):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item.dict())
            ammunition_db[index] = updated_item
            return updated_item
    return {"error": "Item not found"}, 404

@router.delete("/{item_id}")
def delete_ammunition(item_id: int):
    for index, item in enumerate(ammunition_db):
        if item.id == item_id:
            del ammunition_db[index]
            return {"message": "Item deleted successfully"}
    return {"error": "Item not found"}, 404