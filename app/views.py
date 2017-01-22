from app import app
from .decorators import *
from flask import render_template, request
from app.mapper import ReservationMapper
from app.mapper import UserMapper
from app.mapper import WaitingMapper
from app.mapper import TimeslotMapper
from app.core.room import Room
from app.core.registry import *
from app.core.directory import *
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

# create directory
roomList = []
directory = Directory(roomList)

# create registry
registry = Registry(directory, reservationBook)

@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html')

#if 500 error render 500.html
@app.errorhandler(500)
def internal_error(error):
    #db.session.rollback()
    return render_template('500.html'), 500

@app.route('/')
def home():
	return redirect(url_for('index'))
#login
@app.route('/login', methods=['GET', 'POST'])
def index():
	error = 'Invalid credentials. Please try again'
	if request.method == 'POST':
		if request.form['username'].isdigit():
			user = UserMapper.find(request.form['username'])
			if user:
				if user.getId() is int(request.form['username']):
					if user.getPassword() == request.form['password']:
						session['logged_in'] = True
						session['userId'] = user.getId()
						#fetch all user reservation
						#i.e from timeslottable
						#reservationtable
						#merge reservationdata with timeslottable then store in reservation[]
						#waitingtable
						#store the waitingtable in waiting[]

						return redirect(url_for('dashboard',user=user.getName()))
					else:
						return render_template('login.html',error=error)
				else:
					return render_template('login.html',error=error)
			else:
				return render_template('login.html', error=error)
		else:
			return render_template('login.html', error=error)
	else:
		return render_template('login.html', error="")

#logout
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	session.clear()
	return redirect(url_for('index'))

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
	registry.getDirectory().setRoomList(RoomMapper.findAll())
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
	registry.getDirectory().setRoomList(RoomMapper.findAll())
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


@app.route('/month')
@login_required
@nocache
def month():
	return render_template('month.html')

@app.route('/<month>')
@login_required
@nocache
def chooseMonth(month):
	Cm = []
	now = datetime.datetime.now()
	if month == 'september':
		Cm = 9
	if month == 'october':
		Cm = 10
	if month == 'november':
		Cm = 11
	if month == 'december':
		Cm = 12
	if month == 'january':
		Cm = 1
	if month == 'february':
		Cm = 2
	if month == 'march':
		Cm = 3
	if month == 'april':
		Cm = 4
	if month == 'may':
		Cm = 5
	if month == 'june':
		Cm = 6
	if month == 'july':
		Cm = 7
	if month == 'august':
		Cm = 8
	if now.month is Cm:
		if month == 'september':
			return render_template('january.html')
		if month == 'october':
			return render_template('october.html')
		if month == 'november':
			return render_template('november.html')
		if month == 'december':
			return render_template('december.html')
		if month == 'january':
			return render_template('january.html')
		if month == 'february':
			return render_template('february.html')
		if month == 'march':
			return render_template('march.html')
		if month == 'april':
			return render_template('april.html')
		if month == 'may':
			return render_template('may.html')
		if month == 'june':
			return render_template('june.html')
		if month == 'july':
			return render_template('july.html')
		if month == 'august':
			return render_template('august.html')
		else:
			return render_template('month.html')
	else:
		return render_template('month.html', currentmonth="You can only reserve rooms for the current month")

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


# annee mois jour
# fetch dans le timeslottable de ses meme temps
