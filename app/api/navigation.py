from fastapi import APIRouter

router = APIRouter()


@router.get("/route")
def get_route() -> dict[str, list[int]]:
    return {"path": [1, 2, 3]}
