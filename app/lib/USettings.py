#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
if sys.platform == 'darwin':
	from AppKit import NSSearchPathForDirectoriesInDomains
	# http://developer.apple.com/DOCUMENTATION/Cocoa/Reference/Foundation/Miscellaneous/Foundation_Functions/Reference/reference.html#//apple_ref/c/func/NSSearchPathForDirectoriesInDomains
	# NSApplicationSupportDirectory = 14
	# NSUserDomainMask = 1
	# True for expanding the tilde into a fully qualified path
	appdata = path.join(NSSearchPathForDirectoriesInDomains(14, 1, True)[0], APPNAME)
elif sys.platform == 'win32':
	appdata = path.join(environ['APPDATA'], APPNAME)
else:
	appdata = path.expanduser(path.join("~", "." + APPNAME))
"""
import json
import sys
import os

APP_NAME = "dcat"
SETINGS_FILE = "settings.json"



class USettings(object):
	def __init__(self):
		self.settings_path = self.__make_os_file_path()
		self.file_path = os.path.join(self.settings_path, SETINGS_FILE)


		self.data = {
			"version" 		: "0.1",
			"lastbases" 	: [],
			"open_last"		: 1
		}

		self.__check_path()

		



	def save(self):
		with open(self.file_path, "w", encoding="utf-8") as fd:
			fd.write(json.dumps(self.data, indent=4))


	def open_settings(self):
		with open(self.file_path, "r", encoding="utf-8") as fd:
			fcontent = fd.read()
			self.data = json.loads(fcontent)



	def __make_os_file_path(self):
		if sys.platform == 'win32':
			return os.path.join(environ['APPDATA'], APP_NAME)
		else:
			return os.path.expanduser(os.path.join("~", "." + APP_NAME))


	def __check_path(self):
		if not os.path.exists(self.settings_path):
			os.mkdir(self.settings_path)
			self.save()



	

if __name__ == "__main__":


	s = USettings()
	s.open_settings()
	print(s.data)