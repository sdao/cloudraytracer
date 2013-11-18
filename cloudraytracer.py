import os
import urllib
import ast
from datetime import datetime

from google.appengine.api import taskqueue
from google.appengine.ext import db
from google.appengine.api import images

from progresstoken import ProgressToken
from raytracer import Raytracer
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'])

class Render(db.Model):
	progress = db.FloatProperty(required=True)
	date = db.DateTimeProperty(required=True)
	script = db.TextProperty(required=False)
	image = db.BlobProperty(required=False)
	status = db.StringProperty(required=False)

class MainPage(webapp2.RequestHandler):
	def get(self):
		query = Render.all().order('-date');
		
		template_values = {
			'renders': [
			]
		}
		
		for r in query.run():
			template_values['renders'].append({
				'image': webapp2.uri_for('renderImage', id=r.key().id()) if r.progress == 1.0 else None,
				'id': webapp2.uri_for('renderConfirm', id=r.key().id()),
				'progress': r.progress,
				'status': r.status
			})

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

class RenderPage(webapp2.RequestHandler):
	def post(self):
		render_script = self.request.get('script')
		
		r = Render(progress=0.0, script=render_script, date=datetime.utcnow(), status="Waiting")
		key = r.put()
		
		taskqueue.add(url=webapp2.uri_for('renderWorker'), queue_name='render-queue', params={'id': key.id()});
		
		return self.redirect_to('renderConfirm', id=key.id())

class ConfirmPage(webapp2.RequestHandler):
	def get(self, id):
		render = Render.get_by_id(int(id))
		template_values = {
			'render_id': id,
			'render_progress': render.progress,
			'render_script': render.script,
			'render_status': render.status,
			'render_image': webapp2.uri_for('renderImage', id=render.key().id()) if render.progress == 1.0 else None,
		}
		template = JINJA_ENVIRONMENT.get_template('render.html')
		self.response.write(template.render(template_values))

class RenderWorker(webapp2.RequestHandler):
	def post(self):
		render_id = self.request.get('id')
		render = Render.get_by_id(int(render_id))
		
		if render:
			render.status = "Started"
			render.put()
			
			try:
				progress_token = ProgressToken(render)
				
				render_def = ast.literal_eval(render.script)
				tracer = Raytracer(render_def, progress_token)
				render_out = tracer.render()
				
				datetime_now = datetime.utcnow()
				time_diff = datetime_now - render.date
				
				render.image = db.Blob(render_out)
				render.progress = 1.0
				render.status = "Finished (%s)" % time_diff
			except SyntaxError:
				render.status = "Syntax error"
			except:
				render.status = "Unknown error"
			
			render.put()
		
class ImagePage(webapp2.RequestHandler):
	def get(self, id):
		render = Render.get_by_id(int(id))
		
		if render:
			self.response.headers['Content-Type'] = 'image/png'
			self.response.out.write(render.image)
		
application = webapp2.WSGIApplication([
	webapp2.Route(r'/', handler=MainPage, name='root'),
	webapp2.Route(r'/render', handler=RenderPage, name='render'),
	webapp2.Route(r'/render/<id>', handler=ConfirmPage, name='renderConfirm'),
	webapp2.Route(r'/renderWorker', handler=RenderWorker, name='renderWorker'),
	webapp2.Route(r'/image/<id>.png', handler=ImagePage, name='renderImage')
], debug=True)