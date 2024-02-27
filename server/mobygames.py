#!/usr/bin/env python3

"""
Wrappers around the Mobygames API for Python.

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

import urllib
import json
import requests
from cache import isCached, getCached, putCached
import settings

BASE_URL = "https://api.mobygames.com/v1/"

class Mobygames():
	
	def __init__(self):
		self.api_key = settings.MOBYGAMES_API_KEY
		if self.api_key:
			print("Mobygames.__init__ - Loaded API key")
			self.api_key = urllib.parse.quote_plus(self.api_key)
	
	def moby_url(self, url = ""):
		return url
	
	def get(self, url):
		""" Makes a request on behalf of another function """
		
		new_url = BASE_URL + url + "&api_key=" + self.api_key
		print("Mobygames.get - Calling: %s" % (new_url))
		r = requests.get(new_url)
		print("Mobygames.get - [%s]" % r.status_code)
		if (r.status_code != 200):
			print("Mobygames.get - Error retrieving page!")
			print(r.text)
			return False
		
		data = r.json()
		if settings.DEBUG:
			print("Mobygames.get - Returned [%s] bytes " % len(r.text))
			
		return data
	
	############################################
	
	def getPublisherFromData(self, data):
		""" Extract the publisher - G.T. Interactive, Inc. - from a game data block as returned by self.get() """
		
		if 'releases' in data.keys():
			for release in data['releases']:
				if 'companies' in release.keys():
					for company in release['companies']:
						if company['role'] == 'Published by':
							return(company['company_name'])
		
		return("")
	
	def getDeveloperFromData(self, data):
		""" Extract the developer - I.D Software, Inc. - from a game data block as returned by self.get() """
		
		if 'releases' in data.keys():
			for release in data['releases']:
				if 'companies' in release.keys():
					for company in release['companies']:
						if company['role'] == 'Developed by':
							return(company['company_name'])
		
		return("")
	
	def hasBeeper(self, data):
		""" Does the game support PC speaker """
		
		if 'attributes' in data.keys():
			for a in data['attributes']:
				if a['attribute_category_id'] == 1:
					# Attribute no.1 looks like this, and there may be more than one:
					#{
					#	'attribute_category_id': 1,
					#	'attribute_category_name': 'Sound Devices Supported',
					#	'attribute_id': xxxx,
					#	'attribute_name': 'PC Speaker'
					#}
					if a['attribute_name'] == 'PC Speaker':
						return(1)
		
		return(0)
	
	def hasFM(self, data):
		""" Does the game support FM synthesis audio of any type """
		
		return("")
		
	def hasDigiFX(self, data):
		""" Does the game support Digital audio of any type """
		
		return("")
		
	def hasMIDI(self, data):
		""" Does the game support MIDI music of any type """
		
		return("")

	def getGenreFromData(self, data):
		""" Extract the primary genre - Shooter/Adventure/etc - from a game data block as returned by self.get() """
		
		if 'genres' in data.keys():
			for g in data['genres']:
				if g['genre_category_id'] == 1:
					# Genre no.1 looks like this:
					#{	'genre_category': 'Basic Genres',
					#	'genre_category_id': 1,
					#	'genre_id': 5,
					#	'genre_name': 'Sports'
					#},
					return(g['genre_name'])
		
		return("")
	
	def getCPUFromData(self, data):
		""" Extract the minimum cpu requirement - Intel 386DX/etc - from a game data block as returned by self.get() """
		
		if 'attributes' in data.keys():
			for a in data['attributes']:
				if a['attribute_category_id'] == 11:
					# Attribute no.11 looks like this:
					#{
					#	'attribute_category_id': 11,
					#	'attribute_category_name': 'Minimum CPU Class '
					#                                'Required',
					#	'attribute_id': xxxx,
					#	'attribute_name': 'Intel i386'
					#}
					return(a['attribute_name'])
		
		return("")
	
	def getRAMFromData(self, data):
		""" Extract the minimum RAM requirement - 640KB/4 MB/etc - from a game data block as returned by self.get() """
		
		if 'attributes' in data.keys():
			for a in data['attributes']:
				if a['attribute_category_id'] == 15:
					# Attribute no.15 looks like this:
					#{
					#	'attribute_category_id': 15,
					#	'attribute_category_name': 'Minimum RAM Required',
					#	'attribute_id': xxxx,
					#	'attribute_name': '4 MB'
					#}
					return(a['attribute_name'])
		
		return("")
	
	def getVideoFromData(self, data):
		""" Extract the supported video modes/type - CGA/EGA/VGA/etc - from a game data block as returned by self.get() """
		
		video_modes = []
		
		if 'attributes' in data.keys():
			for a in data['attributes']:
				if a['attribute_category_id'] == 2:
					# Attribute no.2 looks like this, and there may be more than one:
					#{
					#	'attribute_category_id': 2,
					#	'attribute_category_name': 'Video Modes Supported',
					#	'attribute_id': xxxx,
					#	'attribute_name': 'VGA (Tweaked)'
					#}
					video_modes.append(a['attribute_name'])
		
		if len(video_modes) > 1:
			return("Multiple video modes")
		
		if len(video_modes) == 1:
			return(video_modes[0])
		
		return("")
	
	#############################################
	
	def platforms(self):
		""" Get a list of all platforms and their ids in the Mobygames database """
		
		key = "platforms.json"
		
		print("Mobygames.platforms - Getting platform list")
		
		if isCached(key):
			data = getCached(key)
			return data
		
		url = self.moby_url("platforms")
		data = self.get(url)
		if data:
			if 'platforms' in data.keys():			
				putCached(key = key, data = data['platforms'])
				return data['platforms']
		else:
			return False
	
	def find(self, title, platform_id):
		""" Find one or more matches against a partial game title for a platform """
		
		key = "find_title_" + title + "_platform_" + str(platform_id) + ".json"
		
		print("Mobygames.find - Finding game matches [title: %s] [platform: %s]" % (title, platform_id))
		
		if isCached(key):
			data = getCached(key)
			return data
		
		url = self.moby_url("games")
		url = url + "?title=" + urllib.parse.quote_plus(title)
		if len(str(platform_id)) > 0:
			url = url + "&platform=" + urllib.parse.quote_plus(str(platform_id))
		data = self.get(url)
		if data:
			if 'games' in data.keys():			
				putCached(key = key, data = data['games'])
				return data['games']
		else:
			return False
			
	def game(self, moby_id):
		""" Return metadata for a single game object """
		
		key = "get_" + str(moby_id) + ".json"
		
		print("Mobygames.game - Get metadata for game [moby_id: %s]" % (moby_id))
		
		if isCached(key):
			data = getCached(key)
			return data
			
		url = self.moby_url("games")
		url = url + "/" + urllib.parse.quote_plus(moby_id)
		data = self.get(url)
		if data:
			if 'game_id' in data.keys():			
				putCached(key = key, data = data)
				return data
		else:
			return False
			
	def gameforplatform(self, moby_id, platform_id):
		""" Return metadata for a single game object on a single platform"""
		
		key = "get_" + str(moby_id) + "_platform_" + str(platform_id) + ".json"
		
		print("Mobygames.gameforplatform - Get metadata for game [moby_id: %s] [platform: %s]" % (moby_id, platform_id))
		
		if isCached(key):
			data = getCached(key)
			return data
			
		url = self.moby_url("games")
		url = url + "/" + urllib.parse.quote_plus(moby_id)
		if len(str(platform_id)) > 0:
			url = url + "/platforms/" + urllib.parse.quote_plus(str(platform_id))
		data = self.get(url)
		if data:
			if 'game_id' in data.keys():			
				putCached(key = key, data = data)
				return data
		else:
			return False