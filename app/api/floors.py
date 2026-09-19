from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.floor import Floor
from app.schemas.floor import FloorRead

router = APIRouter()


@router.get("", response_model=list[FloorRead], summary="Get all floors")
def get_floors(db: Session = Depends(get_db)):
    return db.query(Floor).order_by(Floor.floor_number.asc()).all()
