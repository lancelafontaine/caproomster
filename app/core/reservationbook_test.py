# noinspection PyUnresolvedReferences
import pytest
from app.mapper import UnitOfWork
from app.mapper import WaitingMapper
from app.core.reservationbook import ReservationBook
from app.core.room import Room
from app.core.timeslot import Timeslot
from app.core.user import User
from app.mapper import ReservationMapper
from app.mapper import TimeslotMapper
from app.core.equipment import Equipment
from collections import deque

from datetime import datetime


def test_timeslot_is_available_for_reservation(monkeypatch):
    # initialization
    reservationbook = ReservationBook(deque(), deque(), deque())
    room = Room(3)
    user1 = User("mary", "passw")
    user2 = User("john", "pass", True)
    description = "Both John and Mary want the room."
    equipment1 = Equipment("equipmentID_uvybinom")
    equipment2 = Equipment("equipmentID_ubhijnmm")

    timeslot1 = Timeslot(13, 15, datetime(2017, 04, 01), 2, "mary", "timeslotID_oinoin_Mary")
    timeslot2 = Timeslot(13, 15, datetime(2017, 04, 01), 2, "mary", "timeslotID_ububin_John")

    # mock
    def mockUOW_registernew(_):
        pass

    def mockReservationMapperDone():
        pass

    monkeypatch.setattr(UnitOfWork, 'registerNew', mockUOW_registernew)
    monkeypatch.setattr(ReservationMapper, 'done', mockReservationMapperDone)

    # verify
    assert reservationbook.isTimeslotAvailableforRoom(room, timeslot2)

    # execute
    reservationbook.makeReservation(room, user1, timeslot1, description, equipment1)

    # verify that the timeslot is no longer available
    assert not reservationbook.isTimeslotAvailableforRoom(room, timeslot2)


def test_cancel_reservation(monkeypatch):
    # initialization
    reservationbook = ReservationBook(deque(), deque(), deque())
    room = Room(3)
    user1 = User("mary", "passw")
    user2 = User("john", "pass", True)
    description = "Both John and Mary want the room."
    equipment1 = Equipment("equipmentID_uvybinom")
    equipment2 = Equipment("equipmentID_ubhijnmm")

    timeslot1 = Timeslot(13, 15, datetime(2017, 04, 01), 2, "mary", "timeslotID_oinoin_Mary")
    timeslot2 = Timeslot(13, 15, datetime(2017, 04, 01), 2, "mary", "timeslotID_ububin_John")

    # mock
    def mockUOW_registernew(_):
        pass

    def mockReservationMapperDone():
        pass

    monkeypatch.setattr(UnitOfWork, 'registerNew', mockUOW_registernew)
    monkeypatch.setattr(ReservationMapper, 'done', mockReservationMapperDone)

    # verify
    assert reservationbook.isTimeslotAvailableforRoom(room, timeslot2)

    # execute
    reservationbook.makeReservation(room, user1, timeslot1, description, equipment1)

    # verify that the timeslot is no longer available
    assert not reservationbook.isTimeslotAvailableforRoom(room, timeslot2)

    reservationID = reservationbook.getReservationList()[0].getId()
    reservationbook.cancel(reservationID)

    assert len(reservationbook.getReservationList()) == 0
    assert reservationbook.isTimeslotAvailableforRoom(room, timeslot2)


"""Tests whether students get added to the appropriate waitlist based on capstone flag"""


def test_add_to_appropriate_waiting_list(monkeypatch):
    # Initialization
    reservationBook = ReservationBook([], [], [])

    # mock
    def mockUOW_registernew(_):
        pass

    def mockWaitingMapperDone():
        pass

    monkeypatch.setattr(UnitOfWork, 'registerNew', mockUOW_registernew)
    monkeypatch.setattr(WaitingMapper, 'done', mockWaitingMapperDone)

    # check the size of the waitlist for capstone
    assert len(reservationBook.waitingListCapstone) == 0

    # check the size of the waitlist for regular
    assert len(reservationBook.waitingListRegular) == 0

    # execute
    reservationBook.addToWaitingList(2, User('usrname1', 'pass', True),
                                     Timeslot(11, 13, '2017-03-25', 2, "usrname1", "timeslotID_ibuon"), 'desc',
                                     Equipment("equipmentID_ghvjbk"))
    # verify
    assert len(reservationBook.waitingListCapstone) == 1

    # execute
    reservationBook.addToWaitingList(2, User('usrname2', 'pass', False),
                                     Timeslot(11, 13, '2017-03-25', 2, "usrname2", "timeslotID_hjbkn"), 'desc',
                                     Equipment("equipmentID_asdda"))
    # verify
    assert len(reservationBook.waitingListRegular) == 1

    # execute
    reservationBook.addToWaitingList(2, User('usrname3', 'pass', False),
                                     Timeslot(11, 13, '2017-03-25', 2, "usrname3", "timeslotID_hasda"), 'desc',
                                     Equipment("equipmentID_asdas"))

    # verify
    assert len(reservationBook.waitingListRegular) == 2


def test_update_waiting(monkeypatch):
    # Initialization
    reservationBook = ReservationBook([], [], [])

    # mock
    def mockUOW_registernew(_):
        pass

    def mockWaitingMapperDone():
        pass

    monkeypatch.setattr(UnitOfWork, 'registerNew', mockUOW_registernew)
    monkeypatch.setattr(WaitingMapper, 'done', mockWaitingMapperDone)

    """Populating the list with 2 regular students,
    1 capstone student all in room 5, in that order.
    This was already tested in test_add_to_appropriate_waiting_list()"""
    # putting regular student into waitlist at room 5
    reservationBook.addToWaitingList(5, User('mary', 'pass', False),
                                     Timeslot(11, 13, '2017-03-25', 2, "mary", "timeslotID_iubuasbd"), 'desc',
                                     Equipment("equipmentID_xbcxbc"))

    # putting regular student into waitlist at room 5
    reservationBook.addToWaitingList(5, User('john', 'pass', False),
                                     Timeslot(11, 13, '2017-03-25', 2, "john", "timeslotID_asfafa"), 'desc',
                                     Equipment("equipmentID_anranra"))

    # putting regular student into waitlist at room 5
    reservationBook.addToWaitingList(5, User('gary', 'pass', False),
                                     Timeslot(11, 13, '2017-03-25', 2, "gary", "timeslotID_sngfssn"), 'desc',
                                     Equipment("equipmentID_xnfsgn"))

    # putting capstone student into waitlist at room 5
    reservationBook.addToWaitingList(5, User('emir', 'pass', True),
                                     Timeslot(11, 13, '2017-03-25', 2, "emir", "timeslotID_bafdbd"), 'desc',
                                     Equipment("equipmentID_asfaf"))

    # putting regular student into waitlist at room 5
    reservationBook.addToWaitingList(5, User('cody', 'pass'),
                                     Timeslot(11, 13, '2017-03-25', 2, "cody", "timeslotID_asdsdfffa"), 'desc',
                                     Equipment("equipmentID_avbeerf"))

    # putting capstone student into waitlist at room 5
    reservationBook.addToWaitingList(5, User('mark', 'pass', True),
                                     Timeslot(11, 13, '2017-03-25', 2, "mark", "timeslotID_basfaf"), 'desc',
                                     Equipment("equipmentID_aghtrhr"))

    assert len(reservationBook.waitingListRegular) == 4
    assert len(reservationBook.waitingListCapstone) == 2
    assert len(reservationBook.reservationList) == 0

    # Execute
    reservationBook.updateWaiting(5)

    """The user with the highest priority has been popped out of the whole waitlist."""
    # Verify
    assert len(reservationBook.waitingListRegular) == 4
    assert len(reservationBook.waitingListCapstone) == 1
    assert len(reservationBook.reservationList) == 1

    """Making sure the user is the first capstone student at the top of the list"""
    assert reservationBook.reservationList[0].getUser().getId() == 'emir'

    """Calling update again, this should not change the waitlists since """
    # Execute
    reservationBook.updateWaiting(5)
    assert len(reservationBook.waitingListRegular) == 4
    assert len(reservationBook.waitingListCapstone) == 1
    assert len(reservationBook.reservationList) == 1

    """Calling update again, this should not change the waitlists since """
    # Execute
    reservationBook.updateWaiting(5)
    assert len(reservationBook.waitingListRegular) == 4
    assert len(reservationBook.waitingListCapstone) == 1
    assert len(reservationBook.reservationList) == 1

    """"Toying around with update, clearing the reservationlist, this can be done with a method"""
    reservationBook.reservationList = []
    assert len(reservationBook.waitingListRegular) == 4
    assert len(reservationBook.waitingListCapstone) == 1
    assert len(reservationBook.reservationList) == 0

    reservationBook.updateWaiting(5)
    assert len(reservationBook.waitingListRegular) == 4
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 1

    """Making sure that the user in the reservation list is Mark"""
    assert reservationBook.reservationList[0].getUser().getId() == "mark"

    """"Toying around with update, clearing the reservationlist, this can be done with a method"""
    reservationBook.reservationList = []
    assert len(reservationBook.waitingListRegular) == 4
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 0

    reservationBook.updateWaiting(5)
    assert len(reservationBook.waitingListRegular) == 3
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 1

    """Making sure that the user in the reservation list is Mary"""
    assert reservationBook.reservationList[0].getUser().getId() == "mary"

    """"Toying around with update, clearing the reservationlist, this can be done with a method"""
    reservationBook.reservationList = []
    assert len(reservationBook.waitingListRegular) == 3
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 0

    reservationBook.updateWaiting(5)
    assert len(reservationBook.waitingListRegular) == 2
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 1

    """Making sure that the user in the reservation list is John"""
    assert reservationBook.reservationList[0].getUser().getId() == "john"

    """"Toying around with update, clearing the reservationlist, this can be done with a method"""
    reservationBook.reservationList = []
    assert len(reservationBook.waitingListRegular) == 2
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 0

    reservationBook.updateWaiting(5)
    assert len(reservationBook.waitingListRegular) == 1
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 1

    """Making sure that the user in the reservation list is Gary"""
    assert reservationBook.reservationList[0].getUser().getId() == "gary"

    """"Toying around with update, clearing the reservationlist, this can be done with a method"""
    reservationBook.reservationList = []
    assert len(reservationBook.waitingListRegular) == 1
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 0

    reservationBook.updateWaiting(5)
    assert len(reservationBook.waitingListRegular) == 0
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 1

    """Making sure that the user in the reservation list is Cody"""
    assert reservationBook.reservationList[0].getUser().getId() == "cody"

    """At this point the list is empty, both regular and capstone"""
    """"Toying around with update, clearing the reservationlist, this can be done with a method"""
    reservationBook.reservationList = []
    assert len(reservationBook.waitingListRegular) == 0
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 0

    reservationBook.updateWaiting(5)
    assert len(reservationBook.waitingListRegular) == 0
    assert len(reservationBook.waitingListCapstone) == 0
    assert len(reservationBook.reservationList) == 0

    """Since both waitlists are empty, reservation remains empty upon update"""
    assert reservationBook.reservationList == []


def test_reservation_repeat(monkeypatch):
    # Initialization
    reservationBook = ReservationBook([], [], [])

    # Test Data
    start_time = 9
    end_time = 10
    room_id = 2
    block = 0
    date = '2016-04-20'
    user_id = "username"
    processed_description = ""
    user = User(user_id, "password")
    room = Room(room_id)
    time_slot = Timeslot(start_time, end_time, date, block, user_id, 'timeslotID_yctvubkjas')
    repeat_amount = 2

    # Expected result
    expected_amount_of_reservation = repeat_amount + 1  # + 1 because 0 repeat_amount will still make 1 reservation

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
    reservationBook.makeRepeatedReservation(room, user, time_slot, processed_description,
                                            Equipment("equipmentID_ytcuvibon"), repeat_amount)

    # Verify
    assert len(reservationBook.getReservationList()) == expected_amount_of_reservation


def test_find_total_reserved_time_for_user_for_a_given_week(monkeypatch):
    expected_total_hours = 9

    # Initialization
    reservationBook = ReservationBook([], [], [])

    rows = 3
    columns = 5

    # Mock
    def get_Timeslots(_):
        timeslot_list = [[0 for x in range(columns)] for y in range(rows)]
        date1 = datetime(2017, 3, 23)

        timeslot_list[0][0] = (9)  # start time
        timeslot_list[0][1] = (11)  # end time
        timeslot_list[0][2] = (0)  # id
        timeslot_list[0][3] = (date1)  # date
        timeslot_list[0][4] = (2)  # block

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

    monkeypatch.setattr(TimeslotMapper, 'find_all_timeslots_for_user', get_Timeslots)

    # Execute
    result = reservationBook.find_total_reserved_time_for_user_for_a_given_week(1, '2017-03-25')

    # Verify
    assert result == expected_total_hours
