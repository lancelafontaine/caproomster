from app import views, app
from app.core.user import User
from app.core.room import Room
from app.core.equipment import Equipment
from app.core.reservation import Reservation
from app.core.timeslot import Timeslot
from app.mapper import UserMapper
from app.mapper import RoomMapper
from app.mapper import ReservationMapper
from app.mapper import TimeslotMapper
from app.mapper import EquipmentMapper
from datetime import datetime
from flask import jsonify
import json


def test_invalid_login_no_userid():
    with app.app_context():
        with app.test_request_context():
            data = {
                'password': 'pass'
            }
            response = views.validate_login(data)
            assert (response.status_code == views.STATUS_CODE['UNPROCESSABLE'])


def test_invalid_login_no_pass():
    with app.app_context():
        with app.test_request_context():
            data = {
                'username': 'naan bread'
            }
            response = views.validate_login(data)
            assert (response.status_code == views.STATUS_CODE['UNPROCESSABLE'])


def test_invalid_login_userid_format():
    with app.app_context():
        with app.test_request_context():
            data = {
                'userId': 'not a digit',
                'password': 'test'
            }
            response = views.validate_login(data)
            assert (response.status_code == views.STATUS_CODE['UNPROCESSABLE'])


def test_invalid_login_nonexisting_user(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def user_not_found(_):
                return None

            monkeypatch.setattr(UserMapper, 'find', user_not_found)

            data = {
                'username': "iscapstone",
                'password': 'test'
            }
            response = views.validate_login(data)
            assert (response.status_code == views.STATUS_CODE['NOT_FOUND'])


def test_invalid_login_wrong_pass(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def user_found(_):
                return User('very', 'secret')

            monkeypatch.setattr(UserMapper, 'find', user_found)

            data = {
                'username': 'very',
                'password': 'wrong password'
            }
            response = views.validate_login(data)
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_valid_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def user_found(_):
                return User('mechanical', 'keyboard')

            monkeypatch.setattr(UserMapper, 'find', user_found)

            data = {
                'username': 'mechanical',
                'password': 'keyboard'
            }
            response = views.validate_login(data)
            assert (response.status_code == views.STATUS_CODE['OK'])


def test_is_not_logged_in():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            response = views.is_logged_in()
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_is_logged_in():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'loggedIn!'})
            response = views.is_logged_in()
            assert (response.status_code == views.STATUS_CODE['OK'])


def test_logout():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'potatoes'})
            assert ('logged_in' in views.session)
            assert (views.session['logged_in'] is True)
            assert ('username' in views.session)
            assert (views.session['username'] == 'potatoes')
            response = views.logout()
            assert (response.status_code == views.STATUS_CODE['OK'])
            assert ('logged_in' not in views.session)
            assert ('username' not in views.session)


def test_invalid_get_all_rooms_no_login():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            response = views.get_all_rooms()
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_valid_get_all_rooms_with_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def rooms_found():
                return [Room(1), Room(2), Room(3)]

            monkeypatch.setattr(RoomMapper, 'findAll', rooms_found)

            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'hamburger'})
            response = views.get_all_rooms()
            assert (response.status_code == views.STATUS_CODE['OK'])
            response_data = json.loads(response.get_data())
            assert (isinstance(response_data, dict))
            assert ('rooms' in response_data)
            assert (isinstance(response_data['rooms'], list))


def test_is_logged_in_bool_true():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'hummus'})
            assert (views.is_logged_in_bool() is True)


def test_is_logged_in_bool_false():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            assert (views.is_logged_in_bool() is False)


def test_unauthorized():
    with app.app_context():
        with app.test_request_context():
            assert (views.unauthorized().status_code is views.STATUS_CODE['UNAUTHORIZED'])


def test_make_new_reservation():
    with app.app_context():
        with app.test_request_context(method='POST'):
            assert (views.make_new_reservation() is not None)


def test_login_get():
    with app.app_context():
        with app.test_request_context():
            assert (views.login() is not None)


def test_login_post(monkeypatch):
    with app.app_context():
        with app.test_request_context(method='POST'):
            def mock_validate_login(_):
                return jsonify({'success': 'success'})

            monkeypatch.setattr(views, 'validate_login', mock_validate_login)
            assert (views.login() is not None)


def test_valid_validate_new_reservation(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'username': 'mr',
                'timeslot': {
                    'startTime': '14',
                    'endTime': '15',
                    'date': '3000/03/19'
                },
                'equipment': {
                    'laptop': 1,
                    'projector': 1,
                    'board': 1
                },
                'description': 'cool meeting'
            }

            def mock_user_find(_):
                return User('mr', 'pickles')

            def mock_room_find(_):
                return Room(1)

            def mock_reservation_done():
                return

            def mock_reservation_add(*args):
                time = Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID", "timeslotID")
                room = Room(1)

                user = User('mr', 'pickles')
                return Reservation(room, user, time, 'description', Equipment("EquipmentID"), "ReservationIDunique")

            def mock_timeslot_add(*args):
                return Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID", "timeslotID")

            def mock_equipment_add(*args):
                return Equipment('id', 1,1,1)

            def mock_reservation_find_all(*args):
                return []

            monkeypatch.setattr(UserMapper, 'find', mock_user_find)
            monkeypatch.setattr(RoomMapper, 'find', mock_room_find)
            monkeypatch.setattr(TimeslotMapper, 'makeNew', mock_timeslot_add)
            monkeypatch.setattr(TimeslotMapper, 'done', mock_reservation_done)
            monkeypatch.setattr(EquipmentMapper, 'makeNew', mock_equipment_add)
            monkeypatch.setattr(EquipmentMapper, 'done', mock_reservation_done)
            monkeypatch.setattr(ReservationMapper, 'done', mock_reservation_done)
            monkeypatch.setattr(ReservationMapper, 'makeNew', mock_reservation_add)
            monkeypatch.setattr(ReservationMapper, 'findAll', mock_reservation_find_all)
            assert (views.validate_new_reservation(data).status_code is views.STATUS_CODE['OK'])


def test_valid_validate_make_new_reservation_payload_format():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'username': 'mr',
                'timeslot': {
                    'startTime': '14',
                    'endTime': '15',
                    'date': '3000/03/19'
                },
                'equipment': {
                    'laptop': 1,
                    'projector': 1,
                    'board': 1
                },
                'description': 'cool meeting'
            }
            assert (views.validate_reservation_payload_format(data) is None)


def test_invalid_validate_make_new_reservation_payload_format_missing_key():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'username': 'mr',
                'timeslot': {
                    'startTime': '14',
                    'endTime': '15',
                    'date': '3000/03/19'
                },
                'equipment': {
                    'laptop': 1,
                    'projector': 1,
                    'board': 1
                }
            }
            assert (
                views.validate_reservation_payload_format(data).status_code is views.STATUS_CODE[
                    'UNPROCESSABLE'])


def test_invalid_validate_make_new_reservation_payload_format_not_digits():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'username': 'mr',
                'timeslot': {
                    'startTime': '14',
                    'endTime': '15',
                    'date': '3000/03/19'
                },
                'equipment': {
                    'laptop': 1,
                    'projector': 'haha',
                    'board': 1
                },
                'description': 'cool meeting'
            }
            assert (
            views.validate_reservation_payload_format(data).status_code is views.STATUS_CODE['UNPROCESSABLE'])


def test_valid_validate_make_new_reservation_times():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'username': 'mr',
                'timeslot': {
                    'startTime': '1',
                    'endTime': '2',
                    'date': '3000/03/19'
                },
                'equipment': {
                    'laptop': 1,
                    'projector': 1,
                    'board': 1
                },
                'description': 'cool meeting'
            }
            assert (views.validate_reservation_payload_format(data) is None)
            data['timeslot']['startTime'] = 23
            data['timeslot']['startTime'] = 1
            assert (views.validate_reservation_payload_format(data) is None)


def test_invalid_validate_make_new_reservation_times_no_24_hour_format():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'username': 'mr',
                'timeslot': {
                    'startTime': '1315432',
                    'endTime': '1',
                    'date': '3000/03/19'
                },
                'equipment': {
                    'laptop': 1,
                    'projector': 1,
                    'board': 1
                },
                'description': 'cool meeting'
            }
            assert (views.validate_reservation_payload_format(data).status_code is views.STATUS_CODE[
                'UNPROCESSABLE'])
            data['timeslot']['startTime'] = '1'
            data['timeslot']['startTime'] = '-12313'
            assert (views.validate_reservation_payload_format(data).status_code is views.STATUS_CODE[
                'UNPROCESSABLE'])


def test_invalid_validate_make_new_reservation_times_more_than_3_hours_long():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'username': 'mr',
                'timeslot': {
                    'startTime': '1',
                    'endTime': '23',
                    'date': '3000/03/19'
                },
                'equipment': {
                    'laptop': 1,
                    'projector': 1,
                    'board': 1
                },
                'description': 'cool meeting'
            }
            assert (views.validate_reservation_payload_format(data).status_code is views.STATUS_CODE[
                'UNPROCESSABLE'])
            data['timeslot']['startTime'] = '5'
            data['timeslot']['startTime'] = '1'
            assert (views.validate_reservation_payload_format(data).status_code is views.STATUS_CODE[
                'UNPROCESSABLE'])
            data['timeslot']['startTime'] = '23'
            data['timeslot']['startTime'] = '4'
            assert (views.validate_reservation_payload_format(data).status_code is views.STATUS_CODE[
                'UNPROCESSABLE'])


def test_valid_validate_make_new_reservation_date():
    with app.app_context():
        with app.test_request_context():
            dateList = ['2040', '04', '04']
            assert (views.validate_make_new_reservation_date(dateList) is None)
            dateList = ['2040', '4', '4']
            assert (views.validate_make_new_reservation_date(dateList) is None)


def test_invalid_validate_make_new_reservation_date_more_than_3_elems():
    with app.app_context():
        with app.test_request_context():
            dateList = ['2040', '04', '04', '04']
            assert (
                views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            dateList = ['2040', '04']
            assert (
                views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])


def test_invalid_validate_make_new_reservation_date_elem_is_not_digit():
    with app.app_context():
        with app.test_request_context():
            dateList = ['2040', '04', 'not a digit']
            assert (
                views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            dateList = ['2040', 'not a digit', '04']
            assert (
                views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            dateList = ['not a digit', '04', '04']
            assert (
                views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])


def test_invalid_validate_make_new_reservation_date_impossible_date():
    with app.app_context():
        with app.test_request_context():
            dateList = ['2040', '04', '90']
            assert (
                views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            dateList = ['2040', '49', '04']
            assert (
                views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])


def test_invalid_validate_make_new_reservation_date_before_current_date():
    with app.app_context():
        with app.test_request_context():
            dateList = ['1999', '04', '04']
            assert (
                views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])


def test_valid_make_new_reservation_room_user_exists(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            roomId = '1'
            username = 'brocolli'

            def mock_user_find(_):
                return User('glorious', 'carpet')

            def mock_room_find(_):
                return Room(1)

            monkeypatch.setattr(UserMapper, 'find', mock_user_find)
            monkeypatch.setattr(RoomMapper, 'find', mock_room_find)
            assert (views.validate_reservation_room_user_exists(roomId, username) is None)


def test_invalid_make_new_reservation_room_user_exists_user_missing(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            roomId = '1'
            username = 'ketchup'

            def mock_user_not_found(_):
                return

            def mock_room_find(_):
                return Room(1)

            monkeypatch.setattr(UserMapper, 'find', mock_user_not_found)
            monkeypatch.setattr(RoomMapper, 'find', mock_room_find)
            assert (
            views.validate_reservation_room_user_exists(roomId, username).status_code is views.STATUS_CODE[
                'NOT_FOUND'])


def test_invalid_make_new_reservation_room_user_exists_room_missing(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            roomId = '1'
            username = 'sandwich'

            def mock_user_find(_):
                return User('kwazy', 'kupkakes')

            def mock_room_not_found(_):
                return

            monkeypatch.setattr(RoomMapper, 'find', mock_room_not_found)
            monkeypatch.setattr(UserMapper, 'find', mock_user_find)
            assert (
            views.validate_reservation_room_user_exists(roomId, username).status_code is views.STATUS_CODE[
                'NOT_FOUND'])


def test_valid_make_new_reservation_timeslots_without_reservations():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            dateList = ['2040', '04', '04']
            startTime = 5
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert (result == False)


def test_valid_make_new_reservation_timeslots_with_reservations():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID_ujhbknl", "timeslotID_tycuvi")
            room = Room(1)

            user = User('mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', Equipment("equipmentID_Uviv"),
                                       "ReservationID_rtycvuvib")

            reservations.append(reservation1)

            dateList = ['2040', '04', '04']
            startTime = 5
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert (result == False)


def test_valid_make_new_reservation_timeslots_with_reservations_lower_bound():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_ytcuvib", "timeslotID_exrtcy")
            room = Room(1)

            user = User('mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', Equipment("equipmentID_trxcyv"),
                                       "reservationID_txcfyvuyb")

            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 3
            endTime = 5

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert (result == False)


def test_valid_make_new_reservation_timeslots_with_reservations_upper_bound():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            timeslot = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_txcyvu", "timeslotID_ezwrxt")
            room = Room(1)
            user = User('mr', 'pickles')
            reservation1 = Reservation(room, user, timeslot, 'description', Equipment("equipmentID_jkljh"),
                                       "reservationID_dsxfgc")
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 8
            endTime = 10

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert (result == False)


def test_invalid_make_new_reservation_timeslots_overlapping_time_1():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5, 7, datetime(2020, 01, 01), 1, "userID_gfhasdh", "timeslotID_fgchgvjbk")
            room = Room(1)

            user = User('mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', Equipment("equipmentID_fdxgch"),
                                       "reservationID_fdjhbk")
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 5
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert (result == True)


def test_invalid_make_new_reservation_timeslots_overlapping_time_2():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_fcghv", "timeslotID_fdxgch")
            room = Room(1)
            user = User('mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', Equipment("equipmentID_cghvjb"),
                                       "reservationID_ghvjbas")
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 6
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert (result == True)


def test_invalid_make_new_reservation_timeslots_overlapping_time_3():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_tcyvu", "timeslotID_fctygv")
            room = Room(1)

            user = User('mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', Equipment(1), 1)
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 4
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert (result == True)


def test_invalid_make_new_reservation_timeslots_overlapping_time_4():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5, 8, datetime(2020, 01, 01), 1, "userID_cghvjb", "timeslotID_hgvjbs")
            room = Room(1)
            user = User('mr', 'pickles')

            reservation1 = Reservation(room, user, time, 'description', Equipment("equipmentID_ghvjbk"),
                                       "reservationID_hvjbka")
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 6
            endTime = 9

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert (result == True)


def test_invalid_get_all_rooms_without_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def rooms_found():
                return [Room(1), Room(2), Room(3)]

            monkeypatch.setattr(RoomMapper, 'findAll', rooms_found)

            views.session.clear()
            response = views.get_all_rooms()
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_valid_get_all_rooms_with_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def rooms_found():
                return [Room(1), Room(2), Room(3)]

            monkeypatch.setattr(RoomMapper, 'findAll', rooms_found)

            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'banana'})
            response = views.get_all_rooms()
            assert (response.status_code == views.STATUS_CODE['OK'])
            response_data = json.loads(response.get_data())
            assert (isinstance(response_data, dict))
            assert ('rooms' in response_data)
            assert (isinstance(response_data['rooms'], list))


def test_invalid_make_new_reservation_without_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def empty_return():
                return

            def room_find(_):
                return Room(1)

            def user_find(_):
                return User('buddy', 'boy')

            def reservation_create(*args, **kwargs):
                room = Room(1)
                user = User('buddy', 'boy')
                time = Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID_tyvub", "timeslotID_ugvhbjk")
                return Reservation(room, user, time, 'description', Equipment("equipmentID_yvhjb"),
                                   "reservationID_vghjbk")

            def timeslot_create(_):
                return Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID_vhbj", "timeslotID_iubno")

                monkeypatch.setattr(TimeslotMapper, 'makeNew', empty_return)
                monkeypatch.setattr(ReservationMapper, 'makeNew', reservation_create)
                monkeypatch.setattr(TimeslotMapper, 'done', empty_return)
                monkeypatch.setattr(RoomMapper, 'find', room_find)
                monkeypatch.setattr(UserMapper, 'find', user_find)

                views.session.clear()
                response = views.make_new_reservation()
                assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_invalid_get_reservations_by_room_without_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            response = views.get_reservations_by_room()
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_valid_get_reservations_by_room_with_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def find_by_room(*args, **kwargs):
                room = Room(1)
                user = User('buddy', 'boy')
                time = Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID_ibun", "timeslotID_vuhbjk")
                return [Reservation(room, user, time, 'description', Equipment("equipmentID_vguhbikjn"),
                                    "reservationID_tcytvuhb")]

            monkeypatch.setattr(ReservationMapper, 'findByRoom', find_by_room)

            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'salt and pepper'})
            response = views.get_reservations_by_room("1")
            assert (response.status_code == views.STATUS_CODE['OK'])
            response_data = json.loads(response.get_data())
            assert (isinstance(response_data, dict))
            assert ('roomId' in response_data)
            assert ('reservations' in response_data)
            assert (isinstance(response_data['reservations'], list))
    assert ('waitings' in response_data)
    assert (isinstance(response_data['waitings'], list))


def test_invalid_get_reservations_by_user_without_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            response = views.get_reservations_by_user()
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_valid_get_reservations_by_user_with_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def find_by_user(*args, **kwargs):
                room = Room(1)
                user = User('buddy', 'boy')
                time = Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID_bijknklm", "timeslotID_ghvjbk")
                return [Reservation(room, user, time, 'description', Equipment("equipmentID_hgcvjb"),
                                    "reservationID_vuhbiuj")]

            monkeypatch.setattr(ReservationMapper, 'findByUser', find_by_user)

            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'marmelade'})
            response = views.get_reservations_by_user("1")
            assert (response.status_code == views.STATUS_CODE['OK'])
            response_data = json.loads(response.get_data())
            assert (isinstance(response_data, dict))
            assert ('reservations' in response_data)
            assert ('username' in response_data)
            assert (isinstance(response_data['reservations'], list))


def test_invalid_get_reservations_by_room_without_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            response = views.get_reservations_by_room()
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_valid_get_reservations_by_with_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def find_by_room(*args, **kwargs):
                room = Room(1)
                user = User('buddy', 'boy')
                time = Timeslot(1, 2, datetime(2020, 01, 01), 1, "userID_vubin", "timeslotID_hbijkn")
                return [Reservation(room, user, time, 'description', Equipment("equipmentID_uyvbin"),
                                    "reservationID_ygvuhjbk")]

            monkeypatch.setattr(ReservationMapper, 'findByRoom', find_by_room)

            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'tzatziki'})
            response = views.get_reservations_by_room("1")
            assert (response.status_code == views.STATUS_CODE['OK'])
            response_data = json.loads(response.get_data())
            assert (isinstance(response_data, dict))
            assert ('roomId' in response_data)
            assert ('reservations' in response_data)
            assert (isinstance(response_data['reservations'], list))
            assert ('waitings' in response_data)
            assert (isinstance(response_data['waitings'], list))


def test_invalid_get_all_reservations_no_login():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            response = views.get_all_reservations()
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_valid_get_all_reservations(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def reservations_found():
                room = Room(1)
                user = User('buddy', 'boy')
                time = Timeslot(1, 2, datetime(2020, 01, 01), 1, 'buddy', 'timeslotID_7g8hij')
                return [Reservation(room, user, time, 'description', Equipment("equipmentID_ionoi"),"reservationID")]

            monkeypatch.setattr(ReservationMapper, 'findAll', reservations_found)

            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'pasta'})
            response = views.get_all_reservations()
            assert (response.status_code == views.STATUS_CODE['OK'])
            response_data = json.loads(response.get_data())
            assert (isinstance(response_data, dict))
            assert ('reservations' in response_data)
            assert (isinstance(response_data['reservations'], list))


def test_invalid_delete_reservation_no_login():
    with app.app_context():
        with app.test_request_context(method='DELETE'):
            views.session.clear()
            response = views.delete_reservation('test')
            assert (response.status_code == views.STATUS_CODE['UNAUTHORIZED'])


def test_invalid_delete_reservation_wrong_id(monkeypatch):
    with app.app_context():
        with app.test_request_context(method='DELETE'):
            def reservation_not_found(_):
                return

            monkeypatch.setattr(ReservationMapper, 'find', reservation_not_found)

            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'pasta'})
            response = views.delete_reservation('test')
            assert (response.status_code == views.STATUS_CODE['NOT_FOUND'])


def test_valid_delete_reservation(monkeypatch):
    with app.app_context():
        with app.test_request_context(method='DELETE'):
            def reservation_not_found(_):
                room = Room(1)
                user = User('buddy', 'boy')
                time = Timeslot(1, 2, datetime(2020, 01, 01), '', 1, 1)
                equipment = Equipment("EquipmentID_iionask")
                return Reservation(room, user, time, 'description', equipment,'test')

            def empty_return(*args, **kwargs):
                return

            monkeypatch.setattr(ReservationMapper, 'find', reservation_not_found)
            monkeypatch.setattr(ReservationMapper, 'delete', empty_return)
            monkeypatch.setattr(ReservationMapper, 'done', empty_return)

            views.session.clear()
            views.session.update({'logged_in': True, 'username': 'pasta'})
            response = views.delete_reservation('test')
            assert (response.status_code == views.STATUS_CODE['OK'])
            response_data = json.loads(response.get_data())
            assert (isinstance(response_data, dict))
            assert ('reservationId' in response_data)
