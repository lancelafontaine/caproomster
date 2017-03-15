from app import app
from .decorators import *
from flask import request, jsonify
from app.mapper import ReservationMapper
from app.mapper import UserMapper
from app.mapper import WaitingMapper
from app.mapper import TimeslotMapper
from app.core.room import Room
from app.core.registry import *
from app.core import update
from app.core.reservationbook import ReservationBook
from app.core import checkAvailabilities
from app.TDG import WaitingTDG
from app.TDG import ReservationTDG
from app.TDG import TimeslotTDG
import datetime
rListDb = ReservationMapper.findAll()
reservationList = []
waitingList = []
waitingList = WaitingMapper.findAll()
for index, rId in enumerate(rListDb):
    reservationList.append(ReservationMapper.find(rId.getId()))
reservationBook = ReservationBook(reservationList, waitingList)
registry = Registry(reservationBook)

STATUS_CODE = {
    'UNAUTHORIZED': 401,
    'NOT_FOUND': 404,
    'UNPROCESSABLE': 422
}

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'404': 'Not Found'})

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'500': 'Internal Server Error'})

@app.route('/login', methods=['GET', 'POST'])
def login():

    # Login attempted
    if request.method == 'POST':
        data = request.get_json();
        return validate_login(data)

    # Checking if current user is logged in
    if request.method == 'GET':
        return is_logged_in()

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


def is_logged_in():
    if 'logged_in' in session and 'userId' in session and session['logged_in'] and session['userId']:
        response = {
            'success': {
                'userId': session['userId']
            }
        }
        return jsonify(response)
    response = jsonify({'error': 'not logged in'})
    response.status_code = STATUS_CODE['UNAUTHORIZED']
    return response


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.clear()
    return jsonify({'logout success': 'Successfully logged out.'})




#reservation
@app.route('/dashboard/<user>')
@login_required
@nocache
def dashboard(user):
    session['user'] = user
    reservation1 = []
    userReservation = ReservationTDG.findUserRes(session['userId'])


    for reservation in userReservation:
        print(reservation)
        reservation1.append(reservation[1])
        reservation1.append(reservation[6])
        endTime = reservation[7] + 1
        reservation1.append(endTime)
        reservation1.append(reservation[8])
        reservation1.append(reservation[2])
        reservation1.append(reservation[0])

    waitings1 = []
    userWaiting = WaitingTDG.findByUser(session['userId'])

    for waitingRes in userWaiting:
        waitings1.append(waitingRes[1])
        waitings1.append(waitingRes[6])
        endTime = waitingRes[7] + 1
        waitings1.append(endTime)
        waitings1.append(waitingRes[8])
        waitings1.append(waitingRes[3])
        waitings1.append(waitingRes[0])

    return render_template('index.html',user=user, reservation=reservation1, waitings=waitings1)


@app.route('/cancel/<reservationId>')
@login_required
@nocache
def cancel(reservationId):
    registry.getReservationBook().setReservationList(ReservationMapper.findAll())
    registry.getReservationBook().setWaitingList(WaitingMapper.findAll())
    reservation = ReservationTDG.find(reservationId)
    roomId = reservation[0][1]
    print(reservation[0][4])
    timeslot = TimeslotTDG.find(reservation[0][4])
    print(timeslot[0][4])
    registry.initiateAction(roomId)
    registry.cancelReservation(reservationId)
    registry.endAction(roomId)
    ReservationTDG.delete(reservationId)
    TimeslotTDG.delete(reservationId)
    roomsAvailable = checkAvailabilities.checkAvailabilities(timeslot[0][3])
    if(roomId == 1):
        update.updateWaiting(roomId,timeslot[0][3],roomsAvailable[0])
    if(roomId == 2):
        update.updateWaiting(roomId, timeslot[0][3], roomsAvailable[1])
    if(roomId == 3):
        update.updateWaiting(roomId, timeslot[0][3], roomsAvailable[2])
    if(roomId == 4):
        update.updateWaiting(roomId, timeslot[0][3], roomsAvailable[3])
    if(roomId == 5):
        update.updateWaiting(roomId, timeslot[0][3], roomsAvailable[4])
    return redirect(url_for('dashboard', user=session['user']))

@app.route('/cancelWaiting/<waitingId>')
@login_required
@nocache
def canceWaiting(waitingId):
    timesslotId = WaitingTDG.findTimeslot(waitingId)
    print(timesslotId[0][0])
    WaitingTDG.delete(waitingId)
    TimeslotTDG.delete(timesslotId[0][0])
    return redirect(url_for('dashboard', user=session['user']))

@app.route('/modify/<reservationId>',methods=['GET', 'POST'])
@login_required
@nocache
def modify(reservationId):
    registry.getReservationBook().setReservationList(ReservationMapper.findAll())
    registry.getReservationBook().setWaitingList(WaitingMapper.findAll())
    reservation = ReservationTDG.find(reservationId)
    #fetch room
    roomId = reservation[0][1]
    #fetch date
    timeslot = TimeslotTDG.find(reservation[0][4])
    date = timeslot[0][3]
    #query
    allResDateRoom = ReservationTDG.findDateRoom(roomId,date)
    rTime = checkAvailabilities.checkModifyAvail(allResDateRoom)
    if request.method == 'POST':
        allTime = request.form.getlist('chosenTime')
        block = int(allTime[1]) + 1 - int(allTime[0])
        starttime = int(allTime[0])
        endtime = int(allTime[1])
        block = endtime + 1 - starttime
        if block < 3:
            print(timeslot[0][0])
            print(timeslot[0][3])
            print(starttime)
            print(endtime)
            print(block)
            TimeslotTDG.update(timeslot[0][0],starttime,endtime,timeslot[0][3],block)
            return redirect(url_for('dashboard', user=session['user']))
        else:
            return redirect(url_for('dashboard', user=session['user'] ))
    return render_template('modify.html', rooms=rTime)


@app.route('/<month>/<day>',methods=['GET','POST'])
@login_required
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
                                                if registry.initiateAction(room.getId()):
                                                        # Instantiate parameters
                                                        timeSlot = TimeslotMapper.makeNew(startTime, endTime, date, block, user.getId())
                                                        TimeslotMapper.save(timeSlot)
                                                        timeslotId = TimeslotMapper.findId(user.getId())
                                                        timeSlot.setId(timeslotId)
                                                        # Make Reservation
                                                        reservation = ReservationMapper.makeNewReservation(room, user, timeSlot,
                                                                                                                                                           processed_description, timeslotId)
                                                        ReservationMapper.save(reservation)
                                                        registry.endAction(room.getId())
                                                        return redirect(url_for('dashboard', user=session['user']))
                                        else:
                                                room = Room(roomId[0],False)
                                                if registry.initiateAction(room.getId()):
                                                        #Instantiate parameters
                                                        timeSlot = TimeslotMapper.makeNew(startTime,endTime,date,block, user.getId())
                                                        TimeslotMapper.save(timeSlot)
                                                        timeslotId = TimeslotMapper.findId(user.getId())
                                                        timeSlot.setId(timeslotId)
                                                        #Make Reservation
                                                        reservation = ReservationMapper.makeNewReservation(room, user, timeSlot, processed_description,timeslotId)
                                                        ReservationMapper.save(reservation)
                                                        registry.endAction(room.getId())
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
