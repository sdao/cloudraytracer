from color import Color
from ray import Ray
import math

class BlinnBase:
	def shade_diffuse(self, raytracer, intersect):
		shaded = Color(0, 0, 0, 0)
		for light in raytracer.lights: # Figure out if actually illuminated by any lights
			light_dist = light.position - intersect.position
			light_vect = light_dist.normalize()
			test_light = raytracer.test_ray(Ray(intersect.position, light_vect))
			out_of_shadow = (test_light > light_dist.magnitude()) or (test_light == 0.0)
			if out_of_shadow:
				illum = light_vect.dot(intersect.normal)
				light_color = light.color.scale(illum) if illum > 0 else Color(0, 0, 0, 0)
				specular = intersect.reflect_ray.direction.dot(light_vect)
				specular_color = light.color.scale(math.pow(specular, self._roughness(intersect.position))) if specular > 0 else Color(0, 0, 0, 0)
				shaded = specular_color.multiply(self._specular(intersect.position)).alpha_blend(light_color.multiply(self._diffuse(intersect.position))).alpha_blend(shaded)
				
		return shaded
			
	def shade_reflect(self, raytracer, intersect, depth):
		return raytracer.trace_ray(intersect.reflect_ray, depth - 1).scale(self._reflect(intersect.position))
	
	def _diffuse(self, point):
		return Color(255, 255, 255, 255)
	
	def _specular(self, point):
		return Color(255, 255, 255, 255)
	
	def _reflect(self, point):
		return Color(255, 255, 255, 255)
	
	def _roughness(self, point):
		return 10