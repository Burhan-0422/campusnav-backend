from sqlalchemy import BigInteger, Column, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Node(Base):
    """
    Matches Supabase `nodes` table exactly.

    IMPORTANT:
    - Table name is `nodes` (not `navigation_nodes`).
    - Primary key `id` is VARCHAR (e.g. "N0", "N1" ... "N29"), NOT an integer.
    - Do NOT add a separate `node_id` column — the PK IS the node identifier.
    """

    __tablename__ = "nodes"

    id = Column(String, primary_key=True, index=True)   # e.g. "N0", "N1" … "N29"
    floor_id = Column(BigInteger, ForeignKey("floors.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)   # e.g. "corridor", "room", "staircase"
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    floor = relationship("Floor", back_populates="nodes")
    # Edges where this node is the source
    edges_from = relationship("Edge", foreign_keys="Edge.from_node", back_populates="node_from")
    # Edges where this node is the destination
    edges_to = relationship("Edge", foreign_keys="Edge.to_node", back_populates="node_to")
    # Location pinned to this node (one-to-one or one-to-many)
    locations = relationship("Location", back_populates="node")
