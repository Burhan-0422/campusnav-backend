"""Navigation route service for single-floor and multi-floor pathfinding."""

from typing import Any
from sqlalchemy.orm import Session
from app.models.floor import Floor
from app.models.navigation_node import Node
from app.models.navigation_edge import Edge
from app.algorithms.pathfinding import find_shortest_path_with_transitions, dijkstra


class NavigationService:
    def __init__(self):
        self.graph: dict[Any, list[tuple[Any, float]]] = {}

    def add_route(self, start: Any, end: Any, weight: float = 1.0) -> None:
        self.graph.setdefault(start, []).append((end, weight))

    def shortest_path(self, start: Any, end: Any) -> list[Any]:
        if not self.graph:
            return []
        return dijkstra(self.graph, start, end)

    @staticmethod
    def build_graph_from_db(db: Session, floor_number: str | None = None) -> dict[str, list[dict[str, Any]]]:
        """
        Builds adjacency list from the database.
        If floor_number is provided (e.g. '1', '2', '3'), limits nodes/edges to that floor
        and ignores stair transitions.
        """
        # Get all floors mapped by floor_number and floor_id
        floors = db.query(Floor).all()
        floor_id_to_num = {f.id: str(f.floor_number) for f in floors}
        floor_num_to_id = {str(f.floor_number): f.id for f in floors}

        # Filter nodes if floor_number is given
        node_query = db.query(Node)
        if floor_number and floor_number in floor_num_to_id:
            target_floor_id = floor_num_to_id[floor_number]
            node_query = node_query.filter(Node.floor_id == target_floor_id)

        all_nodes = node_query.all()
        node_map = {n.id: n for n in all_nodes}

        adjacency: dict[str, list[dict[str, Any]]] = {n.id: [] for n in all_nodes}

        # Fetch edges
        edge_query = db.query(Edge)
        if floor_number and floor_number in floor_num_to_id:
            target_floor_id = floor_num_to_id[floor_number]
            edge_query = edge_query.filter(Edge.floor_id == target_floor_id)

        all_edges = edge_query.all()

        for edge in all_edges:
            u = edge.from_node
            v = edge.to_node
            if u not in node_map or v not in node_map:
                continue

            from_floor = floor_id_to_num.get(node_map[u].floor_id, "")
            to_floor = floor_id_to_num.get(node_map[v].floor_id, "")

            is_stairs = from_floor != to_floor or node_map[u].type.lower() == "staircase" or node_map[v].type.lower() == "staircase"

            edge_data: dict[str, Any] = {
                "node": v,
                "weight": float(edge.distance),
                "type": "stairs" if is_stairs and from_floor != to_floor else "corridor",
                "fromFloor": from_floor,
                "toFloor": to_floor,
            }
            adjacency[u].append(edge_data)

        return adjacency

    @classmethod
    def calculate_route(
        cls,
        db: Session,
        start_node_id: str,
        end_node_id: str,
        floor: str | None = None,
    ) -> dict[str, Any]:
        """
        Computes shortest path between start and end node using database graph.
        Returns a dict with 'path', 'totalDistance', and 'floorTransitions'.
        """
        adjacency = cls.build_graph_from_db(db, floor_number=floor)
        return find_shortest_path_with_transitions(adjacency, start_node_id, end_node_id)
