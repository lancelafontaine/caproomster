from app import app
from .decorators import *
from flask import request, jsonify
from app.mapper import ReservationMapper
from app.mapper import RoomMapper
from app.mapper import UserMapper

STATUS_CODE = {
    'OK': 200,
    'UNAUTHORIZED': 401,
    'NOT_FOUND': 404,
    'UNPROCESSABLE': 422
}

##############
# DECORATORS #
##############

def require_login(func):
    def wrapper(*args, **kwargs):
        if not is_logged_in_bool():
            return unauthorized()
        return func(*args, **kwargs)
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
def getAllRooms():
    if request.method == 'GET':
        room_models = RoomMapper.findAll()
        rooms = sorted([room.getId() for room in room_models])
        roomdata = {
            'rooms':  rooms
        }
        return jsonify(roomdata)


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

