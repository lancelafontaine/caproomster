from app.mapper import WaitingMapper
from app.mapper import TimeslotMapper
from app.mapper import UserMapper
from app.mapper import RoomMapper
from app.mapper import IdMap
from app.core.waiting import Waiting
from app.core.room import Room
from app.core.equipment import Equipment
from app.core.user import User
from app.core.timeslot import Timeslot
from app.TDG import WaitingTDG


def teardown_module(module):
    IdMap.clear(Waiting)


def test_find_not_found_in_id_map_not_found_in_DB(monkeypatch):
    # Mock
    def no_find(_):
        return
    def no_find2(_, __):
        return
    monkeypatch.setattr(IdMap, 'find', no_find2)
    monkeypatch.setattr(WaitingTDG, 'find', no_find)

    # Execute
    val = WaitingMapper.find(1)

    # Verify
    assert(val is None)


def test_find_not_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    expected_timeslot = Timeslot(1, 2, 'date', 1, 'usernameid','timeid')
    expected_room = Room(1)
    expected_user = User('abe',3)
    expected_equipment = Equipment("equipmentID_uvibonpm")
    expected = Waiting(expected_room, expected_user, expected_timeslot, 'joe',expected_equipment,234)

    # Mock
    def no_find(_, __):
        return

    def yes_find(_):
        return [[expected.getId(), expected.getRoom(), expected.getUser(), expected.getDescription(), expected_equipment.getId(), expected.getTimeslot().getId()]]

    def timeslot_find(_):
        return expected_timeslot
    def room_find(_):
        return expected_room
    def user_find(_):
        return expected_user

    monkeypatch.setattr(IdMap, 'find', no_find)
    monkeypatch.setattr(WaitingTDG, 'find', yes_find)
    monkeypatch.setattr(TimeslotMapper, 'find', timeslot_find)
    monkeypatch.setattr(RoomMapper, 'find', room_find)
    monkeypatch.setattr(UserMapper, 'find', user_find)

    # Execute
    val = WaitingMapper.find("iyubon")

    # Verify
    assert(val.getTimeslot() is expected_timeslot)
    assert(val.getRoom() is expected_room)
    assert(val.getUser() is expected_user)
    assert(val.getDescription() is expected.getDescription())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_not_found_in_DB(monkeypatch):
    # Test Data
    expected = Waiting("room", User("mammad","password"), Timeslot(1,2,"date",1,"mammad","timeID_ibuon"), 'description',Equipment('equipment'), "waitingID_vubion")

    # Mock
    def id_find(_, __):
        return expected

    def no_find(_):
        return

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(WaitingTDG, 'find', no_find)

    # Execute
    val = WaitingMapper.find("waitingID_vubion")

    # Verify
    assert(val.getTimeslot() is expected.getTimeslot())
    assert(val.getRoom() is expected.getRoom())
    assert(val.getUser() is expected.getUser())
    assert(val.getDescription() is expected.getDescription())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    unexpected = Waiting('room', User('name', 'password'), 'time', 'description', Equipment("trcyvu"), 1)
    expected = Waiting('room1', User('name2', 'password3'), 'time1', 'description2', Equipment("fgvkgas"), 2)

    # Mock
    def id_find(_, __):
        return expected

    def tdg_find(_):
        return [[unexpected.getId(), unexpected.getRoom(), unexpected.getUser(), unexpected.getDescription(), unexpected.getTimeslot()]]

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(WaitingTDG, 'find', tdg_find)

    # Execute
    val = WaitingMapper.find(1)

    # Verify
    assert(val.getTimeslot() is expected.getTimeslot())
    assert(val.getRoom() is expected.getRoom())
    assert(val.getUser() is expected.getUser())
    assert(val.getDescription() is expected.getDescription())
    assert(val.getId() is expected.getId())
