from vector import Vector
from ray import Ray
from isect import Intersection
import math

class Sphere:
	def __init__(self, dict, shader_dict):
		self.origin = Vector(*dict['origin'])
		self.radius = dict['radius']
		self.shader = shader_dict[dict['shader']]
	
	def intersect(self, ray):
		eo = self.origin - ray.origin
		v = eo.dot(ray.direction)
		
		dist = 0.0
		if (v >= 0.0):
			disc = math.pow(self.radius, 2) - (eo.dot(eo) - math.pow(v, 2))
			dist = 0.0 if disc < 0.0 else v - math.sqrt(disc)
		
		if (dist == 0.0):
			return None
		else:
			return Intersection(self, ray, dist)
	
	def normal(self, point):
		return (point - self.origin).normalize()