"""Location operations placeholder."""


class LocationService:
    def __init__(self):
        self.locations = []

    def add_location(self, name: str, x: float, y: float) -> dict[str, float | str]:
        self.locations.append({"name": name, "x": x, "y": y})
        return {"name": name, "x": x, "y": y}
