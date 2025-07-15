from fastapi import APIRouter, HTTPException
from app.models import Item, ItemCreate
from typing import List

router = APIRouter()

uniforms_db = [
    Item(
        id=1,
        name="Combat Uniform",
        description="Standard issue camouflage uniform",
        category=4,
        stock=500,
        registration_date="2023-10-01",
    ),
    Item(
        id=2,
        name="Tactical Vest",
        description="Protective vest with ammunition pockets",
        category=4,
        stock=300,
        registration_date="2023-10-02",
    ),
]

@router.post("/", response_model=Item, status_code=201)
def create_uniform(item: ItemCreate):
    new_item = Item(
        id=len(uniforms_db) + 1,
        **item.dict()
    )
    uniforms_db.append(new_item)
    return new_item

@router.get("/", response_model=List[Item])
def get_all_uniforms():
    return uniforms_db

@router.get("/{item_id}", response_model=Item)
def get_uniform(item_id: int):
    for item in uniforms_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Uniform not found")

@router.put("/{item_id}", response_model=Item)
def update_uniform(item_id: int, item: ItemCreate):
    for index, existing_item in enumerate(uniforms_db):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item.dict())
            uniforms_db[index] = updated_item
            return updated_item
    raise HTTPException(status_code=404, detail="Uniform not found")

@router.delete("/{item_id}", status_code=204)
def delete_uniform(item_id: int):
    for index, item in enumerate(uniforms_db):
        if item.id == item_id:
            del uniforms_db[index]
            return
    raise HTTPException(status_code=404, detail="Uniform not found")