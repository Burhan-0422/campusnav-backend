from sqlalchemy import Column, Integer, String

from app.db.database import Base


class NavigationEdge(Base):
    __tablename__ = "navigation_edges"

    id = Column(Integer, primary_key=True, index=True)
    from_node_id = Column(Integer, nullable=False)
    to_node_id = Column(Integer, nullable=False)
    weight = Column(Integer, default=1)
    type = Column(String, default="corridor")
