from app.core.reservationbook import ReservationBook
from app.core.room import Room
from app.core.timeslot import Timeslot
from app.core.user import User
from app.mapper import ReservationMapper
from app.mapper import TimeslotMapper
from datetime import datetime


def test_reservation_repeat(monkeypatch):
    # Initialization
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

    # Expected result
    expected_amount_of_reservation = repeat_amount + 1 # + 1 because 0 repeat_amount will still make 1 reservation

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
    reservationBook.makeRepeatedReservation(room, user, time_slot, processed_description, repeat_amount)

    # Verify
    assert len(reservationBook.getReservationList()) == expected_amount_of_reservation

def test_find_total_reserved_time_for_user_for_a_given_week(monkeypatch):
    expected_total_hours = 9

    # Initialization
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    rows = 3
    columns = 5

    #Mock
    def get_Timeslots(_):
        timeslot_list = [[0 for x in range(columns)] for y in range(rows)]
        date1 = datetime(2017, 3, 23)

        timeslot_list[0][0] = (9)           #start time
        timeslot_list[0][1] = (11)          #end time
        timeslot_list[0][2] = (0)           #id
        timeslot_list[0][3] = (date1)       #date
        timeslot_list[0][4] = (2)           #block

        timeslot_list[1][0] = (9)
        timeslot_list[1][1] = (10)
        timeslot_list[1][2] = (0)
        timeslot_list[1][3] = (date1)
        timeslot_list[1][4] = (1)

        timeslot_list[2][0] = (9)
        timeslot_list[2][1] = (15)
        timeslot_list[2][2] = (0)
        timeslot_list[2][3] = (date1)
        timeslot_list[2][4] = (6)
        return timeslot_list

    monkeypatch.setattr(TimeslotMapper,'find_all_timeslots_for_user',get_Timeslots)

    # Execute
    result = reservationBook.find_total_reserved_time_for_user_for_a_given_week(1,'2017-03-25')

    # Verify
    assert result == expected_total_hours
