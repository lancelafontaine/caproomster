import pytest
from app.core.reservationbook import ReservationBook
from app.core.room import Room
from app.core.timeslot import Timeslot
from app.core.user import User
from app.mapper import ReservationMapper
from app.mapper import TimeslotMapper


def test_reservation_repeat(monkeypatch):
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    # Test Data
    start_time = 9
    end_time = 10
    room_id = 2
    block = 0
    date = '2016-04-20'
    user_id = 1
    processed_description = ""
    user = User(user_id, "", "")
    room = Room(room_id, False)
    time_slot = Timeslot(start_time, end_time, date, block, user_id)
    repeat_amount = 2

    # Mock
    def TimeslotMapper_makeNew(a, b, c, d, e):
        return time_slot

    def ignore1(_):
        return

    def ignore2(_, __):
        return

    def timeslot_id(_):
        return 1

    monkeypatch.setattr(Timeslot, 'setId', ignore2)
    monkeypatch.setattr(TimeslotMapper, 'makeNew', TimeslotMapper_makeNew)
    monkeypatch.setattr(TimeslotMapper, 'save', ignore1)
    monkeypatch.setattr(TimeslotMapper, 'findId', timeslot_id)
    monkeypatch.setattr(ReservationMapper, 'save', ignore1)

    # Execute
    reservationBook.makeNewReservation(room, user, time_slot, processed_description, repeat_amount)

    # Verify
    assert len(reservationBook.getReservationList()) == repeat_amount + 1
