from datetime import datetime
from app.core.timeslot import Timeslot

def test_valid_make_new_reservation_timeslots_with_reservations():
    time1 = Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
    time2 = Timeslot(4, 5, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
    result = time1.overlaps(time2)
    assert (result == False)


def test_valid_make_new_reservation_timeslots_with_reservations_lower_bound():
    time1 = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_ytcuvib", "timeslotID_exrtcy")
    time2 = Timeslot(4, 5, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
    result = time1.overlaps(time2)
    assert (result == False)


def test_valid_make_new_reservation_timeslots_with_reservations_upper_bound():
    time1= Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_txcyvu", "timeslotID_ezwrxt")
    time2 = Timeslot(8, 10, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
    result = time1.overlaps(time2)
    assert (result == False)


def test_invalid_make_new_reservation_timeslots_overlapping_time_1():
    time1 = Timeslot(5, 7, datetime(2020, 01, 01), 1, "userID_gfhasdh", "timeslotID_fgchgvjbk")
    time2 = Timeslot(5, 7, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
    result = time1.overlaps(time2)
    assert (result == True)


def test_invalid_make_new_reservation_timeslots_overlapping_time_2():
    time1 = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_fcghv", "timeslotID_fdxgch")
    time2 = Timeslot(6, 7, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
    result = time1.overlaps(time2)
    assert (result == True)


def test_invalid_make_new_reservation_timeslots_overlapping_time_3():
    time1 = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_tcyvu", "timeslotID_fctygv")
    time2 = Timeslot(4, 7, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
    result = time1.overlaps(time2)
    assert (result == True)


def test_invalid_make_new_reservation_timeslots_overlapping_time_4():
    time1 = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_cghvjb", "timeslotID_hgvjbs")
    time2 = Timeslot(6, 9, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
    result = time1.overlaps(time2)
    assert (result == True)


