from app import views, app
from app.core.user import User
from app.core.room import Room
from app.core.reservation import Reservation
from app.core.timeslot import Timeslot
from app.mapper import UserMapper
from app.mapper import RoomMapper
from app.mapper import ReservationMapper
from flask import request, jsonify
import json

def test_invalid_login_no_userid():
    with app.app_context():
        with app.test_request_context():
            data = {
                'password': 'pass'
            }
            response = views.validate_login(data)
            assert(response.status_code == views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_login_no_pass():
    with app.app_context():
        with app.test_request_context():
            data = {
                'userId': 1
            }
            response = views.validate_login(data)
            assert(response.status_code == views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_login_userid_format():
    with app.app_context():
        with app.test_request_context():
            data = {
                'userId': 'not a digit',
                'password': 'test'
            }
            response = views.validate_login(data)
            assert(response.status_code == views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_login_nonexisting_user(monkeypatch):
    with app.app_context():
        with app.test_request_context():

            def user_not_found(_):
                return None
            monkeypatch.setattr(UserMapper, 'find', user_not_found)

            data = {
                'userId': 1,
                'password': 'test'
            }
            response = views.validate_login(data)
            assert(response.status_code == views.STATUS_CODE['NOT_FOUND'])

def test_invalid_login_wrong_pass(monkeypatch):
    with app.app_context():
        with app.test_request_context():

            def user_found(_):
                return User(1, 'buddy', 'boy')
            monkeypatch.setattr(UserMapper, 'find', user_found)

            data = {
                'userId': 1,
                'password': 'wrong password'
            }
            response = views.validate_login(data)
            assert(response.status_code == views.STATUS_CODE['UNAUTHORIZED'])

def test_valid_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():

            def user_found(_):
                return User(1, 'mechanical', 'keyboard')
            monkeypatch.setattr(UserMapper, 'find', user_found)

            data = {
                'userId': 1,
                'password': 'keyboard'
            }
            response = views.validate_login(data)
            assert(response.status_code == views.STATUS_CODE['OK'])

def test_is_not_logged_in():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            response = views.is_logged_in()
            assert(response.status_code == views.STATUS_CODE['UNAUTHORIZED'])

def test_is_logged_in():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            views.session.update({'logged_in': True, 'userId': 1})
            response = views.is_logged_in()
            assert(response.status_code == views.STATUS_CODE['OK'])

def test_logout():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            views.session.update({'logged_in': True, 'userId': 1})
            assert('logged_in' in views.session)
            assert(views.session['logged_in'] == True)
            assert('userId' in views.session)
            assert(views.session['userId'] == 1)
            response = views.logout()
            assert(response.status_code == views.STATUS_CODE['OK'])
            assert('logged_in' not in views.session)
            assert('userId' not in views.session)

def test_invalid_get_all_rooms_no_login():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            response = views.get_all_rooms()
            assert(response.status_code == views.STATUS_CODE['UNAUTHORIZED'])

def test_valid_get_all_rooms_with_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def rooms_found():
                return [Room(1, False), Room(2, False), Room(3, False)]
            monkeypatch.setattr(RoomMapper, 'findAll', rooms_found)

            views.session.clear()
            views.session.update({'logged_in': True, 'userId': 1})
            response = views.get_all_rooms()
            assert(response.status_code == views.STATUS_CODE['OK'])
            response_data = json.loads(response.get_data())
            assert(isinstance(response_data, dict))
            assert('rooms' in response_data)
            assert(isinstance(response_data['rooms'], list))

def test_is_logged_in_bool_true():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            views.session.update({'logged_in': True, 'userId': 1})
            assert(views.is_logged_in_bool() is True)

def test_is_logged_in_bool_false():
    with app.app_context():
        with app.test_request_context():
            views.session.clear()
            assert(views.is_logged_in_bool() is False)

def test_unauthorized():
    with app.app_context():
        with app.test_request_context():
            assert(views.unauthorized().status_code is views.STATUS_CODE['UNAUTHORIZED'])

def test_make_new_reservation():
    with app.app_context():
        with app.test_request_context(method='POST'):
            assert(views.make_new_reservation() is not None)

def test_login_get():
    with app.app_context():
        with app.test_request_context():
            assert(views.login() is not None)

def test_login_post(monkeypatch):
    with app.app_context():
        with app.test_request_context(method='POST'):
            def mock_validate_login(_):
                return jsonify({'success':'success'})
            monkeypatch.setattr(views, 'validate_login', mock_validate_login)
            assert(views.login() is not None)

def test_valid_validate_new_reservation(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'userId': '1',
                'timeslot': {
                    'startTime': '14',
                    'endTime': '15',
                    'date': '3000-03-19'
                },
                'description': 'cool meeting'
            }
            def mock_user_find(_):
                return User(1, 'mr', 'pickles')
            def mock_room_find(_):
                return Room(1, False)
            def mock_reservation_done():
                return
            def mock_reservation_add(*args):
                time = Timeslot(1,2,'2020-01-01', '', 1)
                room = Room(1, False)
                user = User(1, 'mr', 'pickles')
                return Reservation(room, user, time, 'description', 1)
            def mock_reservation_find_all(*args):
                return []

            monkeypatch.setattr(UserMapper, 'find', mock_user_find)
            monkeypatch.setattr(RoomMapper, 'find', mock_room_find)
            monkeypatch.setattr(ReservationMapper, 'done', mock_reservation_done)
            monkeypatch.setattr(ReservationMapper, 'makeNew', mock_reservation_add)
            monkeypatch.setattr(ReservationMapper, 'findAll', mock_reservation_find_all)
            assert(views.validate_new_reservation(data).status_code is views.STATUS_CODE['OK'])

def test_valid_validate_make_new_reservation_payload_format():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'userId': '1',
                'timeslot': {
                    'startTime': '14',
                    'endTime': '15',
                    'date': '3000-03-19'
                },
                'description': 'cool meeting'
            }
            assert(views.validate_make_new_reservation_payload_format(data) is None)

def test_invalid_validate_make_new_reservation_payload_format_missing_key():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'userId': '1',
                'timeslot': {
                    'startTime': '14',
                    'endTime': '15',
                    'date': '3000-03-19'
                }
            }
            assert(views.validate_make_new_reservation_payload_format(data).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_validate_make_new_reservation_payload_format_missing_timeslot_key():
    with app.app_context():
        with app.test_request_context():
            data = {
                'roomId': '1',
                'userId': '1',
                'timeslot': {
                    'startTime': '14',
                    'endTime': '15'
                },
                'description': 'best workout'
            }
            assert(views.validate_make_new_reservation_payload_format(data).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_validate_make_new_reservation_payload_format_not_digits():
    with app.app_context():
        with app.test_request_context():
            data = {
            'roomId': '1',
            'userId': '1',
            'timeslot': {
                'startTime': 'not a digit',
                'endTime': '15',
                'date': '3000-03-19'
            },
            'description': 'cool meeting'
            }
            assert(views.validate_make_new_reservation_payload_format(data).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_valid_validate_make_new_reservation_times():
    with app.app_context():
        with app.test_request_context():
            startTime = 1
            endTime = 2
            assert(views.validate_make_new_reservation_times(startTime, endTime) is None)
            startTime = 23
            endTime = 1
            assert(views.validate_make_new_reservation_times(startTime, endTime) is None)

def test_invalid_validate_make_new_reservation_times_no_24_hour_format():
    with app.app_context():
        with app.test_request_context():
            startTime = 13456
            endTime = 1
            assert(views.validate_make_new_reservation_times(startTime, endTime).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            startTime = 1
            endTime = -12313
            assert(views.validate_make_new_reservation_times(startTime, endTime).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_validate_make_new_reservation_times_more_than_3_hours_long():
    with app.app_context():
        with app.test_request_context():
            startTime = 1
            endTime = 23
            assert(views.validate_make_new_reservation_times(startTime, endTime).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            startTime = 5
            endTime = 1
            assert(views.validate_make_new_reservation_times(startTime, endTime).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            startTime = 23
            endTime = 4
            assert(views.validate_make_new_reservation_times(startTime, endTime).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_valid_validate_make_new_reservation_date():
    with app.app_context():
        with app.test_request_context():
            dateList = ['2040', '04', '04']
            assert(views.validate_make_new_reservation_date(dateList) is None)
            dateList = ['2040', '4', '4']
            assert(views.validate_make_new_reservation_date(dateList) is None)

def test_invalid_validate_make_new_reservation_date_more_than_3_elems():
    with app.app_context():
        with app.test_request_context():
            dateList = ['2040', '04', '04', '04']
            assert(views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            dateList = ['2040', '04']
            assert(views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_validate_make_new_reservation_date_elem_is_not_digit():
    with app.app_context():
        with app.test_request_context():
            dateList = ['2040', '04', 'not a digit']
            assert(views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            dateList = ['2040', 'not a digit', '04']
            assert(views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            dateList = ['not a digit', '04', '04']
            assert(views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_validate_make_new_reservation_date_impossible_date():
    with app.app_context():
        with app.test_request_context():
            dateList = ['2040', '04', '90']
            assert(views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])
            dateList = ['2040', '49', '04']
            assert(views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_validate_make_new_reservation_date_before_current_date():
    with app.app_context():
        with app.test_request_context():
            dateList = ['1999', '04', '04']
            assert(views.validate_make_new_reservation_date(dateList).status_code is views.STATUS_CODE['UNPROCESSABLE'])

def test_valid_make_new_reservation_room_user_exists(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            roomId = '1'
            userId = '5'
            def mock_user_find(_):
                return User(5, 'glorious', 'carpet')
            def mock_room_find(_):
                return Room(1, False)
            monkeypatch.setattr(UserMapper, 'find', mock_user_find)
            monkeypatch.setattr(RoomMapper, 'find', mock_room_find)
            assert(views.validate_make_new_reservation_room_user_exists(roomId, userId) is None)

def test_invalid_make_new_reservation_room_user_exists_user_missing(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            roomId = '1'
            userId = '5'
            def mock_user_not_found(_):
                return
            def mock_room_find(_):
                return Room(1, False)
            monkeypatch.setattr(UserMapper, 'find', mock_user_not_found)
            monkeypatch.setattr(RoomMapper, 'find', mock_room_find)
            assert(views.validate_make_new_reservation_room_user_exists(roomId, userId).status_code is views.STATUS_CODE['NOT_FOUND'])

def test_invalid_make_new_reservation_room_user_exists_room_missing(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            roomId = '1'
            userId = '5'
            def mock_user_find(_):
                return User(5, 'kwazy', 'kupkakes')
            def mock_room_not_found(_):
                return
            monkeypatch.setattr(RoomMapper, 'find', mock_room_not_found)
            monkeypatch.setattr(UserMapper, 'find', mock_user_find)
            assert(views.validate_make_new_reservation_room_user_exists(roomId, userId).status_code is views.STATUS_CODE['NOT_FOUND'])

def test_valid_make_new_reservation_timeslots_without_reservations():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            dateList = ['2040', '04', '04']
            startTime = 5
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert(result == None)

def test_valid_make_new_reservation_timeslots_with_reservations():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(1,2,'2020-01-01', '', 1)
            room = Room(1, False)
            user = User(1, 'mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', 1)
            reservations.append(reservation1)

            dateList = ['2040', '04', '04']
            startTime = 5
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert(result == None)

def test_valid_make_new_reservation_timeslots_with_reservations_lower_bound():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5,8,'2020-01-01', '', 1)
            room = Room(1, False)
            user = User(1, 'mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', 1)
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 3
            endTime = 5

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert(result == None)

def test_valid_make_new_reservation_timeslots_with_reservations_upper_bound():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5,8,'2020-01-01', '', 1)
            room = Room(1, False)
            user = User(1, 'mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', 1)
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 8
            endTime = 10

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert(result == None)



def test_invalid_make_new_reservation_timeslots_overlapping_time_1():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5,7,'2020-01-01', '', 1)
            room = Room(1, False)
            user = User(1, 'mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', 1)
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 5
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert(result.status_code == views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_make_new_reservation_timeslots_overlapping_time_2():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5,8,'2020-01-01', '', 1)
            room = Room(1, False)
            user = User(1, 'mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', 1)
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 6
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert(result.status_code == views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_make_new_reservation_timeslots_overlapping_time_3():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5,8,'2020-01-01', '', 1)
            room = Room(1, False)
            user = User(1, 'mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', 1)
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 4
            endTime = 7

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert(result.status_code == views.STATUS_CODE['UNPROCESSABLE'])

def test_invalid_make_new_reservation_timeslots_overlapping_time_4():
    with app.app_context():
        with app.test_request_context():
            reservations = []
            time = Timeslot(5,8,'2020-01-01', '', 1)
            room = Room(1, False)
            user = User(1, 'mr', 'pickles')
            reservation1 = Reservation(room, user, time, 'description', 1)
            reservations.append(reservation1)

            dateList = ['2020', '01', '01']
            startTime = 6
            endTime = 9

            result = views.validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime)
            assert(result.status_code == views.STATUS_CODE['UNPROCESSABLE'])


