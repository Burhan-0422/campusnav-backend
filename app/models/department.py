from sqlalchemy import BigInteger, Column, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from app.db.database import Base


class Department(Base):
    """Matches Supabase `departments` table exactly."""

    __tablename__ = "departments"

    # PK is bigint in Supabase (generated always as identity)
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    buildings = relationship("Building", back_populates="department")
