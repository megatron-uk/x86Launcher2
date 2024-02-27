#!/usr/bin/env python3

"""
A metadata and proxy server for x86Launcher2:
https://github.com/megatron-uk/x86Launcher2

Copyright (C) 2024 John Snowdon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import cherrypy
import jinja2
import settings
from mobygames import Mobygames

class ReportLoader(jinja2.BaseLoader):
	""" A basic template loader for Jinja2 template files """
	
	def __init__(self, path):
		self.path = settings.TEMPLATE_DIR
	
	def get_source(self, environment, template):
		""" We just add the template name onto TEMPLATE_DIR from settings """
		
		path = os.path.join(self.path, template)
		if not os.path.exists(path):
			raise jinja2.TemplateNotFound(template)
		mtime = os.path.getmtime(path)
		with open(path) as f:
			source = f.read()
		return source, path, lambda: mtime == os.path.getmtime(path)

class MetadataServer(object):
	""" This is the real server code here.
		We only respond to a small number of GET requests:
		
		GET / or GET /index
			- Responds with a basic index page describing the server.
			
		GET /find?title=foo&platform=1
			- Returns a list of matching game titles from Mobygames
				
	"""
	
	def __init__(self):
		self.mobygames = Mobygames()

	@cherrypy.expose
	def index(self):
		""" Generate an index page. """
		template_file = "index.html"
		env = jinja2.Environment(loader=ReportLoader(settings.APP_NAME), autoescape=jinja2.select_autoescape())
		template = env.get_template(template_file)
		html_file = template.render()
		
		return(html_file)
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def platforms(self):
		""" Return a list of platforms """
		data = { 'result' : 0, 'status' : "Unknown", 'platforms' : []}
		
		platforms = self.mobygames.platforms()
		
		if platforms:
			data['result'] = 1
			data['status'] = "Ok"
			data['platforms'] = platforms
		
		return(data)
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def find(self, **kwargs):
		""" Search for a given game in Mobygames and return a JSON dictionary of the results. """
		
		data = { 'result' : 0, 'status' : "Unknown", 'games' : []}
		
		params = cherrypy.request.params
		headers = cherrypy.request.headers
		
		if 'title' not in params:
			data['status'] = "Invalid request"
			return(data)
		
		data['title'] = params['title']
		
		return(data)


if __name__ == "__main__":
	
	# Server config
	cherrypy.config.update(
		{
			'server.socket_host': settings.SERVER_HOST,
			'server.socket_port': settings.SERVER_PORT,
			'engine.autoreload_on': True,
		}
	)
	
	# Static content mapping
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/css':
		{ 
			'tools.staticdir.on':True,
			'tools.staticdir.dir': settings.CSS_DIR
		},
		'/js':
		{ 
			'tools.staticdir.on':True,
			'tools.staticdir.dir': settings.JS_DIR
		},
	}
	
	# Start the server
	cherrypy.quickstart(MetadataServer(), '/', conf)