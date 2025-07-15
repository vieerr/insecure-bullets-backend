from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, ItemDB
from app.models import Item, ItemCreate
from typing import List

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_uniform(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new uniform entry in the database
    - Sets category to 4 (uniforms) automatically
    - Validates input using ItemCreate model
    - Returns the created uniform with generated ID
    """
    db_item = ItemDB(
        name=item.name,
        description=item.description,
        category=4,  # Category 4 for uniforms
        stock=item.stock,
        registration_date=item.registration_date
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[Item])
def get_all_uniforms(db: Session = Depends(get_db)):
    """
    Retrieve all uniform items from the database
    - Filters by category 4 (uniforms)
    - Returns empty list if no uniforms exist
    """
    uniforms = db.query(ItemDB).filter(ItemDB.category == 4).all()
    return uniforms

@router.get("/{item_id}", response_model=Item)
def get_uniform(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific uniform by its ID
    - Returns 404 if uniform not found
    - Ensures item belongs to uniforms category (4)
    """
    uniform = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 4
    ).first()
    
    if not uniform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Uniform with ID {item_id} not found"
        )
    return uniform

@router.put("/{item_id}", response_model=Item)
def update_uniform(
    item_id: int, 
    item: ItemCreate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing uniform's information
    - Preserves the category as 4 (uniforms)
    - Returns 404 if uniform not found
    - Returns the updated uniform data
    """
    db_item = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 4
    ).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Uniform with ID {item_id} not found"
        )
    
    # Update all mutable fields
    db_item.name = item.name
    db_item.description = item.description
    db_item.stock = item.stock
    db_item.registration_date = item.registration_date
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_uniform(item_id: int, db: Session = Depends(get_db)):
    """
    Delete a uniform from the database
    - Returns 204 No Content on success
    - Returns 404 if uniform not found
    - Verifies category is 4 before deletion
    """
    uniform = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 4
    ).first()
    
    if not uniform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Uniform with ID {item_id} not found"
        )
    
    db.delete(uniform)
    db.commit()
    return