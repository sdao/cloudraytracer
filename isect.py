from ray import Ray

class Intersection:
	def __init__(self, object, ray, distance):
		self.object = object
		self.ray = ray
		self.distance = distance

	def prepare(self):
		self.position = self.ray.origin + self.ray.direction.scale(self.distance)
		self.normal = self.object.normal(self.position)
		reflect_dir = self.ray.direction - self.normal.scale(self.normal.dot(self.ray.direction) * 2)
		self.reflect_ray = Ray(self.position + reflect_dir.scale(0.001), reflect_dir)