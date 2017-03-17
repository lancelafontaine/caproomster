from app.mapper import RoomMapper
from app.mapper import RoomIdMap
from app.core.room import Room
from app.TDG import RoomTDG


def teardown_module(module):
    RoomIdMap.clear()


def test_find_not_found_in_id_map_not_found_in_DB(monkeypatch):
    # Mock
    def no_find(_):
        return
    monkeypatch.setattr(RoomIdMap, 'find', no_find)
    monkeypatch.setattr(RoomTDG, 'find', no_find)

    # Execute
    val = RoomMapper.find(1)

    # Verify
    assert(val is None)


def test_find_not_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    expected = Room(10, 'lock')

    # Mock
    def no_find(_):
        return

    def yes_find(_):
        return [[expected.getId(), expected.getLock()]]

    monkeypatch.setattr(RoomIdMap, 'find', no_find)
    monkeypatch.setattr(RoomTDG, 'find', yes_find)

    # Execute
    val = RoomMapper.find(1)

    # Verify
    assert(val.getLock() is expected.getLock())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_not_found_in_DB(monkeypatch):
    # Test Data
    expected = Room(110, 'lock')

    # Mock
    def id_find(_):
        return expected

    def no_find(_):
        return

    monkeypatch.setattr(RoomIdMap, 'find', id_find)
    monkeypatch.setattr(RoomTDG, 'find', no_find)

    # Execute
    val = RoomMapper.find(1)

    # Verify
    assert(val.getLock() is expected.getLock())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    unexpected = Room(10, 'lock')
    expected = Room(110, 'lock2')

    # Mock
    def id_find(_):
        return expected

    def tdg_find(_):
        return [[unexpected.getId(), unexpected.getLock()]]

    monkeypatch.setattr(RoomIdMap, 'find', id_find)
    monkeypatch.setattr(RoomTDG, 'find', tdg_find)

    # Execute
    val = RoomMapper.find(1)

    # Verify
    assert(val.getLock() is expected.getLock())
    assert(val.getId() is expected.getId())
