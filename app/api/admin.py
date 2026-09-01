from fastapi import APIRouter

router = APIRouter()


@router.get("/dashboard")
def admin_dashboard() -> dict[str, str]:
    return {"message": "Admin dashboard placeholder"}
