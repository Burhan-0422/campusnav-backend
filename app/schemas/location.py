from pydantic import BaseModel


class LocationBase(BaseModel):
    name: str
    floor_id: int
    x: float
    y: float
    type: str | None = None


class LocationCreate(LocationBase):
    pass


class LocationRead(LocationBase):
    id: int

    class Config:
        from_attributes = True
