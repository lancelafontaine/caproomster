from app.mapper import RoomMapper
from app.mapper import IdMap
from app.core.room import Room
from app.TDG import RoomTDG


def teardown_module(module):
    IdMap.clear(Room)


def test_find_not_found_in_id_map_not_found_in_DB(monkeypatch):
    # Mock
    def no_find(_):
        return
    def no_find2(_, __):
        return
    monkeypatch.setattr(IdMap, 'find', no_find2)
    monkeypatch.setattr(RoomTDG, 'find', no_find)

    # Execute
    val = RoomMapper.find(1)

    # Verify
    assert(val is None)


def test_find_not_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    expected = Room(10)

    # Mock
    def no_find(_, __):
        return

    def yes_find(_):
        return [[expected.getId()]]

    monkeypatch.setattr(IdMap, 'find', no_find)
    monkeypatch.setattr(RoomTDG, 'find', yes_find)

    # Execute
    val = RoomMapper.find(1)

    # Verify
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_not_found_in_DB(monkeypatch):
    # Test Data
    expected = Room(110)

    # Mock
    def id_find(_, __):
        return expected

    def no_find(_):
        return

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(RoomTDG, 'find', no_find)

    # Execute
    val = RoomMapper.find(1)

    # Verify
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    unexpected = Room(10)
    expected = Room(110)

    # Mock
    def id_find(_, __):
        return expected

    def tdg_find(_):
        return [[unexpected.getId()]]

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(RoomTDG, 'find', tdg_find)

    # Execute
    val = RoomMapper.find(1)

    # Verify
    assert(val.getId() is expected.getId())
