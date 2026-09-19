from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str
    code: str
    description: str | None = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(DepartmentBase):
    id: int

    class Config:
        from_attributes = True
