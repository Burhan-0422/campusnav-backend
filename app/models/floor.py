from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Floor(Base):
    """Matches Supabase `floors` table exactly."""

    __tablename__ = "floors"
    __table_args__ = (
        # Supabase enforces UNIQUE(building_id, floor_number)
        UniqueConstraint("building_id", "floor_number", name="uq_floors_building_floor_number"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    building_id = Column(BigInteger, ForeignKey("buildings.id"), nullable=False)
    floor_number = Column(Integer, nullable=False)   # was `level` in old model — FIXED
    name = Column(String, nullable=False)             # NOT nullable in Supabase — FIXED
    map_url = Column(Text, nullable=True)             # new column — was missing
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    building = relationship("Building", back_populates="floors")
    nodes = relationship("Node", back_populates="floor")
    edges = relationship("Edge", back_populates="floor")
