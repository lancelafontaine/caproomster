# Waiting object
class Waiting:
	# Constructor
	def __init__(self, room, user, timeslot, description, equipment, waitingId):
		self.user = user
		self.timeslot = timeslot
		self.room = room
		self.description = description
		self.equipment = equipment
		self.waitingId = waitingId

	# Print method for debugging
	def __str__(self):
		return "Waiting Info: \n Holder: " + \
		       str(self.user.getName()) + \
		       str(self.timeslot) + \
		       "Description: " + str(self.description) + \
		       "Equipment: " + str(self.equipment) + \
		       "WID: " + str(self.waitingId)

	# Accessors and Mutators
	def getId(self):
		return self.waitingId

	def setId(self, waitingId):
		self.waitingId = waitingId

	def getTimeslot(self):
		return self.timeslot

	def setTimeslot(self, time):
		self.timeslot = time

	def getRoom(self):
		# type: () -> object
		"""

		:rtype: object
		"""
		return self.room

	def setRoom(self, room):
		self.room = room

	def getUser(self):
		return self.user

	def setUser(self, user):
		self.user = user

	def getDescription(self):
		return self.description

	def setDescription(self, description):
		self.description = description

	def setEquipment(self, equipment):
		self.equipment = equipment

	def getEquipment(self):
		return self.equipment

	def to_dict(self):
		waiting_data = {}
		waiting_data['room'] = {}
		waiting_data['room']['roomId'] = self.getRoom().getId()
		waiting_data['user'] = {}
		waiting_data['user']['username'] = self.getUser().getName()
		waiting_data['user']['userId'] = self.getUser().getId()
		waiting_data['timeslot'] = {}
		waiting_data['timeslot']['startTime'] = self.getTimeslot().getStartTime()
		waiting_data['timeslot']['endTime'] = self.getTimeslot().getEndTime()
		waiting_data['timeslot']['date'] = self.getTimeslot().getDate().strftime('%Y/%m/%d')
		waiting_data['timeslot']['timeId'] = self.getTimeslot().getId()
		waiting_data['equipment'] = {}
		waiting_data['equipment']['laptops'] = self.getEquipment().equipment['laptops']
		waiting_data['equipment']['projectors'] = self.getEquipment().equipment['projectors']
		waiting_data['equipment']['whiteboards'] = self.getEquipment().equipment['whiteboards']
		waiting_data['description'] = self.getDescription()
		waiting_data['reservationId'] = self.getId()
		return waiting_data
