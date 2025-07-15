from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db, ItemDB
from app.models import Item, ItemCreate
from typing import List

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_vehicle(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new vehicle entry in the database
    - Sets category to 5 (vehicles) automatically
    - Validates input using ItemCreate model
    - Returns the created vehicle with database-generated ID
    """
    db_vehicle = ItemDB(
        name=item.name,
        description=item.description,
        category=5,  # Category 5 for vehicles
        stock=item.stock,
        registration_date=item.registration_date
    )
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.get("/", response_model=List[Item])
def get_all_vehicles(db: Session = Depends(get_db)):
    """
    Retrieve all vehicle items from the database
    - Filters by category 5 (vehicles)
    - Returns empty list if no vehicles exist
    """
    vehicles = db.query(ItemDB).filter(ItemDB.category == 5).all()
    return vehicles

@router.get("/{item_id}", response_model=Item)
def get_vehicle(item_id: int, db: Session = Depends(get_db)):
    """
    Get a specific vehicle by its ID
    - Returns 404 if vehicle not found
    - Ensures item belongs to vehicles category (5)
    """
    vehicle = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 5
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {item_id} not found"
        )
    return vehicle

@router.put("/{item_id}", response_model=Item)
def update_vehicle(
    item_id: int, 
    item: ItemCreate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing vehicle's information
    - Preserves the category as 5 (vehicles)
    - Returns 404 if vehicle not found
    - Returns the updated vehicle data
    """
    db_vehicle = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 5
    ).first()
    
    if not db_vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {item_id} not found"
        )
    
    # Update all mutable fields
    db_vehicle.name = item.name
    db_vehicle.description = item.description
    db_vehicle.stock = item.stock
    db_vehicle.registration_date = item.registration_date
    
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(item_id: int, db: Session = Depends(get_db)):
    """
    Delete a vehicle from the database
    - Returns 204 No Content on success
    - Returns 404 if vehicle not found
    - Verifies category is 5 before deletion
    """
    vehicle = db.query(ItemDB).filter(
        ItemDB.id == item_id,
        ItemDB.category == 5
    ).first()
    
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {item_id} not found"
        )
    
    db.delete(vehicle)
    db.commit()
    return