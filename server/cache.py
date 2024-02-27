#!/usr/bin/env python3

"""
An on-disk persistent cache tool for x86Launcher2:
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

import json
import os
import settings

def isCached(key = "", js = True):
	""" Check if a given file, of name 'key' is present in the cache directory """
	if os.path.isfile(settings.CACHE_DIR + key):
		if os.path.getsize(settings.CACHE_DIR + key) > 0:
			if settings.DEBUG:
				print("isCached - HIT %s" % key)
			return True
	
	if settings.DEBUG:
		print("isCached - MISS %s" % key)
	return False

def getCached(key = "", js = True):
	""" Return a cached file from the cache directory """

	try:
	
		if settings.DEBUG:
			print("getCached - LOAD %s" % key)
		
		if json:
			f = open(settings.CACHE_DIR + key)
			data = json.loads(f.read())
			f.close()
			return data
			
		else:
			f = open(settings.CACHE_DIR + key)
			data = f.read()
			f.close()
			return data
	except Exception as e:
		print("getCached - Exception loading cache entry %s" % key)
		print("getCached - Error was: %s" % e)
		return False


def putCached(key = "", js = True, data = False):
	""" Put a file in the cache directory """
	
	if settings.DEBUG:
		print("putCached - STORE %s" % key)
	
	if isCached(key = key, js = js):
		os.remove(key)
	
	f = open(settings.CACHE_DIR + key, "w")
	
	if json:
		f.write(json.dumps(data))
	else:
		f.write(data)	
	
	f.close()
	
	return True