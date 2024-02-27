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

try:
	import localsettings
except:
	print("No localsettings.py found!")
	print("Please create the text file 'localsettings.py' and add the following entry:")
	print("MOBYGAMES_API_KEY = your_mobygames_api_key")
	print("... and substitute your real mobygames_api_key!")
	print("")

APP_NAME = "x86Launcher2 Metadata Server"
TEMPLATE_DIR = "./templates/"
CSS_DIR = "./css/"
JS_DIR = "./js/"
DEBUG = True
SERVER_PORT = 8080
SERVER_HOST = "0.0.0.0"

# You must set this to your own personal API key.
# See: https://www.mobygames.com/info/api/
# We set it in localsettings.py so that it does not
# get committed to the Git repo.
MOBYGAMES_API_KEY = localsettings.MOBYGAMES_API_KEY

# The number of entries in the local, persistent cache.
CACHE_SIZE = {
	'queries'	: 512,		# Search results to cache
	'covers'	: 512,		# Full size cover/gamebox images to cache
	'screens'	: 1024,		# Full size screenshot images to cache
}
CACHE_DIR = "./cache/"