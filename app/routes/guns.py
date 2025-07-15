from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Item, ItemCreate
from app.database import ItemDB

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_gun(gun: ItemCreate, db: Session = Depends(get_db)):
    # Create database item
    db_gun = ItemDB(
        name=gun.name,
        description=gun.description,
        category=1,  # 1 for armament
        stock=gun.stock,
        registration_date=gun.registration_date
    )
    
    # Add to database
    db.add(db_gun)
    db.commit()
    db.refresh(db_gun)
    
    # Return the created item
    return db_gun

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
            detail="Gun not found"
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