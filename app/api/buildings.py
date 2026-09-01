from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_buildings() -> list[dict[str, str]]:
    return [{"name": "placeholder building"}]
