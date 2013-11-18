class Color:
	def __init__(self, r, g, b, a):
		self.r = r
		self.g = g
		self.b = b
		self.a = a
	
	def __str__(self):
		return "R %d; G %d; B %d; A %d" % (self.r, self.g, self.b, self.a)
	
	def alpha_blend(self, source):
		a_dest = self.a / 255.0
		a_src = source.a / 255.0
		r_dest = self.r / 255.0
		r_src = source.r / 255.0
		g_dest = self.g / 255.0
		g_src = source.g / 255.0
		b_dest = self.b / 255.0
		b_src = source.b / 255.0
		
		a_src_inv = 1.0 - a_src
		
		a_out = a_src + a_dest * a_src_inv
		
		r_out = 0.0
		g_out = 0.0
		b_out = 0.0
		
		if a_out != 0.0:
			r_out = min((r_src * a_src + r_dest * a_dest * a_src_inv) / a_out, 1.0)
			g_out = min((g_src * a_src + g_dest * a_dest * a_src_inv) / a_out, 1.0)
			b_out = min((b_src * a_src + b_dest * a_dest * a_src_inv) / a_out, 1.0)
		
		return Color(int(r_out * 255), int(g_out * 255), int(b_out * 255), int(a_out * 255))
	
	def scale(self, k):
		return Color(min(self.r * k, 255), min(self.g * k, 255), min(self.b * k, 255), min(self.a * k, 255))
	
	def multiply(self, other):
		return Color(self.r * other.r / 255, self.g * other.g / 255, self.b * other.b / 255, self.a * other.a / 255)