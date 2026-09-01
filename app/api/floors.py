from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_floors() -> list[dict[str, str]]:
    return [{"name": "placeholder floor"}]
