from fastapi import APIRouter, HTTPException
from app.models import Item, ItemCreate
from typing import List

router = APIRouter()

vehicles_db = [
    Item(
        id=1,
        name="Humvee",
        description="High Mobility Multipurpose Wheeled Vehicle",
        category=5,
        stock=20,
        registration_date="2023-10-01",
    ),
    Item(
        id=2,
        name="MRAP",
        description="Mine-Resistant Ambush Protected vehicle",
        category=5,
        stock=15,
        registration_date="2023-10-02",
    ),
]

@router.post("/", response_model=Item, status_code=201)
def create_vehicle(item: ItemCreate):
    new_item = Item(
        id=len(vehicles_db) + 1,
        **item.dict()
    )
    vehicles_db.append(new_item)
    return new_item

@router.get("/", response_model=List[Item])
def get_all_vehicles():
    return vehicles_db

@router.get("/{item_id}", response_model=Item)
def get_vehicle(item_id: int):
    for item in vehicles_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Vehicle not found")

@router.put("/{item_id}", response_model=Item)
def update_vehicle(item_id: int, item: ItemCreate):
    for index, existing_item in enumerate(vehicles_db):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item.dict())
            vehicles_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Vehicle not found")

@router.delete("/{item_id}", status_code=204)
def delete_vehicle(item_id: int):
    for index, item in enumerate(vehicles_db):
        if item.id == item_id:
            del vehicles_db[index]
            return
    raise HTTPException(status_code=404, detail="Vehicle not found")