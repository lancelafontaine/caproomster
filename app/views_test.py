from app import views, app
from app.core.user import User
from app.core.room import Room
from app.mapper import UserMapper
from app.mapper import RoomMapper
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
            response = views.getAllRooms()
            assert(response.status_code == views.STATUS_CODE['UNAUTHORIZED'])

def test_valid_get_all_rooms_with_login(monkeypatch):
    with app.app_context():
        with app.test_request_context():
            def rooms_found():
                return [Room(1, False), Room(2, False), Room(3, False)]
            monkeypatch.setattr(RoomMapper, 'findAll', rooms_found)

            views.session.clear()
            views.session.update({'logged_in': True, 'userId': 1})
            response = views.getAllRooms()
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


