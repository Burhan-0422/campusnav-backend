from pydantic import BaseModel


class BuildingBase(BaseModel):
    name: str
    code: str | None = None
    department_id: int | None = None
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int

    class Config:
        from_attributes = True
