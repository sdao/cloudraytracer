from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import StringIO
import math
import numpy
from vector import Vector
from ray import Ray
from color import Color
from light import Light

from sphere import Sphere
from plane import Plane

from blinn import Blinn
from checker import Checker

import sys

# Background color
default_bg = Color(0, 0, 0, 255)
# Maximum raytraced reflections
max_depth = 5
# Color for past raytraced max
default_far = Color(127, 127, 127, 255)

class Raytracer:
	def __init__(self, scene_definition, progress_token):
		self.progress_token = progress_token
		
		# Parse camera
		camera_definition = scene_definition['camera']
		self.look_at = Vector(*camera_definition['look_at'])
		self.position = Vector(*camera_definition['position'])
		self.width = camera_definition['width']
		self.height = camera_definition['height']
		self.angle = camera_definition['angle'] * math.pi # expressed in increments of pi radians
		
		# Parse shaders
		self.shaders = {}
		shader_definition = scene_definition['shaders']
		for key in shader_definition:
			shader = shader_definition[key]
			shader_type = shader['type'].lower();
			shader_params = shader['params']
			if (shader_type == 'blinn'):
				self.shaders[key] = Blinn(shader_params)
			elif (shader_type == 'checker'):
				self.shaders[key] = Checker(shader_params)
			else:
				raise Exception('Unknown shader: %s' % shader_type)
		
		# Parse objects
		self.objects = []
		object_definition = scene_definition['objects']
		for object in object_definition:
			object_type = object['type'].lower();
			object_params = object['params']
			if (object_type == 'sphere'):
				self.objects.append(Sphere(object_params, self.shaders))
			elif (object_type == 'plane'):
				self.objects.append(Plane(object_params, self.shaders))
			else:
				raise Exception('Unknown object: %s' % object_type)
		
		# Parse lights
		self.lights = []
		light_definition = scene_definition['lights']
		for light_params in light_definition:
			self.lights.append(Light(light_params))
		
	def render(self):
		array = numpy.array(Image.new('RGBA', (self.width, self.height)))
		self.cast_rays(array)
	
		raw_img = Image.fromarray(array)

		output = StringIO.StringIO()
		raw_img.save(output, format="png")
		png_img = output.getvalue()
		output.close()
	
		return png_img
	
	def cast_rays(self, output):
		print(output.shape)
		
		v_forward = (self.look_at - self.position).normalize()
	
		magnitude_right = (self.look_at - self.position).magnitude() * math.tan(self.angle / 2)
		magnitude_up = magnitude_right * (float(self.height) / float(self.width))
	
		v_up = Vector(0.0, 0.0, 1.0).scale(magnitude_up)
		v_right = v_forward.cross(v_up).normalize().scale(magnitude_right);
	
		top_left = (self.look_at + v_up - v_right) - self.position
		
		sweep_down = v_up.scale(-2)
		sweep_right = v_right.scale(2)
		
		total_pixels = float(self.height * self.width);
		pixel_count = 0;
		
		for y in range(self.height):
			fraction_down = y / float(self.height - 1)
			for x in range(self.width):
				fraction_right = x / float(self.width - 1)
				ray = Ray(self.position, top_left + sweep_down.scale(fraction_down) + sweep_right.scale(fraction_right))
				color = self.trace_ray(ray, max_depth)
				output[y,x,0] = color.r
				output[y,x,1] = color.g
				output[y,x,2] = color.b
				output[y,x,3] = color.a
				
				if (pixel_count > 0 and pixel_count % 10000 == 0):
					self.progress_token.update(pixel_count / total_pixels)
				
				pixel_count += 1
			
		return output

	def best_intersect(self, ray):
		best_intersect = None
		for object in self.objects:
			intersect = object.intersect(ray)
			if (not intersect is None) and (best_intersect is None or intersect.distance < best_intersect.distance):
				best_intersect = intersect
		
		return best_intersect

	def test_ray(self, ray):
		best_intersect = self.best_intersect(ray)
		
		if best_intersect is None:
			return 0
		else:
			return best_intersect.distance

	def trace_ray(self, ray, depth):
		best_intersect = self.best_intersect(ray)
		
		if best_intersect is None:
			return default_bg
		else:
			return self.shade(best_intersect, depth)
	
	def shade(self, intersect, depth):
		intersect.prepare()
		
		color_result = default_bg
		color_result = color_result.alpha_blend(intersect.object.shader.shade_diffuse(self, intersect))
		
		if depth == 0:
			return color_result.alpha_blend(default_far)
		else:
			return color_result.alpha_blend(intersect.object.shader.shade_reflect(self, intersect, depth))