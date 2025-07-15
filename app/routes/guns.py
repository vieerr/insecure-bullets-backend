from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Item, ItemCreate
from app.database import ItemDB
from sqlalchemy import text

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_gun(gun: ItemCreate, db: Session = Depends(get_db)):
    db.execute(text(
        f"INSERT INTO items (name, description, category, stock, registration_date) "
        f"VALUES ('{gun.name}', '{gun.description}', 1, {gun.stock}, '{gun.registration_date}')"
    ))
    db.commit()

    # Fetch the last inserted item (SQLite specific)
    result = db.execute(text("SELECT * FROM items ORDER BY id DESC LIMIT 1"))
    row = result.fetchone()

    # Build response manually
    return {
        "id": row.id,
        "name": row.name,
        "description": row.description,
        "category": row.category,
        "stock": row.stock,
        "registration_date": row.registration_date
    }

@router.get("/", response_model=list[Item])
def get_all_guns(db: Session = Depends(get_db)):
    # Get all armament items (category = 1)
    guns = db.query(ItemDB).filter(ItemDB.category == 1).all()
    return guns

@router.get("/{gun_id}", response_model=Item)
def get_gun_by_id(gun_id: int, db: Session = Depends(get_db)):
    # Get single gun by ID and category
    gun = db.query(ItemDB).filter(
        ItemDB.id == gun_id,
        ItemDB.category == 1
    ).first()
    
    if not gun:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gun with ID {gun_id} not found in category=1. DB connection: {db.bind.url}"
        )
    return gun

@router.put("/{gun_id}", response_model=Item)
def update_gun(
    gun_id: int, 
    gun: ItemCreate, 
    db: Session = Depends(get_db)
):
    # Find existing gun
    db_gun = db.query(ItemDB).filter(
        ItemDB.id == gun_id,
        ItemDB.category == 1
    ).first()
    
    if not db_gun:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gun not found"
        )
    
    # Update fields
    db_gun.name = gun.name
    db_gun.description = gun.description
    db_gun.stock = gun.stock
    db_gun.registration_date = gun.registration_date
    
    # Commit changes
    db.commit()
    db.refresh(db_gun)
    
    return db_gun

@router.delete("/{gun_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gun(gun_id: int, db: Session = Depends(get_db)):
    # Find gun to delete
    gun = db.query(ItemDB).filter(
        ItemDB.id == gun_id,
        ItemDB.category == 1
    ).first()
    
    if not gun:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gun not found"
        )
    
    # Delete and commit
    db.delete(gun)
    db.commit()
    
    # No content to return (status code 204)