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

import pprint
import glob
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
		self.pp = pprint.PrettyPrinter(indent=4)

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
	def purge(self):
		""" Purge all cached data """
		data = { 'result' : 0, 'status' : "Unknown", 'removed' : []}
		
		files1 = glob.glob(settings.CACHE_DIR + '*.json', recursive=False)
		files2 = glob.glob(settings.CACHE_DIR + '*.jpg', recursive=False)
		
		print("MetadataServer.purge - Purging files")
		
		for f in files1:
			try:
				print("MetadataServer.purge - %s" % f)
				os.remove(f)
				data['removed'].append(f)
				data['result'] = 1
				data['status'] = "Ok"
			except Exception as e:
				data['result'] = 0
				data['status'] = "Error"
		
		print("MetadataServer.purge - Purged [files: %s]" % len(data['removed']))
		
		return(data)
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def platforms(self):
		""" Return a list of platforms """
		data = { 'result' : 0, 'status' : "Unknown", 'platforms' : []}
		
		platforms = self.mobygames.platforms()
		
		if platforms:
			data['result'] = len(platforms)
			data['status'] = "Ok"
			data['platforms'] = platforms
		
		return(data)
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def platformid(self, platform = ""):
		""" Return the id for a platforms """
		
		data = { 'result' : 0, 'status' : "Unknown", 'platform_id' : -1}
		
		params = cherrypy.request.params
		headers = cherrypy.request.headers
		
		if 'platform' not in params:
			data['status'] = "Invalid request"
			return(data)
		
		print("MetadataServer.platformid - Finding platform_id for [platform: %s]" % platform)
		
		platforms = self.mobygames.platforms()
		
		if platforms:
			data['result'] = 1
			data['status'] = "Ok"
			data['platform_id'] = -1
			for p in platforms:
				if params['platform'] == p['platform_name']:
					data['platform_id'] = p['platform_id']
					
		else:
			data['result'] = 0
			data['status'] = "Error"
	
		print("MetadataServer.platformid - Platform_id is %s" % data['platform_id'])
	
		return(data)
	
	@cherrypy.expose
	@cherrypy.tools.json_out()
	def find(self, **kwargs):
		""" Search for a given game in Mobygames and return a JSON dictionary of the results. """
		
		found_games = []
		data = { 'result' : 0, 'status' : "Unknown", 'games' : []}
		
		params = cherrypy.request.params
		headers = cherrypy.request.headers
		
		if 'title' not in params:
			data['status'] = "Invalid request"
			return(data)
		else:
			title = params['title']
			
		if 'platform' not in params:
			platform = ""
		else:
			platform = params['platform']

		print("MetadataServer.find - Finding games [title: %s] [platform: %s]" % (title, platform))

		platforms = self.mobygames.platforms()
		platform_id = ""
		for p in platforms:
			if platform.lower() == p['platform_name'].lower():
				platform_id = p['platform_id']
		
		data['title'] = params['title']
		data['platform_id'] = platform_id
		
		games = self.mobygames.find(title = title, platform_id = platform_id)
		if games:
			data['result'] = len(games)
			data['status'] = "Ok"		
			for g in games:
				new_game = {
					'moby_id' : g['game_id'],
					'title' : g['title'],
					'date' : ''
				}
				for p in g['platforms']:
					if p['platform_id'] == platform_id:
						new_game['date'] = p['first_release_date']
						
				#self.pp.pprint(g)
				if settings.DEBUG:
					print(new_game)
				found_games.append(new_game)
		else:
			data['status'] = "Error"
		
		print("MetadataServer.find - Found [games: %s]" % len(found_games))
		
		data['games'] = found_games
		return(data)


	@cherrypy.expose
	@cherrypy.tools.json_out()
	def getdata(self, **kwargs):
		""" Search for a given game in Mobygames and return a JSON dictionary of the results. """
		
		data = { 'result' : 0, 'status' : "Unknown"}
		
		params = cherrypy.request.params
		headers = cherrypy.request.headers
		
		if 'moby_id' not in params:
			data['status'] = "Invalid request"
			return(data)
		else:
			moby_id = params['moby_id']
			
		if 'platform' not in params:
			platform = ""
		else:
			platform = params['platform']
		
		platforms = self.mobygames.platforms()
		platform_id = ""
		for p in platforms:
			if platform.lower() == p['platform_name'].lower():
				platform_id = p['platform_id']
		
		game = self.mobygames.game(moby_id)
		game_platform = self.mobygames.gameforplatform(moby_id, platform_id)
		
		if game_platform and game:
			data['result'] = 1
			data['status'] = "Ok"
			data['moby_id'] = moby_id
			data['platform'] = game_platform['platform_name']
			data['year'] = game_platform['first_release_date']
			data['name'] = game['title']
			data['publisher'] = self.mobygames.getPublisherFromData(game_platform)
			data['developer'] = self.mobygames.getDeveloperFromData(game_platform)
			data['genre'] = self.mobygames.getGenreFromData(game)
			data['min_cpu'] = self.mobygames.getCPUFromData(game_platform)
			data['min_ram'] = self.mobygames.getRAMFromData(game_platform)
			data['video'] = self.mobygames.getVideoFromData(game_platform)
			data['beeper'] = self.mobygames.hasBeeper(game_platform)
			data['fm'] = self.mobygames.hasFM(game_platform)
			data['midi'] = self.mobygames.hasMIDI(game_platform)
			data['digifx'] = self.mobygames.hasDigiFX(game_platform)
			data['rating'] = game['moby_score']
			
			if settings.DEBUG:
				#self.pp.pprint(game)
				#print(game_platform)
				#print("")
				self.pp.pprint(data)
				print("")
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