class Ray:
	def __init__(self, origin, direction):
		self.origin = origin
		self.direction = direction.normalize()

	def __str__(self):
		return "Origin: <%f, %f, %f>; Direction: <%f, %f, %f>" % (self.origin.x, self.origin.y, self.origin.z, self.direction.x, self.direction.y, self.direction.z)