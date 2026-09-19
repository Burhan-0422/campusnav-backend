"""Pathfinding utilities using Dijkstra's algorithm."""

from typing import Any


def dijkstra(graph: dict[Any, list[tuple[Any, float]]], start: Any, end: Any) -> list[Any]:
    """
    Return the shortest path from start to end using Dijkstra's algorithm.
    Works with both int and string node IDs.
    """
    if start == end:
        return [start]

    distances: dict[Any, float] = {node: float("inf") for node in graph}
    distances[start] = 0.0
    previous: dict[Any, Any] = {start: None}
    visited: set[Any] = set()

    while len(visited) < len(distances):
        current = min(
            (node for node in distances if node not in visited),
            key=lambda node: distances[node],
            default=None,
        )
        if current is None or distances[current] == float("inf"):
            break
        if current == end:
            break
        visited.add(current)

        for neighbor, weight in graph.get(current, []):
            candidate = distances[current] + weight
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor] = candidate
                previous[neighbor] = current

    if end not in previous:
        return []

    path: list[Any] = []
    curr: Any = end
    while curr is not None:
        path.append(curr)
        curr = previous.get(curr)
    path.reverse()
    return path


def find_shortest_path_with_transitions(
    adjacency: dict[str, list[dict[str, Any]]],
    start_node_id: str,
    end_node_id: str,
) -> dict[str, Any]:
    """
    Find shortest path between start_node_id and end_node_id using Dijkstra's algorithm.
    Supports stair/floor transitions matching frontend lib/dijkstra.js.
    """
    if not start_node_id or not end_node_id:
        return {"path": [], "totalDistance": 0.0, "floorTransitions": []}

    if start_node_id == end_node_id:
        return {"path": [start_node_id], "totalDistance": 0.0, "floorTransitions": []}

    if start_node_id not in adjacency or end_node_id not in adjacency:
        return {"path": [], "totalDistance": 0.0, "floorTransitions": []}

    distances: dict[str, float] = {node: float("inf") for node in adjacency}
    distances[start_node_id] = 0.0
    previous: dict[str, dict[str, Any] | None] = {}
    unvisited: set[str] = set(adjacency.keys())

    while unvisited:
        current = min(unvisited, key=lambda n: distances[n], default=None)
        if current is None or distances[current] == float("inf"):
            break
        if current == end_node_id:
            break

        unvisited.remove(current)

        for edge in adjacency.get(current, []):
            neighbor = edge["node"]
            if neighbor not in unvisited:
                continue

            weight = edge.get("weight", 1.0)
            alt = distances[current] + weight
            if alt < distances.get(neighbor, float("inf")):
                distances[neighbor] = alt
                previous[neighbor] = {
                    "node": current,
                    "edge": edge,
                }

    if end_node_id not in previous and end_node_id != start_node_id:
        return {"path": [], "totalDistance": 0.0, "floorTransitions": []}

    path: list[str] = []
    curr: str | None = end_node_id
    while curr:
        path.insert(0, curr)
        step = previous.get(curr)
        curr = step["node"] if step else None

    total_dist = round(distances.get(end_node_id, 0.0), 2) if distances.get(end_node_id) != float("inf") else 0.0

    floor_transitions = []
    for i in range(1, len(path)):
        step = previous.get(path[i])
        if step and step.get("edge", {}).get("type") == "stairs":
            edge_info = step["edge"]
            floor_transitions.append({
                "fromNode": path[i - 1],
                "toNode": path[i],
                "fromFloor": str(edge_info.get("fromFloor", "")),
                "toFloor": str(edge_info.get("toFloor", "")),
            })

    return {
        "path": path,
        "totalDistance": total_dist,
        "floorTransitions": floor_transitions,
    }
