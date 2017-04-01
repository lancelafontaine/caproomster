from app import app
from .decorators import *
from flask import request, jsonify
from app.mapper import ReservationMapper
from app.mapper import RoomMapper
from app.mapper import UserMapper
from app.mapper import TimeslotMapper
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
        return jsonify(data)


@app.route('/reservations/all', methods=['GET'])
@nocache

def addNewReservation(month,day):

	if month == 'september':
		m = '09'
		redirectTo = "september.html"
	if month == 'october':
		m = '10'
		redirectTo = "october.html"
	if month == 'november':
		m = '11'
		redirectTo = "november.html"
	if month == 'december':
		m = '12'
		redirectTo = "december.html"
	if month == 'january':
		m = '01'
		redirectTo = "january.html"
	if month == 'february':
		m = '02'
		redirectTo = "february.html"
	if month == 'march':
		m = '03'
		redirectTo = "march.html"
	if month == 'april':
		m = '04'
		redirectTo = "april.html"
	if month == 'may':
		m = '05'
		redirectTo = "may.html"
	if month == 'june':
		m = '06'
		redirectTo = "june.html"
	if month == 'july':
		m = '07'
		redirectTo = "july.html"
	if month == 'august':
		m = '08'
		redirectTo = "august.html"
	if int(day) < 10:
		date = '2016-' + m + '-0' + day
	else:
		date = '2016-' + m + '-' + day
	rooms = checkAvailabilities.checkAvailabilities(date)
	if request.method == 'POST':
		if request.form.getlist('chosenTime'):
			chosenTime = request.form.getlist('chosenTime')
			endTime = int(chosenTime[-1])
			startTime = int(chosenTime[0])
			roomId = request.form.getlist('room')
			block = endTime + 1 - startTime
			if block < 3:
				block = block + 1
				description = request.form['description']
				processed_description = description.upper()
				user = UserMapper.find(session['userId'])
				if checkAvailabilities.validateAvailability(roomId[0],date,startTime, endTime):
					userTimeslots = TimeslotTDG.findUser(user.getId())
					checkBlock = 0
					print(userTimeslots)
					if userTimeslots:
						print("userTimeslots:")
						for timeslots in userTimeslots:
							checkBlock = checkBlock + timeslots[2] + 1 - timeslots[1]
						for timeslots in userTimeslots:
							print("checkBlock:")
							print (checkBlock)
							if str(timeslots[3]) == str(date) and checkBlock >1:
								print(timeslots[3])
								return render_template(redirectTo, allowed = "You can only have a reservation that totals to 2 hours per day")
						room = Room(roomId[0], False)
						if registry.initiateAction():
							# Instantiate parameters
							timeSlot = TimeslotMapper.makeNew(startTime, endTime, date, block, user.getId())
							TimeslotMapper.save(timeSlot)
							timeslotId = TimeslotMapper.findId(user.getId())
							timeSlot.setId(timeslotId)
							# Make Reservation
							reservation = ReservationMapper.makeNewReservation(room, user, timeSlot,
																			   processed_description, timeslotId)
							ReservationMapper.save(reservation)
							#registry.endAction()
							return redirect(url_for('dashboard', user=session['user']))
					else:
						room = Room(roomId[0],False)
						if registry.initiateAction():
							#Instantiate parameters
							timeSlot = TimeslotMapper.makeNew(startTime,endTime,date,block, user.getId())
							TimeslotMapper.save(timeSlot)
							timeslotId = TimeslotMapper.findId(user.getId())
							timeSlot.setId(timeslotId)
							#Make Reservation
							reservation = ReservationMapper.makeNewReservation(room, user, timeSlot, processed_description,timeslotId)
							ReservationMapper.save(reservation)
							#registry.endAction(room.getId())
							return redirect(url_for('dashboard', user=session['user']))
				else:
					userTimeslots = TimeslotTDG.findUser(user.getId())
					if userTimeslots:
						print("userTimeslots:")
						for timeslots in userTimeslots:
							if str(timeslots[3]) == str(date):
								print(timeslots[3])
								return render_template('month.html', allowed="You can only have 1 reservation per day")
					else:
						room = Room(roomId[0], False)
						timeSlot = TimeslotMapper.makeNew(startTime, endTime, date, block, user.getId())
						TimeslotMapper.save(timeSlot)
						timeslotId = TimeslotMapper.findId(user.getId())
						timeSlot.setId(timeslotId)
						waiting = WaitingMapper.makeNew(room,description,user,timeSlot)
						WaitingMapper.save(waiting)
						return redirect(url_for('dashboard', user=session['user']))
			else:
				return render_template('add.html', allowed="You can only reserve the room for 2 consecutive hours.", rooms=rooms)
	return render_template('add.html',rooms=rooms, allowed="")


# annee mois jour
# fetch dans le timeslottable de ses meme temps

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
    response = validate_make_new_reservation_payload_format(data)
    if response:
        return response

    startTime = int(data['timeslot']['startTime'])
    endTime = int(data['timeslot']['endTime'])
    response = validate_make_new_reservation_times(startTime, endTime)
    if response:
        return response

    date = str(data['timeslot']['date'])
    dateList = date.split('-')
    response = validate_make_new_reservation_date(dateList)
    if response:
        return response

    roomId = data['roomId']
    username = data['username']

    response = validate_make_new_reservation_room_user_exists(roomId, username)
    if response:
        return response

    reservation = ReservationMapper.findAll()
    response = validate_make_new_reservation_timeslots(reservation, dateList, startTime, endTime)
    if response:
        return response

    # no use for `block` parameter, for now, just passing empty string
    time = TimeslotMapper.makeNew(startTime, endTime, date, '', username, str(uuid4()))
    TimeslotMapper.done()
    room = RoomMapper.find(roomId)
    user = UserMapper.find(username)
    description = str(data['description'])
    reservation = ReservationMapper.makeNew(room, user, time, description, str(uuid4()))
    ReservationMapper.done()

    response_data = {
        'makeNewReservation': 'successfully created the reservation',
        'reservationId': reservation.getId()
    }
    return jsonify(response_data)


def validate_make_new_reservation_payload_format(data):
    if 'roomId' not in data or \
                    'username' not in data or \
                    'timeslot' not in data or \
                    'description' not in data:
        response = jsonify(
            {'makeNewReservation error': '`roomId`, `username`, `timeslot`, and `description` fields are required.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if 'startTime' not in data['timeslot'] or \
                    'endTime' not in data['timeslot'] or \
                    'date' not in data['timeslot']:
        response = jsonify(
            {'makeNewReservation error': '`startTime`, `endTime`, `date` fields are required in `timeslot`.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response

    if not str(data['timeslot']['startTime']).isdigit() or \
            not str(data['timeslot']['endTime']).isdigit():
        response = jsonify({'makeNewReservation error': '`startTime` and `endTime` must be integers.'})
        response.status_code = STATUS_CODE['UNPROCESSABLE']
        return response


def validate_make_new_reservation_times(startTime, endTime):
    if startTime < 0 or startTime > 23 or endTime < 0 or endTime > 23 or startTime == endTime:
        response = jsonify(
            {'makeNewReservation error': '`startTime` and `endTime` must be different integers between 0 and 23.'})
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


def validate_make_new_reservation_room_user_exists(roomId, username):
    if not UserMapper.find(username) or not RoomMapper.find(roomId):
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

    if reservations:
        for reservation in reservations:
            timeslot = reservation.getTimeslot()
            timeslot_date_list = timeslot.getDate().split('-')

            existing_timestamp_start = to_timestamp(timeslot_date_list, timeslot.getStartTime())
            existing_timestamp_end = to_timestamp(timeslot_date_list, timeslot.getEndTime())

<<<<<<< HEAD

=======
            if (new_timestamp_start < existing_timestamp_end) and \
                    (new_timestamp_end > existing_timestamp_start):
                return time_overlap_error()
>>>>>>> master
