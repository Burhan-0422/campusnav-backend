"""
Seed database script for CampusNav.
Populates PostgreSQL with departments, buildings, floors, nodes, edges, and locations
matching the campusnav-frontend data.
"""

import math
import sys
from app.db.database import SessionLocal, engine, Base
from sqlalchemy import create_engine
from app.models import Department, Building, Floor, Node, Edge, Location

# Floor 3 Data from floorData.js
FLOOR_3_NODES = [
    {"id": "N0", "x": 160, "y": 585, "type": "Entry", "name": "Staircase (Entrance)"},
    {"id": "N1", "x": 213, "y": 480, "type": "corridor", "name": "Server Room door"},
    {"id": "N2", "x": 294, "y": 480, "type": "corridor", "name": "Network & Security Lab door"},
    {"id": "N3", "x": 383, "y": 480, "type": "corridor", "name": "Electronics & Signal Processing Lab door"},
    {"id": "N4", "x": 474, "y": 480, "type": "corridor", "name": "Programing Paradigm Lab door"},
    {"id": "N5", "x": 561, "y": 480, "type": "corridor", "name": "Project Lab door"},
    {"id": "N6", "x": 610, "y": 480, "type": "Junction", "name": "Bottom-Right junction"},
    {"id": "N7", "x": 610, "y": 320, "type": "corridor", "name": "Database & Analytics Lab door"},
    {"id": "N8", "x": 610, "y": 190, "type": "corridor", "name": "Cloud Computing Lab door"},
    {"id": "N9", "x": 610, "y": 95, "type": "Junction", "name": "Top-Right junction"},
    {"id": "N10", "x": 670, "y": 95, "type": "corridor", "name": "System Programing Lab door"},
    {"id": "N11", "x": 575, "y": 95, "type": "corridor", "name": "Artificial Intelligence Lab door"},
    {"id": "N12", "x": 490, "y": 95, "type": "corridor", "name": "Software Engineering Lab door"},
    {"id": "N13", "x": 423, "y": 95, "type": "corridor", "name": "Staff Toilet door"},
    {"id": "N14", "x": 370, "y": 95, "type": "corridor", "name": "Boys Toilet door"},
    {"id": "N15", "x": 266, "y": 95, "type": "corridor", "name": "B-409 Seminar Hall door"},
    {"id": "N16", "x": 195, "y": 95, "type": "corridor", "name": "B-408 Classroom door"},
    {"id": "N17", "x": 122, "y": 95, "type": "corridor", "name": "B-407 Classroom door"},
    {"id": "N18", "x": 49, "y": 95, "type": "corridor", "name": "B-406 Classroom door"},
    {"id": "N19", "x": 85, "y": 95, "type": "Junction", "name": "Top-Left junction"},
    {"id": "N20", "x": 85, "y": 152, "type": "corridor", "name": "B-405 Classroom door"},
    {"id": "N21", "x": 85, "y": 237, "type": "corridor", "name": "B-404 Classroom door"},
    {"id": "N22", "x": 85, "y": 317, "type": "corridor", "name": "Girls Toilet door"},
    {"id": "N23", "x": 85, "y": 480, "type": "Junction", "name": "Bottom-Left junction"},
    {"id": "N24", "x": 122, "y": 480, "type": "corridor", "name": "CSE AIML Lab-1 door"},
    {"id": "N25", "x": 49, "y": 480, "type": "corridor", "name": "CSE DS Lab-1 door"},
    {"id": "N26", "x": 85, "y": 402, "type": "corridor", "name": "ECE Admin door"},
    {"id": "N27", "x": 315, "y": 95, "type": "Junction", "name": "Middle passage, top"},
    {"id": "N28", "x": 315, "y": 480, "type": "Junction", "name": "Middle passage, bottom"},
    {"id": "N29", "x": 315, "y": 252, "type": "corridor", "name": "Admin Lounge/Staff Room door"},
    {"id": "N30", "x": 320, "y": 95, "type": "Staircase", "name": "Back staircase landing"},
]

FLOOR_3_EDGES = [
    ("N18", "N19"), ("N19", "N17"), ("N17", "N16"), ("N16", "N15"), ("N15", "N27"),
    ("N27", "N30"), ("N30", "N14"), ("N14", "N13"), ("N13", "N12"), ("N12", "N11"),
    ("N11", "N10"), ("N10", "N9"), ("N9", "N8"), ("N8", "N7"), ("N7", "N6"),
    ("N6", "N5"), ("N5", "N4"), ("N4", "N3"), ("N3", "N28"), ("N28", "N2"),
    ("N2", "N1"), ("N1", "N0"), ("N0", "N24"), ("N24", "N23"), ("N23", "N25"),
    ("N23", "N26"), ("N26", "N22"), ("N22", "N21"), ("N21", "N20"), ("N20", "N19"),
    ("N27", "N29"), ("N29", "N28"),
]

FLOOR_3_ROOMS = [
    ("N18", "B-406 Classroom", "Classroom"),
    ("N17", "B-407 Classroom", "Classroom"),
    ("N16", "B-408 Classroom", "Classroom"),
    ("N15", "B-409 Seminar Hall", "Classroom"),
    ("N14", "Boys Toilet", "Washroom"),
    ("N13", "Staff Toilet", "Washroom"),
    ("N12", "Software Engineering Lab", "Lab"),
    ("N11", "Artificial Intelligence Lab", "Lab"),
    ("N10", "System Programing Lab", "Lab"),
    ("N8", "Cloud Computing Lab", "Lab"),
    ("N7", "Database & Analytics Lab", "Lab"),
    ("N5", "Project Lab 418", "Lab"),
    ("N4", "Programing Paradigm Lab", "Lab"),
    ("N3", "Electronics & Signal Processing Lab", "Lab"),
    ("N2", "Network & Security Lab", "Lab"),
    ("N1", "Server Room", "Admin"),
    ("N24", "CSE AIML Lab-1", "Lab"),
    ("N25", "CSE DS Lab-1", "Lab"),
    ("N26", "ECE Admin", "Admin"),
    ("N22", "Girls Toilet", "Washroom"),
    ("N21", "B-404 Classroom", "Classroom"),
    ("N20", "B-405 Classroom", "Classroom"),
    ("N29", "Admin Lounge/Staff Room", "Admin"),
    ("N0", "Staircase (3rd Floor Entrance)", "Entrance"),
    ("N30", "Back Staircase (Floor 3)", "Entrance"),
]

# Floor 2 Data from floor2Data.js (updated to match frontend simplified geometry)
FLOOR_2_NODES = [
    {"id": "F2-N0", "x": 286, "y": 585, "type": "Staircase", "name": "Front Staircase"},
    {"id": "F2-N1", "x": 337, "y": 480, "type": "corridor", "name": "B-319 Girls Common Room door"},
    {"id": "F2-N2", "x": 410, "y": 480, "type": "corridor", "name": "B-318 ECS Lab-1 door"},
    {"id": "F2-N3", "x": 505, "y": 480, "type": "corridor", "name": "B-317 ECS Lab-2 door"},
    {"id": "F2-N4", "x": 590, "y": 480, "type": "corridor", "name": "B-316 ECS CR2 door"},
    {"id": "F2-N5", "x": 668, "y": 480, "type": "corridor", "name": "B-315 ECS CR1 door"},
    {"id": "F2-N6", "x": 610, "y": 480, "type": "Junction", "name": "Bottom-Right junction"},
    {"id": "F2-N7", "x": 610, "y": 320, "type": "corridor", "name": "B-314 ECS Project Lab door"},
    {"id": "F2-N8", "x": 610, "y": 190, "type": "corridor", "name": "B-313 ECS Lab 3 door"},
    {"id": "F2-N9", "x": 610, "y": 95, "type": "Junction", "name": "Top-Right junction"},
    {"id": "F2-N10", "x": 640, "y": 95, "type": "corridor", "name": "B-312 ECS Lab 4 door"},
    {"id": "F2-N11", "x": 535, "y": 95, "type": "corridor", "name": "B-311 ECS Lab 5 door"},
    {"id": "F2-N12", "x": 452, "y": 95, "type": "corridor", "name": "B-310 ECE Lab 6 door"},
    {"id": "F2-N13", "x": 382, "y": 95, "type": "corridor", "name": "Boys Toilet door"},
    {"id": "F2-N14", "x": 333, "y": 95, "type": "Junction", "name": "Top-Center junction"},
    {"id": "F2-N15", "x": 286, "y": 95, "type": "corridor", "name": "Girls Toilet door"},
    {"id": "F2-N16", "x": 222, "y": 95, "type": "corridor", "name": "B-308 FE CR1 door"},
    {"id": "F2-N17", "x": 149, "y": 95, "type": "corridor", "name": "B-307 ECE Lab 3 door"},
    {"id": "F2-N18", "x": 62, "y": 95, "type": "corridor", "name": "B-306 ECE Project Lab door"},
    {"id": "F2-N19", "x": 85, "y": 95, "type": "Junction", "name": "Top-Left junction"},
    {"id": "F2-N20", "x": 85, "y": 152, "type": "corridor", "name": "B-305 ECE Lab 4 door"},
    {"id": "F2-N21", "x": 85, "y": 237, "type": "corridor", "name": "B-304 ECE Lab 3 door"},
    {"id": "F2-N22", "x": 85, "y": 317, "type": "corridor", "name": "Staff Toilet door"},
    {"id": "F2-N23", "x": 85, "y": 480, "type": "Junction", "name": "Bottom-Left junction"},
    {"id": "F2-N24", "x": 46, "y": 480, "type": "corridor", "name": "B-303 ECE Lab 2 door"},
    {"id": "F2-N25", "x": 129, "y": 480, "type": "corridor", "name": "B-302 ECE CR2 door"},
    {"id": "F2-N26", "x": 216, "y": 480, "type": "corridor", "name": "B-301 ECE CR1 door"},
    {"id": "F2-N27", "x": 315, "y": 480, "type": "Junction", "name": "Bottom-Center junction"},
    {"id": "F2-S1", "x": 333, "y": 74, "type": "Staircase", "name": "Back Staircase"},
    {"id": "F2-I0", "x": 315, "y": 130, "type": "Junction", "name": "Inner top junction"},
    {"id": "F2-I3", "x": 315, "y": 255, "type": "corridor", "name": "B-320 ECS Lab 4 door"},
    {"id": "F2-I5", "x": 315, "y": 430, "type": "Junction", "name": "Inner bottom junction"},
]

FLOOR_2_EDGES = [
    ("F2-N0", "F2-N27"), ("F2-N27", "F2-N1"), ("F2-N1", "F2-N2"), ("F2-N2", "F2-N3"),
    ("F2-N3", "F2-N4"), ("F2-N4", "F2-N5"), ("F2-N5", "F2-N6"), ("F2-N6", "F2-N7"),
    ("F2-N7", "F2-N8"), ("F2-N8", "F2-N9"), ("F2-N9", "F2-N10"), ("F2-N10", "F2-N11"),
    ("F2-N11", "F2-N12"), ("F2-N12", "F2-N13"), ("F2-N13", "F2-N14"), ("F2-N14", "F2-N15"),
    ("F2-N15", "F2-N16"), ("F2-N16", "F2-N17"), ("F2-N17", "F2-N18"), ("F2-N18", "F2-N19"),
    ("F2-N19", "F2-N20"), ("F2-N20", "F2-N21"), ("F2-N21", "F2-N22"), ("F2-N22", "F2-N23"),
    ("F2-N23", "F2-N24"), ("F2-N24", "F2-N25"), ("F2-N25", "F2-N26"), ("F2-N26", "F2-N27"),
    ("F2-N14", "F2-S1"), ("F2-N14", "F2-I0"),
    ("F2-I0", "F2-I3"), ("F2-I3", "F2-I5"), ("F2-I5", "F2-N27"),
]

FLOOR_2_ROOMS = [
    ("F2-N18", "B-306 ECE Project Lab / FE CR2", "Lab"),
    ("F2-N17", "B-307 ECE Lab 3", "Lab"),
    ("F2-N16", "B-308 FE CR1", "Classroom"),
    ("F2-N15", "Girls Toilet", "Washroom"),
    ("F2-N13", "Boys Toilet", "Washroom"),
    ("F2-N12", "B-310 ECE Lab 6", "Lab"),
    ("F2-N11", "B-311 ECS Lab 5", "Lab"),
    ("F2-N10", "B-312 ECS Lab 4", "Lab"),
    ("F2-N8", "B-313 ECS Lab 3", "Lab"),
    ("F2-N7", "B-314 ECS Project Lab", "Lab"),
    ("F2-N24", "B-303 ECE Lab 2", "Lab"),
    ("F2-N25", "B-302 ECE CR2", "Classroom"),
    ("F2-N26", "B-301 ECE CR1", "Classroom"),
    ("F2-N1", "B-319 Girls Common Room", "Admin"),
    ("F2-N2", "B-318 ECS Lab-1", "Lab"),
    ("F2-N3", "B-317 ECS Lab-2", "Lab"),
    ("F2-N4", "B-316 ECS CR2", "Classroom"),
    ("F2-N5", "B-315 ECS CR1", "Classroom"),
    ("F2-N20", "B-305 ECE Lab 4", "Lab"),
    ("F2-N21", "B-304 ECE Lab 3", "Lab"),
    ("F2-N22", "Staff Toilet", "Washroom"),
    ("F2-I3", "B-320 ECS Lab 4", "Lab"),
    ("F2-N0", "Front Staircase (Floor 2)", "Entrance"),
    ("F2-S1", "Back Staircase (Floor 2)", "Entrance"),
]

# Floor 1 Data from floor1Data.js
FLOOR_1_NODES = [
    {"id": "F1-N0", "x": 266, "y": 585, "type": "Staircase", "name": "Front Staircase"},
    {"id": "F1-N1", "x": 320, "y": 480, "type": "corridor", "name": "Corridor node 1"},
    {"id": "F1-N2", "x": 410, "y": 480, "type": "corridor", "name": "B-216 Tom Lab door"},
    {"id": "F1-N3", "x": 505, "y": 480, "type": "corridor", "name": "B-215 Classroom door"},
    {"id": "F1-N4", "x": 590, "y": 480, "type": "corridor", "name": "B-214 Classroom door"},
    {"id": "F1-N5", "x": 620, "y": 480, "type": "Junction", "name": "Bottom-Right junction"},
    {"id": "F1-N6", "x": 620, "y": 390, "type": "corridor", "name": "B-212 Drawing Hall-2 door"},
    {"id": "F1-N7", "x": 620, "y": 250, "type": "corridor", "name": "B-211 Drawing Hall-1 door"},
    {"id": "F1-N8", "x": 620, "y": 95, "type": "Junction", "name": "Top-Right junction"},
    {"id": "F1-N9", "x": 590, "y": 95, "type": "corridor", "name": "B-208 / B-209 door"},
    {"id": "F1-N10", "x": 440, "y": 95, "type": "corridor", "name": "Boys Toilet door"},
    {"id": "F1-N11", "x": 358, "y": 95, "type": "corridor", "name": "Female Staff Toilet door"},
    {"id": "F1-N12", "x": 399, "y": 95, "type": "Staircase", "name": "Back Staircase"},
    {"id": "F1-N13", "x": 350, "y": 95, "type": "corridor", "name": "B-207B Civil Engg Project Lab door"},
    {"id": "F1-N14", "x": 266, "y": 95, "type": "corridor", "name": "B-207A ISRO Lab door"},
    {"id": "F1-N15", "x": 195, "y": 95, "type": "corridor", "name": "B-206C Classroom door"},
    {"id": "F1-N16", "x": 122, "y": 95, "type": "corridor", "name": "B-206B Survey Lab door"},
    {"id": "F1-N17", "x": 49, "y": 95, "type": "corridor", "name": "B-206A Classroom door"},
    {"id": "F1-N18", "x": 85, "y": 95, "type": "Junction", "name": "Top-Left junction"},
    {"id": "F1-N19", "x": 85, "y": 210, "type": "corridor", "name": "B-205 Environmental Engg Lab door"},
    {"id": "F1-N20", "x": 85, "y": 315, "type": "corridor", "name": "B-204 Engg Geology Lab door"},
    {"id": "F1-N21", "x": 85, "y": 410, "type": "corridor", "name": "Conduction Room / Staff Toilet door"},
    {"id": "F1-N22", "x": 85, "y": 480, "type": "Junction", "name": "Bottom-Left junction"},
    {"id": "F1-N23", "x": 45, "y": 480, "type": "corridor", "name": "B-203 Classroom door"},
    {"id": "F1-N24", "x": 130, "y": 480, "type": "corridor", "name": "B-202 Classroom door"},
    {"id": "F1-N25", "x": 220, "y": 480, "type": "corridor", "name": "B-201 Classroom door"},
    {"id": "F1-M0", "x": 365, "y": 95, "type": "Junction", "name": "Mid corridor top junction"},
    {"id": "F1-C1", "x": 365, "y": 200, "type": "corridor", "name": "B-218 Staffroom door"},
    {"id": "F1-C2", "x": 365, "y": 315, "type": "corridor", "name": "Conference Room door"},
    {"id": "F1-M2", "x": 365, "y": 480, "type": "Junction", "name": "Mid corridor bottom junction"},
]

FLOOR_1_EDGES = [
    ("F1-N0", "F1-N1"), ("F1-N1", "F1-N2"), ("F1-N2", "F1-N3"), ("F1-N3", "F1-N4"), ("F1-N4", "F1-N5"),
    ("F1-N5", "F1-N6"), ("F1-N6", "F1-N7"), ("F1-N7", "F1-N8"), ("F1-N8", "F1-N9"), ("F1-N9", "F1-N10"),
    ("F1-N10", "F1-N12"), ("F1-N12", "F1-N11"), ("F1-N11", "F1-N13"), ("F1-N13", "F1-N14"), ("F1-N14", "F1-N15"),
    ("F1-N15", "F1-N16"), ("F1-N16", "F1-N17"), ("F1-N17", "F1-N18"), ("F1-N18", "F1-N19"), ("F1-N19", "F1-N20"),
    ("F1-N20", "F1-N21"), ("F1-N21", "F1-N22"), ("F1-N22", "F1-N23"), ("F1-N23", "F1-N24"), ("F1-N24", "F1-N25"),
    ("F1-N25", "F1-N0"),
    ("F1-N11", "F1-M0"), ("F1-M0", "F1-C1"), ("F1-C1", "F1-C2"), ("F1-C2", "F1-M2"), ("F1-M2", "F1-N1"),
]

FLOOR_1_ROOMS = [
    ("F1-N17", "B-206A Classroom", "Classroom"),
    ("F1-N16", "B-206B Survey Lab", "Lab"),
    ("F1-N15", "B-206C Classroom", "Classroom"),
    ("F1-N14", "B-207A ISRO Lab", "Lab"),
    ("F1-N13", "B-207B Civil Engg Project Lab", "Lab"),
    ("F1-N11", "Female Staff Toilet", "Washroom"),
    ("F1-N10", "Boys Toilet", "Washroom"),
    ("F1-N9", "B-208 Classroom", "Classroom"),
    ("F1-N9", "B-209 CADD Lab", "Lab"),
    ("F1-N8", "B-210 Classroom", "Classroom"),
    ("F1-N7", "B-211 Drawing Hall-1", "Classroom"),
    ("F1-N6", "B-212 Drawing Hall-2", "Classroom"),
    ("F1-N5", "B-213 Class Room", "Classroom"),
    ("F1-N4", "B-214 Classroom", "Classroom"),
    ("F1-N3", "B-215 Classroom", "Classroom"),
    ("F1-N2", "B-216 Tom Lab", "Lab"),
    ("F1-N1", "B-217 Exam Cell", "Admin"),
    ("F1-N25", "B-201 Classroom", "Classroom"),
    ("F1-N24", "B-202 Classroom", "Classroom"),
    ("F1-N23", "B-203 Classroom", "Classroom"),
    ("F1-N21", "Conduction Room", "Admin"),
    ("F1-N21", "Staff Toilet", "Washroom"),
    ("F1-N20", "B-204 Engineering Geology Lab", "Lab"),
    ("F1-N19", "B-205 Environmental Engineering Lab", "Lab"),
    ("F1-C1", "Civil HOD / B-218 Staffroom", "Admin"),
    ("F1-C2", "Conference Room", "Admin"),
    ("F1-N0", "Front Staircase (1st Floor)", "Entrance"),
    ("F1-N12", "Back Staircase (Floor 1)", "Entrance"),
]

# Multi-floor stair connections (bidirectional) from floorData.js
STAIR_CONNECTIONS = [
    # (from_node, to_node, weight, from_floor_num, to_floor_num)
    ("N0", "F2-N0", 45.0, 3, 2),
    ("N30", "F2-S1", 45.0, 3, 2),
    ("F1-N0", "F2-N0", 45.0, 1, 2),
    ("F1-N12", "F2-S1", 45.0, 1, 2),
]


def calculate_distance(node_map, u, v):
    n1 = node_map.get(u)
    n2 = node_map.get(v)
    if not n1 or not n2:
        return 1.0
    dx = n1["x"] - n2["x"]
    dy = n1["y"] - n2["y"]
    return round(math.sqrt(dx * dx + dy * dy), 2)


def seed_database(db_url, reset=False):
    target_engine = create_engine(db_url)
    Base.metadata.create_all(bind=target_engine)
    from sqlalchemy.orm import sessionmaker
    TargetSession = sessionmaker(bind=target_engine)
    session = TargetSession()

    try:
        # Check if already seeded
        dept_count = session.query(Department).count()
        floor_count = session.query(Floor).count()
        if dept_count > 0 and floor_count >= 3 and not reset:
            print(f"Database at {target_engine.url.database} already has 3 floors. Skipping. (Pass --reset to reseed)")
            return

        if reset or dept_count > 0:
            print(f"Clearing existing navigation data in {target_engine.url.database} to ensure clean sync...")
            session.query(Location).delete()
            session.query(Edge).delete()
            session.query(Node).delete()
            session.query(Floor).delete()
            session.query(Building).delete()
            session.query(Department).delete()
            session.commit()

        print(f"Seeding database at {target_engine.url.database} with Floors 1, 2, 3 and stair connections...")

        # 1. Departments
        dept_eng = Department(name="Engineering", code="ENG", description="Faculty of Engineering & Technology")
        dept_pharm = Department(name="Pharmacy", code="PHARM", description="Faculty of Pharmacy")
        dept_arch = Department(name="Architecture", code="ARCH", description="Faculty of Architecture")
        session.add_all([dept_eng, dept_pharm, dept_arch])
        session.flush()

        # 2. Buildings
        bldg = Building(
            department_id=dept_eng.id,
            name="Engineering Building",
            code="ENG-MAIN",
            description="Main Engineering Building with Labs, Classrooms, and Faculty Rooms"
        )
        session.add(bldg)
        session.flush()

        # 3. Floors (1, 2, and 3)
        floor1 = Floor(building_id=bldg.id, floor_number=1, name="First Floor")
        floor2 = Floor(building_id=bldg.id, floor_number=2, name="Second Floor")
        floor3 = Floor(building_id=bldg.id, floor_number=3, name="Third Floor")
        session.add_all([floor1, floor2, floor3])
        session.flush()

        floor_map = {1: floor1, 2: floor2, 3: floor3}

        # 4. Nodes
        node_lookup = {}
        for n in FLOOR_1_NODES:
            node = Node(id=n["id"], floor_id=floor1.id, name=n["name"], type=n["type"], notes=f"Coordinates: ({n['x']}, {n['y']})")
            session.add(node)
            node_lookup[n["id"]] = n

        for n in FLOOR_2_NODES:
            node = Node(id=n["id"], floor_id=floor2.id, name=n["name"], type=n["type"], notes=f"Coordinates: ({n['x']}, {n['y']})")
            session.add(node)
            node_lookup[n["id"]] = n

        for n in FLOOR_3_NODES:
            node = Node(id=n["id"], floor_id=floor3.id, name=n["name"], type=n["type"], notes=f"Coordinates: ({n['x']}, {n['y']})")
            session.add(node)
            node_lookup[n["id"]] = n

        session.flush()

        # 5. Edges
        edge_count = 0
        for u, v in FLOOR_1_EDGES:
            dist = calculate_distance(node_lookup, u, v)
            session.add(Edge(floor_id=floor1.id, from_node=u, to_node=v, distance=dist))
            session.add(Edge(floor_id=floor1.id, from_node=v, to_node=u, distance=dist))
            edge_count += 2

        for u, v in FLOOR_2_EDGES:
            dist = calculate_distance(node_lookup, u, v)
            session.add(Edge(floor_id=floor2.id, from_node=u, to_node=v, distance=dist))
            session.add(Edge(floor_id=floor2.id, from_node=v, to_node=u, distance=dist))
            edge_count += 2

        for u, v in FLOOR_3_EDGES:
            dist = calculate_distance(node_lookup, u, v)
            session.add(Edge(floor_id=floor3.id, from_node=u, to_node=v, distance=dist))
            session.add(Edge(floor_id=floor3.id, from_node=v, to_node=u, distance=dist))
            edge_count += 2

        # 5b. Stair Connections (Inter-floor edges)
        for u, v, weight, f1_num, f2_num in STAIR_CONNECTIONS:
            f1 = floor_map[f1_num]
            f2 = floor_map[f2_num]
            session.add(Edge(floor_id=f1.id, from_node=u, to_node=v, distance=weight))
            session.add(Edge(floor_id=f2.id, from_node=v, to_node=u, distance=weight))
            edge_count += 2

        session.flush()

        # 6. Locations
        loc_count = 0
        for node_id, label, cat in FLOOR_1_ROOMS:
            loc = Location(node_id=node_id, label=label, category=cat)
            session.add(loc)
            loc_count += 1

        for node_id, label, cat in FLOOR_2_ROOMS:
            loc = Location(node_id=node_id, label=label, category=cat)
            session.add(loc)
            loc_count += 1

        for node_id, label, cat in FLOOR_3_ROOMS:
            loc = Location(node_id=node_id, label=label, category=cat)
            session.add(loc)
            loc_count += 1

        session.commit()
        print(f"Successfully seeded {target_engine.url.database}:")
        print(f"  - 3 Departments")
        print(f"  - 1 Building")
        print(f"  - 3 Floors (Floor 1, 2 & 3)")
        print(f"  - {len(node_lookup)} Navigation Nodes")
        print(f"  - {edge_count} Navigation Edges (including multi-floor stairs)")
        print(f"  - {loc_count} Locations / Rooms")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database {target_engine.url.database}:", e)
        raise e
    finally:
        session.close()


if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv
    # Seed both campusnav and postgres databases so the user sees all data in pgAdmin whichever they open
    seed_database("postgresql+psycopg2://postgres:admin@localhost:5432/campusnav", reset=reset_flag)
    seed_database("postgresql+psycopg2://postgres:admin@localhost:5432/postgres", reset=reset_flag)
