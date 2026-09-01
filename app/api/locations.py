from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_locations() -> list[dict[str, str]]:
    return [{"name": "placeholder location"}]
