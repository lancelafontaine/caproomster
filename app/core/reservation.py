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
		       "Holder: " + str(self.user.getId()) + \
		       str(self.timeslot) + \
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
		reservation_data['room'] = self.getRoom().to_dict()
		reservation_data['user'] = self.getUser().to_dict()
		reservation_data['timeslot'] = self.getTimeslot().to_dict()
		reservation_data['equipment'] = self.getEquipment().to_dict()
		reservation_data['description'] = self.getDescription()
		reservation_data['reservationId'] = self.getId()
		return reservation_data
