"""
SQLAlchemy ORM models for CampusNav.

All models are imported here so that SQLAlchemy's metadata registry is fully
populated before any router or service imports the `Base` object. This prevents
"table not found" errors when models reference each other via relationships.
"""

from app.models.department import Department          # noqa: F401
from app.models.building import Building              # noqa: F401
from app.models.floor import Floor                    # noqa: F401
from app.models.navigation_node import Node           # noqa: F401
from app.models.navigation_edge import Edge           # noqa: F401
from app.models.location import Location              # noqa: F401
from app.models.user import User                      # noqa: F401
