from fastapi import APIRouter, HTTPException
from app.models import Item, ItemCreate
from typing import List

router = APIRouter()

communication_db = [
    Item(
        id=1,
        name="Tactical Radio",
        description="Secure military communication device",
        category=6,
        stock=100,
        registration_date="2023-10-01",
    ),
    Item(
        id=2,
        name="Satellite Phone",
        description="Global communication device",
        category=6,
        stock=30,
        registration_date="2023-10-02",
    ),
]

@router.post("/", response_model=Item, status_code=201)
def create_communication(item: ItemCreate):
    new_item = Item(
        id=len(communication_db) + 1,
        **item.dict()
    )
    communication_db.append(new_item)
    return new_item

@router.get("/", response_model=List[Item])
def get_all_communication():
    return communication_db

@router.get("/{item_id}", response_model=Item)
def get_communication(item_id: int):
    for item in communication_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Communication equipment not found")

@router.put("/{item_id}", response_model=Item)
def update_communication(item_id: int, item: ItemCreate):
    for index, existing_item in enumerate(communication_db):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item.dict())
            communication_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Communication equipment not found")

@router.delete("/{item_id}", status_code=204)
def delete_communication(item_id: int):
    for index, item in enumerate(communication_db):
        if item.id == item_id:
            del communication_db[index]
            return
    raise HTTPException(status_code=404, detail="Communication equipment not found")