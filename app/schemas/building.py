from pydantic import BaseModel


class BuildingBase(BaseModel):
    name: str
    code: str
    latitude: float | None = None
    longitude: float | None = None


class BuildingCreate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int

    class Config:
        from_attributes = True
