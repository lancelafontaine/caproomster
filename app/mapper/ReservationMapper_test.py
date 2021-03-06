from app.mapper import ReservationMapper
from app.mapper import TimeslotMapper
from app.mapper import RoomMapper
from app.mapper import IdMap
from app.core.reservation import Reservation
from app.core.user import User
from app.core.timeslot import Timeslot
from app.core.room import Room
from app.core.equipment import Equipment
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
    val = ReservationMapper.find("rtcyvu")

    # Verify
    assert(val is None)


def test_find_not_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    expected_timeslot = Timeslot(1, 2, 'date', 1, 'usernameid','timeid')
    expected_room = Room(1)
    expected = Reservation(expected_room, User('name', 'password'), expected_timeslot, 'description', Equipment("3w4ex5rcy"), "reservationID####")

    # Mock
    def no_find(_, __):
        return

    def yes_find(_):
        return [[expected.getId(), expected_room.getId(), expected.getDescription(), expected.getUser().getId(), expected.getEquipment().getId(), expected_timeslot.getId()]]

    def timeslot_find(_):
        return expected_timeslot

    def room_find(_):
        return expected_room

    monkeypatch.setattr(IdMap, 'find', no_find)
    monkeypatch.setattr(ReservationTDG, 'find', yes_find)
    monkeypatch.setattr(TimeslotMapper, 'find', timeslot_find)
    monkeypatch.setattr(RoomMapper, 'find', room_find)

    # Execute
    val = ReservationMapper.find("trcyv")

    # Verify
    assert(val.getRoom().getId() is expected_room.getId())
    assert(val.getDescription() is expected.getDescription())
    assert(val.getTimeslot().getId() is expected_timeslot.getId())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_not_found_in_DB(monkeypatch):
    # Test Data
    expected = Reservation('room', User('name', 'password'), 'time', 'description',Equipment("dxhtcfjygv"), 1)


    # Mock
    def id_find(_, __):
        return expected

    def no_find(_):
        return

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(ReservationTDG, 'find', no_find)

    # Execute
    val = ReservationMapper.find("vuybi")

    # Verify
    assert(val.getRoom() is expected.getRoom())
    assert(val.getDescription() is expected.getDescription())
    assert(val.getTimeslot() is expected.getTimeslot())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    unexpected = Reservation('room', User('name', 'password'), 'time', 'description', Equipment("trcyvu"), 1)
    expected = Reservation('room1', User('name2', 'password3'), 'time1', 'description2', Equipment("fgvkgas"), 2)

    # Mock
    def id_find(_, __):
        return expected

    def tdg_find(_):
        return [[unexpected.getId(), unexpected.getRoom()]]

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(ReservationTDG, 'find', tdg_find)

    # Execute
    val = ReservationMapper.find("tvyub")

    # Verify
    assert(val.getRoom() is expected.getRoom())
    assert(val.getDescription() is expected.getDescription())
    assert(val.getTimeslot() is expected.getTimeslot())
    assert(val.getId() is expected.getId())
