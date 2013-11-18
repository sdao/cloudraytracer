import math

class Vector:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
	
	def magnitude(self):
		return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
	
	def normalize(self):
		mag = self.magnitude()
		return Vector(self.x / mag, self.y / mag, self.z / mag)
	
	def __add__(self, v):
		return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
	
	def __sub__(self, v):
		return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
	
	def scale(self, k):
		return Vector(self.x * k, self.y * k, self.z * k)
	
	def dot(self, v):
		return self.x * v.x + self.y * v.y + self.z * v.z
	
	def cross(self, v):
		return Vector(self.y * v.z - self.z * v.y, self.z * v.x - self.x * v.z, self.x * v.y - self.y * v.x)
	
	def __str__(self):
		return "<%f, %f, %f>" % (self.x, self.y, self.z)
		
	def invert(self):
		return Vector(-self.x, -self.y, -self.z)