from app import app
from .decorators import *
from flask import request, jsonify
from app.mapper import ReservationMapper
from app.mapper import WaitingMapper
from app.mapper import TimeslotMapper
from app.mapper import EquipmentMapper
from app.mapper import UserMapper
from app.reservationbook import ReservationBook
from datetime import datetime
from constants import STATUS_CODE

reservationbook = ReservationBook()

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
        roomdata = {
            'rooms': reservationbook.get_all_rooms()
        }
        return jsonify(roomdata)


@app.route('/reservations/create', methods=['POST'])
@nocache
@require_login
def make_new_reservation():
    if request.method == 'POST':
        data = request.get_json()
        response = validate_reservation_payload_format(data)
        if response:
            return response
        return reservationbook.make_new_reservation(data)


@app.route('/reservations/room/<roomId>', methods=['GET'])
@nocache
@require_login
def get_reservations_by_room(roomId):
    if request.method == 'GET':
        return reservationbook.get_reservations_by_room(roomId)


@app.route('/reservations/user/<username>', methods=['GET'])
@nocache
@require_login
def get_reservations_by_user(username):
    if request.method == 'GET':
        return reservationbook.get_reservations_by_user(username)

@app.route('/reservations/all', methods=['GET'])
@nocache
@require_login
def get_all_reservations():
    if request.method == 'GET':
        return reservationbook.get_all_reservations()

@app.route('/reservations/<reservationId>', methods=['DELETE'])
@nocache
@require_login
def delete_reservation(reservationId):
    if request.method == 'DELETE':
        return reservationbook.delete_reservation(reservationId)


####################
# HELPER FUNCTIONS #
####################

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

    date = str(data['timeslot']['date'])
    dateList = date.split('/')

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
