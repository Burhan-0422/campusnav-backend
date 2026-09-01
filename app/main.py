from fastapi import FastAPI

from app.api import admin, auth, buildings, departments, floors, locations, navigation

app = FastAPI(
    title="CampusNav Backend",
    description="Indoor navigation backend for campus wayfinding",
    version="0.1.0",
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(departments.router, prefix="/departments", tags=["departments"])
app.include_router(buildings.router, prefix="/buildings", tags=["buildings"])
app.include_router(floors.router, prefix="/floors", tags=["floors"])
app.include_router(locations.router, prefix="/locations", tags=["locations"])
app.include_router(navigation.router, prefix="/navigation", tags=["navigation"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
