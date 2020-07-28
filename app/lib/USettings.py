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
MAX_LAST_BASES = 50


class USettings(object):
	"""
		хранилище настроек
		набор настроек хранится в словаре data

		при загрузке конфига происходит перетерание ключей словаря data, тем самым - мы не боимся добавлять переменные в код
	"""
	# EV_SAVED = "EV_SAVED"
	# EV_OPENED = "EV_OPENED"
	def __init__(self):
		self.settings_path = self.__make_os_file_path()
		self.file_path = os.path.join(self.settings_path, SETINGS_FILE)


		self.data = {
			"version" 			: "0.1",
			"lastbases" 		: [],
			"open_last"			: 1,
			"max_last_bases"	: MAX_LAST_BASES,			# кол-во сохранённых баз


			# "style"			: "clam"
		}

		self.__check_path()

		

	@property
	def is_open_last(self):
		return self.data.get("open_last", 0)

	@is_open_last.setter
	def is_open_last(self, value):
		self.data["open_last"] = value



	def clear_lastbases(self):
		self.data["lastbases"] = []
		self.save()


	def save(self):
		with open(self.file_path, "w", encoding="utf-8") as fd:
			fd.write(json.dumps(self.data, indent=4))


	def open_settings(self):
		"""загрузка данных из конфига"""
		with open(self.file_path, "r", encoding="utf-8") as fd:
			fcontent = fd.read()
			settings_data = json.loads(fcontent)

			#--- обновляем все ключи данных
			for key, value in settings_data.items():
				self.data[key] = value




	def update_last_base(self, value):
		"""
			обновление списка последних баз. 
				если база есть в списке - удалем её и добавляем в конец
				если кол-во записей больше максимального - очищаем старые
			Args:
				value 	[string] - путь до базы
		"""

		#--- уже сущ. - ничего не делаем
		if value in self.data["lastbases"]:
			return False
			# self.data["lastbases"].remove(value)

		#--- проверяем на переполнение
		# if len(self.data["lastbases"]) > self.data["max_last_bases"]:
		if len(self.data["lastbases"]) > MAX_LAST_BASES:
			self.data["lastbases"].pop()

		#--- добавляем
		self.data["lastbases"].append(value)

		self.save()



	def get_last_base(self):
		if len(self.data["lastbases"]) > 0:
			return self.data["lastbases"][-1]
		return None


	def remove_last(self, item):
		if item in self.data["lastbases"]:
			self.data["lastbases"].remove(item)
			self.save()



	def __make_os_file_path(self):
		if sys.platform == 'win32':
			# print(os.environ['APPDATA'])
			return os.path.join(os.environ['APPDATA'], APP_NAME)
		else:
			return os.path.expanduser(os.path.join("~", "." + APP_NAME))


	def __check_path(self):
		if not os.path.exists(self.settings_path):
			os.mkdir(self.settings_path)
			self.save()




	def check_bases_exists(self):
		"""проверка на существование баз в истории"""
		dbs = []
		need_update = False
		for item in self.data["lastbases"]:
			if os.path.exists(item):
				dbs.append(item)
			else:
				need_update = True

		self.data["lastbases"] = dbs

		#--- если одна из баз не существует - тогда обновляем конфиг
		if need_update:
			self.save()

	
	#--- events ---------------------------------------------------------------
	# def connect(self, ev, handler):
	# 	pass
	#
	# def disconnect(self, ev, handler):
	# 	pass
	#--- events ---------------------------------------------------------------




if __name__ == "__main__":


	s = USettings()
	s.open_settings()
	print(s.data)