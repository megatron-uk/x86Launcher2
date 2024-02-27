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

import json
import requests
import settings

BASE_URL = "https://api.mobygames.com/v1/"

class Mobygames():
	
	def __init__(self):
		self.api_key = settings.MOBYGAMES_API_KEY
		if self.api_key:
			print("Mobygames.__init__ - Loaded API key")
	
	def moby_url(self, url = ""):
		return BASE_URL + url + "?api_key=" + self.api_key
	
	def get(self, url):
		""" Makes a request on behalf of another function """
		
		print("Mobygames.get - Calling: %s" % url)
		r = requests.get(url)
		print("Mobygames.get - [%s]" % r.status_code)
		if (r.status_code != 200):
			return False
		
		data = r.json()
		if settings.DEBUG:
			print("Mobygames.get - Returned [%s] bytes " % len(r.text))
			
		return data
	
	def platforms(self):
		""" Get a list of all platforms and their ids in the Mobygames database """
		
		print("Mobygames.platforms - Getting platform list")
		
		url = self.moby_url("platforms")
		data = self.get(url)
		if 'platforms' in data.keys():
			if settings.DEBUG:
				for p in data['platforms']:
					print("Mobygames.platforms - %s: %s" % (p['platform_name'], p['platform_id']))
			return data['platforms']
		else:
			return False
	
	