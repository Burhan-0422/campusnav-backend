from app.schemas.location import NavLocationItem
from seed_database import FLOOR_1_ROOMS, FLOOR_2_ROOMS, FLOOR_3_ROOMS
import re

ROOM_CODE_PATTERN = re.compile(r"([A-Z]-\d{3}[A-Z]?)")


def test_nav_location_item_schema():
    loc = NavLocationItem(
        id="LOC-1",
        name="B-406 Classroom",
        category="Classroom",
        nodeId="N18",
        roomCode="B-406",
        subtitle="Classroom • Floor 3",
        floor="3",
    )
    assert loc.id == "LOC-1"
    assert loc.name == "B-406 Classroom"
    assert loc.roomCode == "B-406"
    assert loc.floor == "3"


def test_seed_rooms_validation():
    # Verify all room entries in seed_database produce valid NavLocationItems
    total_rooms = 0
    for floor_num, rooms in [("1", FLOOR_1_ROOMS), ("2", FLOOR_2_ROOMS), ("3", FLOOR_3_ROOMS)]:
        for idx, (node_id, label, category) in enumerate(rooms):
            match = ROOM_CODE_PATTERN.search(label)
            room_code = match.group(1) if match else None
            item = NavLocationItem(
                id=f"LOC-{floor_num}-{idx}",
                name=label,
                category=category,
                nodeId=node_id,
                roomCode=room_code,
                subtitle=f"{category} • Floor {floor_num}",
                floor=floor_num,
            )
            assert item.nodeId == node_id
            assert item.floor == floor_num
            total_rooms += 1

    assert total_rooms >= 70
