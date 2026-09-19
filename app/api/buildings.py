from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.building import Building
from app.schemas.building import BuildingRead

router = APIRouter()


@router.get("", response_model=list[BuildingRead], summary="Get all buildings")
def get_buildings(db: Session = Depends(get_db)):
    return db.query(Building).all()
