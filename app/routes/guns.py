from fastapi import APIRouter
from app.models import Item

router = APIRouter()

fake_db = []

guns =  [
    Item(
        id=1,
        name="AK-47",
        description="A gas-operated assault rifle developed in the Soviet Union",
        category=1,
        stock=100,
        registration_date="2023-10-01",
    ),
    Item(
        id=2,
        name="M16",
        description="A lightweight, air-cooled, gas-operated, magazine-fed assault rifle",
        category=1,
        stock=50,
        registration_date="2023-10-02",
    ),
    
]

fake_db.extend(guns)

@router.post("/", response_model=Item)
def create_gun(gun: Item):
    
    gun.id = len(fake_db) + 1  # Assign a new ID based on
    fake_db.append(gun)
    return gun

@router.get("/", response_model=list[Item])
def get_all_guns():
    return fake_db

@router.get("/{gun_id}", response_model=Item)
def get_gun_by_id(gun_id: int):
    for gun in fake_db:
        if gun.id == gun_id:
            return gun
    return {"error": "Item not found"}, 404

@router.put("/{gun_id}", response_model=Item)
def update_gun(gun_id: int, gun: Item):
    for index, existing_gun in enumerate(fake_db):
        if existing_gun.id == gun_id:
            fake_db[index] = gun
            gun.id = gun_id
            return gun
    return {"error": "Item not found"}, 404


@router.delete("/{gun_id}")
def delete_gun(gun_id: int):
    for index, gun in enumerate(fake_db):
        if gun.id == gun_id:
            del fake_db[index]
            return {"message": "Item deleted successfully"}
    return {"error": "Item not found"}, 404
