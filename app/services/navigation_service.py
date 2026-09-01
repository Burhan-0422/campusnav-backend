"""Navigation route logic placeholder."""


class NavigationService:
    def __init__(self):
        self.graph = {}

    def add_route(self, start: int, end: int, weight: int = 1) -> None:
        self.graph.setdefault(start, []).append((end, weight))

    def shortest_path(self, start: int, end: int) -> list[int]:
        if start == end:
            return [start]

        if start not in self.graph:
            return []

        visited = set()
        queue = [start]
        previous = {start: None}

        while queue:
            node = queue.pop(0)
            if node == end:
                break
            for neighbor, _ in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    previous[neighbor] = node
                    queue.append(neighbor)

        if end not in previous:
            return []

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path
