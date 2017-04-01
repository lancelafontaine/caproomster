# Reservation object
class Reservation:
	# Constructor
	def __init__(self, room, user, timeslot, description, equipment, reservationId):
		self.user = user
		self.timeslot = timeslot
		self.room = room
		self.description = description
		self.reservationId = reservationId
		self.equipment = equipment

	# Print method for debugging
	def __str__(self):
		return "Reservation Info" + \
		       "Holder: " + str(self.user.getName()) + \
		       self.timeslot + \
		       "Description: " + str(self.description) + \
		       "Equipment: " + str(self.equipment) + \
		       "RID: " + str(self.reservationId)

	# Accessors and Mutators
	def getId(self):
		return self.reservationId

	def setId(self, reservationId):
		self.reservationId = reservationId

	def getTimeslot(self):
		return self.timeslot

	def setTimeslot(self, time):
		self.timeslot = time

	def getRoom(self):
		"""

		:rtype: Room
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
		"""

		:rtype: Equipment
		"""
		return self.equipment

	def to_dict(self):
		reservation_data = {}
		reservation_data['room'] = {}
		reservation_data['room']['roomId'] = self.getRoom().getId()
		reservation_data['user'] = {}
		reservation_data['user']['username'] = self.getUser().getName()
		reservation_data['user']['userId'] = self.getUser().getId()
		reservation_data['timeslot'] = {}
		reservation_data['timeslot']['startTime'] = self.getTimeslot().getStartTime()
		reservation_data['timeslot']['endTime'] = self.getTimeslot().getEndTime()
		reservation_data['timeslot']['date'] = self.getTimeslot().getDate()
		reservation_data['timeslot']['timeId'] = self.getTimeslot().getId()
		reservation_data['equipment']['laptop'] = self.getEquipment()['laptop']
		reservation_data['equipment']['projector'] = self.getEquipment()['projector']
		reservation_data['equipment']['whiteboard'] = self.getEquipment()['whiteboard']
		reservation_data['description'] = self.getDescription()
		reservation_data['reservationId'] = self.getId()
		return reservation_data
