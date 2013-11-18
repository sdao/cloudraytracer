class ProgressToken:
	def __init__(self, render):
		self.render = render
	
	def update(self, progress):
		self.render.progress = progress
		self.render.put()