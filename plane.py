from vector import Vector
from ray import Ray
from isect import Intersection
import math

class Plane:
	def __init__(self, dict, shader_dict):
		self.face_normal = Vector(*dict['face_normal']).normalize()
		self.offset = dict['offset']
		self.shader = shader_dict[dict['shader']]
	
	def intersect(self, ray):
		normalDotOrigin = self.face_normal.dot(ray.origin)
		normalDotDirection = self.face_normal.dot(ray.direction)
		
		if normalDotDirection >= 0:
			return None
		else:
			return Intersection(self, ray, (self.offset - normalDotOrigin) / normalDotDirection)
	
	def normal(self, point):
		return self.face_normal