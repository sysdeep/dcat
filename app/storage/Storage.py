#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import shutil
import time

from app import log
from app.lib import dbus

from .DB import DB
from . import sbus
from . import finder
from . import cache
from . import defs
from .export import ejson, evolume



class Storage(object):
	def __init__(self):

		self.storage_path = None
		self.db = DB()
		self.is_open = False


		#--- прослушка событий
		sbus.eon(sbus.DB_COMMITTED, self.__on_db_committed)
		sbus.eon(sbus.DB_MIGRATED, self.__on_db_migrated)



	#--- db file actions ------------------------------------------------------
	def open_storage(self, file_path):
		"""открытие базы"""
		log.info("open storage: " + file_path)
		self.storage_path = file_path
		self.db.open_db(self.storage_path)
		self.is_open = True

		self.load_system()
		sbus.emit(sbus.STORAGE_OPENED)




	def close_storage(self):
		"""закрытие базы"""
		self.db.close_db()
		cache.clear_volumes()
		self.is_open = False

		sbus.emit(sbus.STORAGE_CLOSED)


	def create_storage(self, file_path):
		"""создание базы"""
		log.info("создание базы: " + file_path)
		if self.is_open:
			self.close_storage()

		self.storage_path = file_path
		self.db.create_db(self.storage_path)
		self.is_open = True

		self.load_system()
		sbus.emit(sbus.STORAGE_CREATED)


	def commit(self):
		"""принудительная запись базы"""
		self.db.commit()
	#--- db file actions ------------------------------------------------------
	
	




	#--- получение элементов --------------------------------------------------
	# def fetch_system(self):
	# 	"""получить системную информацию из базы"""
	# 	return self.db.get_system()


	def load_system(self):
		"""загрузить данные по базе в кэш"""
		system_info = self.db.get_system()
		system_data = {}
		for row in system_info:
			system_data[row["key"]] = row["value"]

		cache.set_system(system_data)

	def get_system_value(self, key):
		"""получить тек. значение системной информации"""
		system_data = cache.get_system()
		return system_data.get(key, "not found")

	def get_system_info(self):
		"""получить все данные по системной информации"""
		return cache.get_system()







	def fetch_volumes(self, iscache=False):
		"""получить список томов
			:param	iscache	[bool]		- флаг выбора томов из текущего кэша, а не из базы
			:returns	[vnode]
		"""

		#--- если флаг из кэша - возвращаем данные из кэша
		if iscache:
			log.debug("fetch volumes - cache")
			return cache.get_volumes()

		log.debug("fetch volumes")
		if not self.is_open:
			return []

		volumes = self.db.get_volumes()
		cache.set_volumes(volumes)

		return volumes
		

	def fetch_volume_files(self, volime_id):
		log.debug("fetch volume files")
		if not self.is_open:
			return []

		files = self.db.get_volume_root_files(volime_id)
		return files


	def fetch_parent_files(self, parent_id):
		log.debug("fetch files")
		if not self.is_open:
			return []

		files = self.db.get_parent_files(parent_id)
		return files





	def find_items(self, term, is_file=True, is_folder=False, volume_id=None):
		"""поиск элементов по заданным пареметрам, дополнительно рекурсивно строится полный путь"""

		pre_fnodes = self.db.find_by_name(term, volume_id)

		fnodes = []
		for fnode in pre_fnodes:
			if is_file and fnode.is_file():
				fnodes.append(fnode)

			if is_folder and fnode.is_dir():
				fnodes.append(fnode)

		pre_fnodes = None

		result = finder.find_top_items(self.db, fnodes)

		return result
	#--- получение элементов --------------------------------------------------








	#--- удаление элементов ---------------------------------------------------
	def remove_volume(self, volume_uuid):
		"""удаление тома"""
		if not self.is_open:
			return False

		self.db.remove_volume_files(volume_uuid)
		self.db.remove_volume(volume_uuid)

		return True
	#--- удаление элементов ---------------------------------------------------







	#--- создание элементов ---------------------------------------------------
	def create_volume_row(self, vdata, commit=False):
		volume_id = self.db.create_volume_row(vdata, commit)
		return volume_id


	def create_file_row(self, fdata, commit=False):
		file_id = self.db.create_file_row(fdata, commit)
		return file_id
	#--- создание элементов ---------------------------------------------------









	#--- обновление элементов -------------------------------------------------
	def update_volume_row(self, vdata, commit=False):
		self.db.update_volume_row(vdata, commit)

		sbus.emit(sbus.STORAGE_VOLUME_UPDATED, vdata["uuid"])


	def update_system(self, key, value):
		"""обновление заданной системной переменной(вместе с кэшем)"""
		self.db.update_system(key, value)
		system_data = cache.get_system()
		system_data[key] = value
		cache.set_system(system_data)
	#--- обновление элементов -------------------------------------------------




	#--- aliaces --------------------------------------------------------------
	def get_db_version(self):
		"""получить версию открытой базы"""
		return self.get_system_value(defs.SYS_KEY_VERSION)
	#--- aliaces --------------------------------------------------------------



	#--- сервис ---------------------------------------------------------------
	def create_current_backup(self):
		# print("create_current_backup")

		if self.is_open is False:
			return False


		# print(self.storage_path)

		base_name = os.path.splitext(self.storage_path)
		# print(base_name)

		new_backup_name = base_name[0] + "_" + str(int(time.time())) + base_name[1]
		# print(new_backup_name)


		try:
			shutil.copyfile(self.storage_path, new_backup_name)
		except:
			log.exception("unable copy file for backup...")


	def export_volume(self, volume_id, export_file_path):
		log.debug("export volume - " + volume_id)
		log.debug("export path - " + export_file_path)

		#--- sysinfo
		sys_info = self.get_system_info()
		sys_info["sorage_path"] = self.storage_path

		#--- volume info
		vnode = self.db.get_volume(volume_id)
		volume_info = vnode.make_data_dict()


		#--- files
		files = []
		fnodes = self.fetch_volume_files(volume_id)
		for fnode in fnodes:
			result = fnode.make_data_dict()
			files.append(result)


		result = evolume.export(sys_info, volume_info, files, export_file_path)
		if result:
			dbus.emit(dbus.SHOW_EXPORT_VOLUME_OK)
		else:
			dbus.emit(dbus.SHOW_EXPORT_VOLUME_ERR)






	def export_db(self, file_name_path, format="json"):
		ejson.add_db_info("qqq")


		volumes = self.fetch_volumes()


		for vnode in volumes:
			files = self.db.get_volume_all_files(vnode.uuid)
			vnode.files = files

			ejson.add_volume(vnode, files)


		ejson.make(file_name_path)
	#--- сервис ---------------------------------------------------------------



	#--- events ---------------------------------------------------------------
	def __on_db_committed(self):
		"""событие от базы - запись изменений в файл"""

		#--- обновляем данные в кэше - время изменения базы
		updated_timestamp = self.db.get_system_value(defs.SYS_KEY_UPDATED)
		system_cache = cache.get_system()
		system_cache[defs.SYS_KEY_UPDATED] = updated_timestamp
		cache.set_system(system_cache)


	def __on_db_migrated(self):
		"""событие от базы - произошла миграция"""

		#--- обновляем данные в кэше - версия базы
		version = self.db.get_system_value(defs.SYS_KEY_VERSION)
		system_cache = cache.get_system()
		system_cache[defs.SYS_KEY_VERSION] = version
		cache.set_system(system_cache)

	#--- events ---------------------------------------------------------------