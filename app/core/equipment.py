class Equipment:
	"""A wrapper for a dictionary containing different types of equipment 
	that can be borrowed for use in the study rooms."""

	def __init__(self, equipmentId, laptops=0, projectors=0, whiteboards=0):
		self.equipment = {}
		self.equipment['laptops'] = laptops
		self.equipment['projectors'] = projectors
		self.equipment['whiteboards'] = whiteboards
		self.equipmentId = equipmentId

	def __len__(self):
		accumulator = 0
		for v in self.equipment.itervalues():
			accumulator+=v
		return accumulator

	def __str__(self):
		return self.equipment.__str__()

	def getId(self):
		return self.equipmentId

	def setId(self, equipmentId):
		self.equipmentId = equipmentId