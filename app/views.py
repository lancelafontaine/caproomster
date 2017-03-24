from app import app
from .decorators import *
from flask import request, jsonify
from app.mapper import ReservationMapper
from app.mapper import RoomMapper
from app.mapper import UserMapper
from app.mapper import TimeslotMapper
from app.core.timeslot import Timeslot
from datetime import datetime
from random import randint
from collections import namedtuple
import calendar

STATUS_CODE = {
    'OK': 200,
    'UNAUTHORIZED': 401,
    'NOT_FOUND': 404,
    'UNPROCESSABLE': 422
}
RAND_UPPER = 999999

##############
# DECORATORS #
##############

def require_login(func):
    def wrapper(*args, **kwargs):
        if not is_logged_in_bool():
            return unauthorized()
        return func(*args, **kwargs)
    wrapper.func_name = func.func_name
    return wrapper

##########
# ROUTES #
##########

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'404': 'Not Found'})

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'500': 'Internal Server Error'})

@app.route('/login', methods=['GET', 'POST'])
@nocache
def login():
    if request.method == 'POST':
        data = request.get_json();
        return validate_login(data)

    if request.method == 'GET':
        return is_logged_in()

@app.route('/logout', methods=['GET'])
@nocache
def logout():
    session.clear()
    return jsonify({'logout success': 'Successfully logged out.'})

@app.route('/rooms/all', methods=['GET'])
@nocache
@require_login
def get_all_rooms():
    if request.method == 'GET':
        room_models = RoomMapper.findAll()
        rooms = sorted([room.getId() for room in room_models])
        roomdata = {
            'rooms':  rooms
        }
        return jsonify(roomdata)

@app.route('/reservations/create', methods=['POST'])
@nocache
@require_login
def make_new_reservation():
    if request.method == 'POST':
        data = request.get_json()
        return validate_new_reservation(data)


####################
# HELPER FUNCTIONS #
####################

def validate_login(data):
    if 'userId' not in data or 'password' not in data:
        response = jsonify({'login error': '`userId` and `password` fields are required.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if str(data['userId']).isdigit() == False:
        response = jsonify({'login error': '`userId` must be an integer.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    user = UserMapper.find(int(data['userId']))
    if not user:
        response = jsonify({'login error': 'That user does not exist.'})
        response.status_code = STATUS_CODE['NOT_FOUND']
        return response

    if user.getPassword() != str(data['password']):
        response = jsonify({'login error': 'Credentials refused for that user.'})
        response.status_code = STATUS_CODE['UNAUTHORIZED']
        return response

    session['logged_in'] = True
    session['userId'] = user.getId()

    success = {
        'login success': 'Successfully logged in',
        'data': {
            'userId': str(user.getId()),
            'username': str(user.getName())
        }
    }
    return jsonify(success)


def is_logged_in_bool():
    return 'logged_in' in session and 'userId' in session and session['logged_in']

def is_logged_in():
    if is_logged_in_bool():
        response = {
            'success': {
                'userId': session['userId']
            }
        }
        return jsonify(response)
    return unauthorized()

def unauthorized():
    response = jsonify({'unauthorized': 'Not logged in. You must login.'})
    response.status_code = STATUS_CODE['UNAUTHORIZED']
    return response

def validate_new_reservation(data):
    response = validate_make_new_reservation_payload_format(data)
    if response:
        return response

    startTime = int(data['startTime'])
    endTime = int(data['endTime'])
    response = validate_make_new_reservation_times(startTime, endTime)
    if response:
        return response

    date = str(data['date'])
    dateList = date.split('-')
    response = validate_make_new_reservation_date(dateList)
    if response:
        return response

    roomId = data['roomId']
    userId = data['userId']

    response = validate_make_new_reservation_room_user_exists(roomId, userId)
    if response:
        return response

    reservation = ReservationMapper.findAll()
    response = validate_make_new_reservation_timeslots(reservation, dateList, startTime, endTime)
    if response:
        return response

    # no use for `block` parameter, for now, just passing empty string
    time = TimeslotMapper.makeNew(startTime, endTime, date, '', userId)
    TimeslotMapper.done()
    room = RoomMapper.find(roomId)
    user = UserMapper.find(userId)
    description = str(data['description'])
    reservation = ReservationMapper.makeNew(room, user, time, description, randint(0,RAND_UPPER))
    ReservationMapper.done()

    response_data = {
        'makeNewReservation': 'successfully created the reservation',
        'reservationId': reservation.getId()
    }
    return jsonify(response_data)

def validate_make_new_reservation_payload_format(data):
    if 'roomId' not in data or \
       'userId' not in data or \
       'startTime' not in data or \
       'endTime' not in data or \
       'date' not in data or \
       'description' not in data:
        response = jsonify({'makeNewReservation error': '`roomId`, `userId`, `startTime`, `endTime`, `date` and `description` fields are required.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if not str(data['startTime']).isdigit() or \
       not str(data['endTime']).isdigit() or \
       not str(data['userId']).isdigit():
        response = jsonify({'makeNewReservation error': '`userId`, `startTime` and `endTime` must be integers.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

def validate_make_new_reservation_times(startTime, endTime):
    if startTime < 0 or startTime > 23 or endTime < 0 or endTime > 23 or  startTime == endTime:
        response = jsonify({'makeNewReservation error': '`startTime` and `endTime` must be different integers between 0 and 23.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if (endTime - startTime) % 24 > 3:
        response = jsonify({'makeNewReservation error': 'The reservation cannot last for longer than 3 hours.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

def validate_make_new_reservation_date(dateList):
    def date_error():
        response = jsonify({'makeNewReservation error': '`date` must be in the format 2034-03-03 and must be a valid date, today or in the future.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if len(dateList) != 3:
        return date_error()

    for field in dateList:
        if not field.isdigit():
            return date_error()

    try:
        payload_date = datetime(int(dateList[0]), int(dateList[1]), int(dateList[2]))
    except ValueError:
        return date_error()

    now = datetime.now()
    current_date = datetime(now.year, now.month, now.day)
    if payload_date < current_date:
        return date_error()

def validate_make_new_reservation_room_user_exists(roomId, userId):
    if not UserMapper.find(userId) or not RoomMapper.find(roomId):
        response = jsonify({'makeNewReservation error': 'Either the room or user does not exist.'})
        response.status_code = STATUS_CODE['NOT_FOUND']
        return response

def validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime):
    # TO DO: check that the user's hours of reservation per week does not exceed 3
    def time_overlap_error():
        response = jsonify({'makeNewReservation error': 'This reservation\'s timeslot conflict with an existing reservation\'s timeslot. Calls the addToWaitingList endpoint with this data.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    def to_timestamp(date_list, time):
        return calendar.timegm(datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(time)).timetuple())

    new_timestamp_start = to_timestamp(dateList, startTime)
    new_timestamp_end = to_timestamp(dateList, endTime)

    for reservation in reservations:
        timeslot = reservation.getTimeslot()
        timeslot_date_list= timeslot.getDate().isoformat().split('-')

        existing_timestamp_start = to_timestamp(timeslot_date_list, timeslot.getStartTime())
        existing_timestamp_end = to_timestamp(timeslot_date_list, timeslot.getEndTime())

        if (new_timestamp_start < existing_timestamp_end) and \
           (new_timestamp_end > existing_timestamp_start):
            return time_overlap_error()









