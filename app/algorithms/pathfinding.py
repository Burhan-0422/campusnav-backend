"""Simple pathfinding utilities."""


def dijkstra(graph: dict[int, list[tuple[int, int]]], start: int, end: int) -> list[int]:
    """Return the shortest path from start to end using Dijkstra's algorithm."""
    if start == end:
        return [start]

    distances = {node: float("inf") for node in graph}
    distances[start] = 0
    previous: dict[int, int | None] = {start: None}
    visited: set[int] = set()

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

    path: list[int] = []
    current: int | None = end
    while current is not None:
        path.append(current)
        current = previous.get(current)
    path.reverse()
    return path
