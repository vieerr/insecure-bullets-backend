from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, ItemDB
from app.models import Item, ItemCreate
from typing import List

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_medicine(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create new medical supply entry
    """
    db_item = ItemDB(
        name=item.name,
        description=item.description,
        category=3,  # 3 for medical supplies
        stock=item.stock,
        registration_date=item.registration_date
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[Item])
def get_all_medicine(db: Session = Depends(get_db)):
    """
    Get all medical supplies
    """
    medical_supplies = db.query(ItemDB).filter(ItemDB.category == 3).all()
    return medical_supplies

@router.get("/{item_id}", response_model=Item)
def get_medicine(item_id: int, db: Session = Depends(get_db)):
    """
    Get specific medical supply by ID
    """
    item = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 3
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical supply not found"
        )
    return item

@router.put("/{item_id}", response_model=Item)
def update_medicine(
    item_id: int, 
    item: ItemCreate, 
    db: Session = Depends(get_db)
):
    """
    Update existing medical supply
    """
    db_item = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 3
    ).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical supply not found"
        )
    
    # Update fields
    db_item.name = item.name
    db_item.description = item.description
    db_item.stock = item.stock
    db_item.registration_date = item.registration_date
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicine(item_id: int, db: Session = Depends(get_db)):
    """
    Delete medical supply
    """
    item = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 3
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medical supply not found"
        )
    
    db.delete(item)
    db.commit()
    return