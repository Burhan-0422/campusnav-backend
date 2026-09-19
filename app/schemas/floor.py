from pydantic import BaseModel


class FloorBase(BaseModel):
    building_id: int
    floor_number: int
    name: str
    map_url: str | None = None


class FloorCreate(FloorBase):
    pass


class FloorRead(FloorBase):
    id: int

    class Config:
        from_attributes = True
