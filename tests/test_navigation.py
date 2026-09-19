from app.algorithms.pathfinding import dijkstra, find_shortest_path_with_transitions
from seed_database import (
    FLOOR_1_NODES,
    FLOOR_1_EDGES,
    FLOOR_2_NODES,
    FLOOR_2_EDGES,
    FLOOR_3_NODES,
    FLOOR_3_EDGES,
    STAIR_CONNECTIONS,
    calculate_distance,
)


def build_test_graph():
    node_lookup = {}
    for n in FLOOR_1_NODES + FLOOR_2_NODES + FLOOR_3_NODES:
        node_lookup[n["id"]] = n

    adjacency = {n["id"]: [] for n in FLOOR_1_NODES + FLOOR_2_NODES + FLOOR_3_NODES}

    def add_edges(edges, floor_str):
        for u, v in edges:
            dist = calculate_distance(node_lookup, u, v)
            adjacency[u].append({"node": v, "weight": dist, "type": "corridor", "fromFloor": floor_str, "toFloor": floor_str})
            adjacency[v].append({"node": u, "weight": dist, "type": "corridor", "fromFloor": floor_str, "toFloor": floor_str})

    add_edges(FLOOR_1_EDGES, "1")
    add_edges(FLOOR_2_EDGES, "2")
    add_edges(FLOOR_3_EDGES, "3")

    for u, v, weight, f1_num, f2_num in STAIR_CONNECTIONS:
        adjacency[u].append({"node": v, "weight": weight, "type": "stairs", "fromFloor": str(f1_num), "toFloor": str(f2_num)})
        adjacency[v].append({"node": u, "weight": weight, "type": "stairs", "fromFloor": str(f2_num), "toFloor": str(f1_num)})

    return adjacency


def test_dijkstra_basic_integer_compatibility():
    # Backward compatibility with integer node graph
    graph = {
        1: [(2, 1.0), (3, 4.0)],
        2: [(1, 1.0), (3, 2.0)],
        3: [(1, 4.0), (2, 2.0)],
    }
    path = dijkstra(graph, 1, 3)
    assert path == [1, 2, 3]


def test_floor1_same_floor_navigation():
    adjacency = build_test_graph()
    # Path between B-206A door (F1-N17) and Front Staircase (F1-N0)
    result = find_shortest_path_with_transitions(adjacency, "F1-N17", "F1-N0")
    assert len(result["path"]) > 0
    assert result["path"][0] == "F1-N17"
    assert result["path"][-1] == "F1-N0"
    assert result["totalDistance"] > 0
    assert result["floorTransitions"] == []


def test_floor2_simplified_geometry_navigation():
    adjacency = build_test_graph()
    # Path across new central spine on Floor 2: from top-center (F2-N14) through F2-I0, F2-I3, F2-I5 to bottom-center (F2-N27)
    result = find_shortest_path_with_transitions(adjacency, "F2-N14", "F2-N27")
    assert len(result["path"]) > 0
    assert result["path"][0] == "F2-N14"
    assert result["path"][-1] == "F2-N27"
    assert result["totalDistance"] > 0


def test_multifloor_navigation_floor1_to_floor3():
    adjacency = build_test_graph()
    # Route from Floor 1 classroom (F1-N17) to Floor 3 Server Room (N1)
    result = find_shortest_path_with_transitions(adjacency, "F1-N17", "N1")
    assert len(result["path"]) > 0
    assert result["path"][0] == "F1-N17"
    assert result["path"][-1] == "N1"
    assert len(result["floorTransitions"]) >= 1
    # Check that transitions include the stair climbing
    floors_visited = {t["fromFloor"] for t in result["floorTransitions"]}.union({t["toFloor"] for t in result["floorTransitions"]})
    assert "1" in floors_visited or "2" in floors_visited
