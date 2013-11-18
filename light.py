from color import Color
from vector import Vector

class Light:
	def __init__(self, dict):
	   self.color = Color(*dict['color'])
	   self.position = Vector(*dict['position'])