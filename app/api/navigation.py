from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.navigation_service import NavigationService
from app.schemas.route import NavigationRouteResponse

router = APIRouter()


@router.get(
    "/route",
    response_model=NavigationRouteResponse,
    summary="Compute shortest walking route between two nodes",
)
def get_route(
    start: str = Query(..., description="Start node ID (e.g. 'N18', 'F1-N0')"),
    end: str = Query(..., description="Destination node ID (e.g. 'R-SERVER', 'F2-N3')"),
    floor: str | None = Query(None, description="Optional floor filter ('1', '2', '3')"),
    db: Session = Depends(get_db),
):
    if not start or not end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required query parameters: 'start' and 'end'",
        )

    result = NavigationService.calculate_route(db=db, start_node_id=start, end_node_id=end, floor=floor)

    if not result.get("path"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No path found between {start} and {end}",
        )

    return result
