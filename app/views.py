from app import app
from .decorators import *
from flask import request, jsonify
from app.mapper import ReservationMapper
from app.mapper import WaitingMapper
from app.mapper import RoomMapper
from app.mapper import UserMapper
from app.mapper import TimeslotMapper
from app.mapper import EquipmentMapper
from datetime import datetime
import calendar
from uuid import uuid4

STATUS_CODE = {
    'OK': 200,
    'UNAUTHORIZED': 401,
    'NOT_FOUND': 404,
    'UNPROCESSABLE': 422
}


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
        if room_models:
            rooms = sorted([room.getId() for room in room_models])
        else:
            rooms = []
        roomdata = {
            'rooms': rooms
        }
        return jsonify(roomdata)


@app.route('/reservations/create', methods=['POST'])
@nocache
@require_login
def make_new_reservation():
    if request.method == 'POST':
        data = request.get_json()
        return validate_new_reservation(data)


@app.route('/reservations/room/<roomId>', methods=['GET'])
@nocache
@require_login
def get_reservations_by_room(roomId):
    if request.method == 'GET':
        reservations = ReservationMapper.findByRoom(roomId)
        reservations_data = []
        if reservations:
            for reservation in reservations:
                reservations_data += [reservation.to_dict()]
        data = {
            'roomId': roomId,
            'reservations': reservations_data
        }
        waitings = WaitingMapper.findByRoom(roomId)
        waitings_data = []
        if waitings:
            for waiting in waitings:
                waitings_data += [waiting.to_dict()]
        data.update({'waitings': waitings_data})
        return jsonify(data)


@app.route('/reservations/user/<username>', methods=['GET'])
@nocache
@require_login
def get_reservations_by_user(username):
    if request.method == 'GET':
        reservations = ReservationMapper.findByUser(str(username))
        reservations_data = []
        if reservations:
            for reservation in reservations:
                reservations_data += [reservation.to_dict()]
        data = {
            'username': username,
            'reservations': reservations_data
        }
        waitings = WaitingMapper.findByUser(str(username))
        waitings_data = []
        if waitings:
            for waiting in waitings:
                waitings_data += [waiting.to_dict()]
        data.update({'waitings': waitings_data})
        return jsonify(data)


@app.route('/reservations/all', methods=['GET'])
@nocache
@require_login
def get_all_reservations():
    if request.method == 'GET':
        reservations = ReservationMapper.findAll()
        reservations_data = []
        if reservations:
            for reservation in reservations:
                reservations_data += [reservation.to_dict()]
        data = {
            'reservations': reservations_data
        }
        waitings = WaitingMapper.findAll()
        waitings_data = []
        if waitings:
            for waiting in waitings:
                waitings_data += [waiting.to_dict()]
        data.update({'waitings': waitings_data})
        return jsonify(data)


@app.route('/reservations/<reservationId>', methods=['DELETE'])
@nocache
@require_login
def delete_reservation(reservationId):
    if request.method == 'DELETE':
        reservation = ReservationMapper.find(reservationId)
        waiting = WaitingMapper.find(reservationId)
        if not reservation and not waiting:
            response = jsonify({'reservation error': 'that reservationId does not exist'})
            response.status_code = STATUS_CODE['NOT_FOUND']
            return response

        if reservation:
            ReservationMapper.delete(reservationId)
            ReservationMapper.done()
            data = {
                'success': 'reservation successfully deleted',
                'reservationId': reservationId
            }
        if waiting:
            WaitingMapper.delete(reservationId)
            WaitingMapper.done()
            data = {
                'success': 'reservation on waiting list successfully deleted',
                'waitingId': reservationId
            }

        # update reservation and waiting lists here
        return jsonify(data)


####################
# HELPER FUNCTIONS #
####################

def validate_login(data):
    if 'username' not in data or 'password' not in data:
        response = jsonify({'login error': '`username` and `password` fields are required.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    user = UserMapper.find(str(data['username']))
    if not user:
        response = jsonify({'login error': 'That user does not exist.'})
        response.status_code = STATUS_CODE['NOT_FOUND']
        return response

    if user.getPassword() != str(data['password']):
        response = jsonify({'login error': 'Credentials refused for that user.'})
        response.status_code = STATUS_CODE['UNAUTHORIZED']
        return response

    session['logged_in'] = True
    session['username'] = user.getId()

    success = {
        'login success': 'Successfully logged in',
        'data': {
            'username': str(user.getId()),
            'capstone': str(user.isCapstone())
        }
    }
    return jsonify(success)


def is_logged_in_bool():
    return 'logged_in' in session and 'username' in session and session['logged_in']


def is_logged_in():
    if is_logged_in_bool():
        response = {
            'success': {
                'username': session['username']
            }
        }
        return jsonify(response)
    return unauthorized()


def unauthorized():
    response = jsonify({'unauthorized': 'Not logged in. You must login.'})
    response.status_code = STATUS_CODE['UNAUTHORIZED']
    return response


def validate_new_reservation(data):
    response = validate_reservation_payload_format(data)
    if response:
        return response

    startTime = int(data['timeslot']['startTime'])
    endTime = int(data['timeslot']['endTime'])
    date = str(data['timeslot']['date'])
    dateList = date.split('/')
    roomId = data['roomId']
    username = data['username']
    description = str(data['description'])
    laptop = int(data['equipment']['laptop'])
    board = int(data['equipment']['board'])
    projector = str(data['equipment']['projector'])


    response = validate_make_new_reservation_date(dateList)
    if response:
        return response

    response = validate_reservation_room_user_exists(roomId, username)
    if response:
        return response

    reservations = ReservationMapper.findAll()

    # no use for `block` parameter, for now, just passing empty strin
    time = TimeslotMapper.makeNew(startTime, endTime, datetime(int(dateList[0]), int(dateList[1]), int(dateList[2])), '', username, str(uuid4()))
    TimeslotMapper.done()
    room = RoomMapper.find(roomId)
    user = UserMapper.find(username)
    equipment = EquipmentMapper.makeNew(laptop, projector, board, str(uuid4()))
    EquipmentMapper.done()


    if validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime):
        return jsonify(commit_new_waiting(room, user, time, description, equipment))
    else:
        return jsonify(commit_new_reservation(room, user, time, description, equipment))


def commit_new_waiting(room, user, time, description, equipment):
    waiting = WaitingMapper.makeNew(room, user, time, description, equipment, str(uuid4()))
    WaitingMapper.done()
    response_data = {
        'makeNewReservation': 'there is a conflict: added to the waitlist',
        'waitingId': waiting.getId()
    }
    return response_data


def commit_new_reservation(room, user, time, description, equipment):
    reservation = ReservationMapper.makeNew(room, user, time, description, equipment, str(uuid4()))
    ReservationMapper.done()
    response_data = {
        'makeNewReservation': 'successfully created reservation',
        'reservation': reservation.getId()
    }
    return response_data


def validate_reservation_payload_format(data):

    response_data = {'error': ''}

    if 'roomId' not in data or \
                    'username' not in data or \
                    'timeslot' not in data or \
                    'equipment' not in data or \
                    'description' not in data:
        response_data['error'] = '`roomId`, `username`, `timeslot`, `equipment` and `description` fields are required.'
        response = jsonify(response_data)
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if 'startTime' not in data['timeslot'] or \
                    'endTime' not in data['timeslot'] or \
                    'date' not in data['timeslot']:
        response_data['error'] = '`startTime`, `endTime`, `date` fields are required in `timeslot`.'
        response = jsonify(response_data)
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if 'laptop' not in data['equipment'] or \
                    'projector' not in data['equipment'] or \
                    'board' not in data['equipment']:
        response_data['error'] = '`laptop`, `projector`, `board` fields are required in `equipment`.'
        response = jsonify(response_data)
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if not str(data['timeslot']['startTime']).isdigit() or \
                    not str(data['timeslot']['endTime']).isdigit() or \
                    not str(data['equipment']['laptop']).isdigit() or \
                    not str(data['equipment']['projector']).isdigit() or \
                    not str(data['equipment']['board']).isdigit():
        response_data['error'] = '`laptop`, `projector`, `board`, `startTime` and `endTime` fields must be integers`.'
        response = jsonify(response_data)
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    startTime = int(data['timeslot']['startTime'])
    endTime = int(data['timeslot']['endTime'])

    if startTime < 0 or startTime > 23 or endTime < 0 or endTime > 23 or startTime == endTime:
        response_data['error'] = '`startTime` and `endTime` must be integers between 0 and 23'
        response = jsonify(response_data)
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if (endTime - startTime) % 24 > 3:
        response_data['error'] = 'The reservation cannot last for longer than 3 hours.'
        response = jsonify(response_data)
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response


def validate_make_new_reservation_date(dateList):
    def date_error():
        response = jsonify({'makeNewReservation error': '`date` must be in the format 2034/03/03 and must be a valid date, today or in the future.'})
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


def validate_reservation_room_user_exists(roomId, username):
    if not UserMapper.find(username) or not RoomMapper.find(roomId):
        response = jsonify({'makeNewReservation error': 'Either the room or user does not exist.'})
        response.status_code = STATUS_CODE['NOT_FOUND']
        return response


def validate_make_new_reservation_timeslots(reservations, dateList, startTime, endTime):
    def to_timestamp(date_list, time):
        return calendar.timegm(datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(time)).timetuple())

    new_timestamp_start = to_timestamp(dateList, startTime)
    new_timestamp_end = to_timestamp(dateList, endTime)

    if reservations:
        for reservation in reservations:
            timeslot = reservation.getTimeslot()
            timeslot_date_list = timeslot.getDate().strftime('%Y/%m/%d').split('/')

            existing_timestamp_start = to_timestamp(timeslot_date_list, timeslot.getStartTime())
            existing_timestamp_end = to_timestamp(timeslot_date_list, timeslot.getEndTime())

            if (new_timestamp_start < existing_timestamp_end) and \
                    (new_timestamp_end > existing_timestamp_start):
                return True
    return False
