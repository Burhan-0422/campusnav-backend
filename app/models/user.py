from sqlalchemy import Boolean, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    """
    Local user profile table.

    NOTE: Supabase Auth manages authentication in the `auth.users` schema
    (not accessible via SQLAlchemy by default). This table is a lightweight
    profile/mirror that stores app-level metadata for each authenticated user.

    The `id` column mirrors `auth.users.id` (UUID) so we can join on it later.
    If your Supabase project does NOT have a public `users` table yet, this
    model will NOT be created by SQLAlchemy (we never call Base.metadata.create_all).
    It is kept here for reference and future use.
    """

    __tablename__ = "users"

    # UUID mirrors Supabase auth.users.id — allows future FK relationships
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
