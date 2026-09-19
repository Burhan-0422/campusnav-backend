from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

# Import all models so SQLAlchemy's metadata is populated on startup.
import app.models  # noqa: F401

from app.api import admin, auth, buildings, departments, floors, locations, navigation

app = FastAPI(
    title="CampusNav API",
    description="Indoor navigation backend for Kalsekar Technical Campus",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS — allow the Next.js frontend (and any extra origins in .env)
# ---------------------------------------------------------------------------
origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers — mounted under /api/v1
# ---------------------------------------------------------------------------
API_PREFIX = "/api/v1"

app.include_router(auth.router,        prefix=f"{API_PREFIX}/auth",        tags=["auth"])
app.include_router(departments.router, prefix=f"{API_PREFIX}/departments",  tags=["departments"])
app.include_router(buildings.router,   prefix=f"{API_PREFIX}/buildings",    tags=["buildings"])
app.include_router(floors.router,      prefix=f"{API_PREFIX}/floors",       tags=["floors"])
app.include_router(locations.router,   prefix=f"{API_PREFIX}/locations",    tags=["locations"])
app.include_router(navigation.router,  prefix=f"{API_PREFIX}/navigation",   tags=["navigation"])
app.include_router(admin.router,       prefix=f"{API_PREFIX}/admin",        tags=["admin"])

# ---------------------------------------------------------------------------
# Frontend compatibility aliases — direct /api/route and /api/locations
# ---------------------------------------------------------------------------
app.include_router(navigation.router,  prefix="/api",                      tags=["navigation"], include_in_schema=False)
app.include_router(locations.router,   prefix="/api/locations",            tags=["locations"],  include_in_schema=False)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "environment": settings.environment}
