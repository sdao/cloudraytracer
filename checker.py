from color import Color
from blinnbase import BlinnBase
import math

class Checker(BlinnBase):
	def __init__(self, dict):
	   self.diffuse1 = Color(*dict['diffuse1'])
	   self.diffuse2 = Color(*dict['diffuse2'])
	   self.reflect1 = dict['reflect1']
	   self.reflect2 = dict['reflect2']
	
	def _diffuse(self, point):
		return self.diffuse1 if (math.floor(point.x) + math.floor(point.y)) % 2 == 0 else self.diffuse2
	
	def _specular(self, point):
		return Color(255, 255, 255, 255)
	
	def _reflect(self, point):
		return self.reflect1 if (math.floor(point.x) + math.floor(point.y)) % 2 == 0 else self.reflect2
	
	def _roughness(self, point):
		return 200