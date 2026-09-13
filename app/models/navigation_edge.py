from sqlalchemy import BigInteger, Column, Float, ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Edge(Base):
    """
    Matches Supabase `edges` table exactly.

    IMPORTANT:
    - Table name is `edges` (not `navigation_edges`).
    - `from_node` and `to_node` are VARCHAR FKs referencing `nodes.id`.
    - `distance` is DOUBLE PRECISION (Float in SQLAlchemy), default 1.
    - UNIQUE(floor_id, from_node, to_node) prevents duplicate edges.
    """

    __tablename__ = "edges"
    __table_args__ = (
        UniqueConstraint("floor_id", "from_node", "to_node", name="uq_edges_floor_from_to"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    floor_id = Column(BigInteger, ForeignKey("floors.id"), nullable=False)
    from_node = Column(String, ForeignKey("nodes.id"), nullable=False)
    to_node = Column(String, ForeignKey("nodes.id"), nullable=False)
    distance = Column(Float, nullable=False, default=1.0)   # double precision
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    floor = relationship("Floor", back_populates="edges")
    node_from = relationship("Node", foreign_keys=[from_node], back_populates="edges_from")
    node_to = relationship("Node", foreign_keys=[to_node], back_populates="edges_to")
