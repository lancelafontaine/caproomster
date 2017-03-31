
class Equipment:
	def __init__(self):
		self.equipment = {}

	def __init__(self, laptops, projectors, whiteboards):
		self.equipment['laptop'] = laptops
		self.equipment['projector'] = projectors
		self.equipment['whiteboard']= whiteboards

	def __len__(self):
		return self.equipment.__len__()

