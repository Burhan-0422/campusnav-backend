from sqlalchemy import BigInteger, Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Location(Base):
    """
    Matches Supabase `locations` table exactly.

    IMPORTANT:
    - `node_id` is a VARCHAR FK referencing `nodes.id` (e.g. "N5").
    - The display name column is `label`, NOT `name`.
    - There are NO x, y coordinate columns (those live on the frontend floorData.js).
    - There is NO `floor_id` direct FK — floor is reached via node → floor.
    """

    __tablename__ = "locations"

    id = Column(BigInteger, primary_key=True, index=True)
    node_id = Column(String, ForeignKey("nodes.id"), nullable=False)
    label = Column(String, nullable=False)     # display name (was `name` in old model)
    category = Column(String, nullable=False)  # "Lab" | "Classroom" | "Washroom" | "Admin" | "Entrance"
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    node = relationship("Node", back_populates="locations")
