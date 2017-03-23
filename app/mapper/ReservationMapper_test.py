from app.mapper import ReservationMapper
from app.mapper import TimeslotMapper
from app.mapper import IdMap
from app.core.reservation import Reservation
from app.core.user import User
from app.core.timeslot import Timeslot
from app.core.room import Room
from app.TDG import ReservationTDG


def teardown_module(module):
    IdMap.clear(Reservation)


def test_find_not_found_in_id_map_not_found_in_DB(monkeypatch):
    # Mock
    def no_find(_):
        return

    def no_find2(_, __):
        return
    monkeypatch.setattr(IdMap, 'find', no_find2)
    monkeypatch.setattr(ReservationTDG, 'find', no_find)

    # Execute
    val = ReservationMapper.find(1)

    # Verify
    assert(val is None)


def test_find_not_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    expected_timeslot = Timeslot(1, 2, 'date', 'block', 1)
    expected = Reservation(Room(1, 'a'), User(
        1, 'name', 'password'), expected_timeslot, 'description', 1)

    # Mock
    def no_find(_, __):
        return

    def yes_find(_):
        return [[expected.getId(), expected.getRoom().getId(), expected.getDescription(), expected.getUser().getId(), expected_timeslot.getId()]]

    def timeslot_find(_):
        return expected_timeslot

    monkeypatch.setattr(IdMap, 'find', no_find)
    monkeypatch.setattr(ReservationTDG, 'find', yes_find)
    monkeypatch.setattr(TimeslotMapper, 'find', timeslot_find)

    # Execute
    val = ReservationMapper.find(1)

    # Verify
    assert(val.getRoom().getId() is expected.getRoom().getId())
    assert(val.getDescription() is expected.getDescription())
    assert(val.getTimeslot().getId() is expected.getTimeslot().getId())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_not_found_in_DB(monkeypatch):
    # Test Data
    expected = Reservation('room', User(
        1, 'name', 'password'), 'time', 'description', 1)

    # Mock
    def id_find(_, __):
        return expected

    def no_find(_):
        return

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(ReservationTDG, 'find', no_find)

    # Execute
    val = ReservationMapper.find(1)

    # Verify
    assert(val.getRoom() is expected.getRoom())
    assert(val.getDescription() is expected.getDescription())
    assert(val.getTimeslot() is expected.getTimeslot())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    unexpected = Reservation('room', User(
        1, 'name', 'password'), 'time', 'description', 1)
    expected = Reservation('room1', User(
        1, 'name2', 'password3'), 'time1', 'description2', 2)

    # Mock
    def id_find(_, __):
        return expected

    def tdg_find(_):
        return [[unexpected.getId(), unexpected.getRoom()]]

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(ReservationTDG, 'find', tdg_find)

    # Execute
    val = ReservationMapper.find(1)

    # Verify
    assert(val.getRoom() is expected.getRoom())
    assert(val.getDescription() is expected.getDescription())
    assert(val.getTimeslot() is expected.getTimeslot())
    assert(val.getId() is expected.getId())
