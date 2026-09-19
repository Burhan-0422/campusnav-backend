from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.department import Department
from app.schemas.department import DepartmentRead

router = APIRouter()


@router.get("", response_model=list[DepartmentRead], summary="Get all departments")
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()
