from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_departments() -> list[dict[str, str]]:
    return [{"name": "placeholder department"}]
