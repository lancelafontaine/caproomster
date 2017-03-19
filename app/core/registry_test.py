import pytest
from app.core.registry import Registry
from app.core.reservationbook import ReservationBook
from app.core.room import Room
from app.core.timeslot import Timeslot
from app.mapper import ReservationMapper
from app.mapper import TimeslotMapper
from app.mapper import UserMapper


def test_valid_registry_init():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    registry = Registry(reservationBook)

    assert(type(registry.reservationBook.reservationList) is list)
    assert(type(registry.reservationBook.waitingList) is list)

def test_invalid_registry_init():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    registry = Registry(reservationBook)

    with pytest.raises(AttributeError) as e:
        registry.fakeAttributeDoesntExist

def test_reservation_repeat():

    # test data
    start_time = 9
    end_time = 10
    room_id = 2
    block = 0
    date = '2016-04-20'
    user_id = 1
    processed_description = ""
    user = UserMapper.find(user_id)
    room = Room(room_id, False)
    timeSlot = Timeslot(start_time, end_time, date, block, user.getId())
    repeat_amount = 2

    # Execute
    ReservationMapper.makeNewReservation(room, user, timeSlot, processed_description, repeat_amount)

    # Verify
    assert len(ReservationMapper.find_time_slot_ids(user_id)) == repeat_amount + 1
    assert len(TimeslotMapper.find_all_timeslots_for_user(user_id)) == repeat_amount + 1

