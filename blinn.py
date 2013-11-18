from color import Color
from blinnbase import BlinnBase

class Blinn(BlinnBase):
	def __init__(self, dict):
	   self.diffuse = Color(*dict['diffuse'])
	   self.specular = Color(*dict['specular'])
	   self.reflect = dict['reflect']
	   self.roughness = dict['roughness']
	
	def _diffuse(self, point):
		return self.diffuse
	
	def _specular(self, point):
		return self.specular
	
	def _reflect(self, point):
		return self.reflect
	
	def _roughness(self, point):
		return self.roughness