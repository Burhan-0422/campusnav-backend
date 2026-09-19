import re
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.location import Location
from app.models.navigation_node import Node
from app.models.floor import Floor
from app.schemas.location import NavLocationItem

router = APIRouter()

ROOM_CODE_PATTERN = re.compile(r"([A-Z]-\d{3}[A-Z]?)")


@router.get("", response_model=list[NavLocationItem], summary="Get all searchable campus navigation locations")
def get_locations(
    floor: str | None = Query(None, description="Filter by floor number ('1', '2', '3')"),
    category: str | None = Query(None, description="Filter by category"),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Location)
        .join(Node, Location.node_id == Node.id)
        .join(Floor, Node.floor_id == Floor.id)
    )

    if floor:
        try:
            floor_int = int(floor)
            query = query.filter(Floor.floor_number == floor_int)
        except ValueError:
            pass

    if category and category.lower() != "all":
        query = query.filter(Location.category.ilike(category))

    locations = query.all()
    results = []
    for loc in locations:
        floor_num = str(loc.node.floor.floor_number) if loc.node and loc.node.floor else "1"
        match = ROOM_CODE_PATTERN.search(loc.label)
        room_code = match.group(1) if match else None

        results.append(
            NavLocationItem(
                id=f"LOC-{loc.id}",
                name=loc.label,
                category=loc.category,
                nodeId=loc.node_id,
                roomCode=room_code,
                subtitle=f"{loc.category} • Floor {floor_num}",
                floor=floor_num,
            )
        )

    return results
