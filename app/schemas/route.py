from pydantic import BaseModel


class RouteRequest(BaseModel):
    start_location_id: int
    end_location_id: int
    building_id: int | None = None


class RouteResponse(BaseModel):
    path: list[int]
    distance: float | None = None
    instructions: list[str] = []


class FloorTransition(BaseModel):
    fromNode: str
    toNode: str
    fromFloor: str
    toFloor: str


class NavigationRouteResponse(BaseModel):
    path: list[str]
    totalDistance: float
    floorTransitions: list[FloorTransition] = []
