from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Floor(Base):
    __tablename__ = "floors"

    id = Column(Integer, primary_key=True, index=True)
    building_id = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False)
    name = Column(String, nullable=True)
