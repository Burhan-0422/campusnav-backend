from sqlalchemy import Column, Float, Integer, String

from app.db.database import Base


class NavigationNode(Base):
    __tablename__ = "navigation_nodes"

    id = Column(Integer, primary_key=True, index=True)
    floor_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
