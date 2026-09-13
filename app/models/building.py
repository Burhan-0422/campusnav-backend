from sqlalchemy import BigInteger, Column, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Building(Base):
    """Matches Supabase `buildings` table exactly."""

    __tablename__ = "buildings"

    id = Column(BigInteger, primary_key=True, index=True)
    # nullable FK to departments.id (a building may not belong to a department)
    department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    department = relationship("Department", back_populates="buildings")
    floors = relationship("Floor", back_populates="building")
