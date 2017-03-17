from app.mapper import TimeslotMapper
from app.mapper import TimeslotIdMap
from app.core.timeslot import Timeslot
from app.TDG import TimeslotTDG


def teardown_module(module):
    TimeslotIdMap.clear()


def test_find_not_found_in_id_map_not_found_in_DB(monkeypatch):
    # Mock
    def no_find(_):
        return
    monkeypatch.setattr(TimeslotIdMap, 'find', no_find)
    monkeypatch.setattr(TimeslotTDG, 'find', no_find)

    # Execute
    val = TimeslotMapper.find(1)

    # Verify
    assert(val is None)


def test_find_not_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    expected = Timeslot(1, 5, 'date', 'block', 'id')

    # Mock
    def no_find(_):
        return

    def yes_find(_):
        return [[expected.getId(), expected.getStartTime(), expected.getEndTime(), expected.getDate(), expected.getBlock(), expected.getId()]]

    monkeypatch.setattr(TimeslotIdMap, 'find', no_find)
    monkeypatch.setattr(TimeslotTDG, 'find', yes_find)

    # Execute
    val = TimeslotMapper.find(1)

    # Verify
    assert(val.getStartTime() is expected.getStartTime())
    assert(val.getEndTime() is expected.getEndTime())
    assert(val.getDate() is expected.getDate())
    assert(val.getBlock() is expected.getBlock())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_not_found_in_DB(monkeypatch):
    # Test Data
    expected = Timeslot(1, 5, 'date', 'block', 'id')

    # Mock
    def id_find(_):
        return expected

    def no_find(_):
        return

    monkeypatch.setattr(TimeslotIdMap, 'find', id_find)
    monkeypatch.setattr(TimeslotTDG, 'find', no_find)

    # Execute
    val = TimeslotMapper.find(1)

    # Verify
    assert(val.getStartTime() is expected.getStartTime())
    assert(val.getEndTime() is expected.getEndTime())
    assert(val.getDate() is expected.getDate())
    assert(val.getBlock() is expected.getBlock())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    unexpected = Timeslot(11, 52, 'date2', 'block2', 'id2')
    expected = Timeslot(1, 5, 'date', 'block', 'id')

    # Mock
    def id_find(_):
        return expected

    def tdg_find(_):
        return [[unexpected.getId(), unexpected.getStartTime(), unexpected.getEndTime(), unexpected.getDate(), unexpected.getBlock(), unexpected.getId()]]

    monkeypatch.setattr(TimeslotIdMap, 'find', id_find)
    monkeypatch.setattr(TimeslotTDG, 'find', tdg_find)

    # Execute
    val = TimeslotMapper.find(1)

    # Verify
    assert(val.getStartTime() is expected.getStartTime())
    assert(val.getEndTime() is expected.getEndTime())
    assert(val.getDate() is expected.getDate())
    assert(val.getBlock() is expected.getBlock())
    assert(val.getId() is expected.getId())
