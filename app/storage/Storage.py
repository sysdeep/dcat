#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import shutil
import time


from app import log
from app.lib import dbus


from .DB import DB
from .enums import FRow, VRow, FType
from . import finder


class Storage(object):
	def __init__(self):

		self.storage_path = None
		self.db = DB()
		self.is_open = False

		self.volumes = []
		self.files = []


	def open_storage(self, file_path):
		log.info("open storage: " + file_path)
		self.storage_path = file_path
		self.db.open_db(self.storage_path)
		self.is_open = True
		# self.__load_storage()

		


	def close_storage(self):
		self.db.close_db()
		self.volumes = []
		self.files = []
		self.is_open = False


	def create_storage(self, file_path):
		log.info("создание базы: " + file_path)
		if self.is_open:
			self.close_storage()

		self.storage_path = file_path
		self.db.create_db(self.storage_path)
		self.is_open = True

	
	


	def fetch_system(self):
		return self.db.get_system()


	def fetch_volumes(self):
		log.debug("fetch volumes")
		if not self.is_open:
			return []

		volumes = self.db.get_volumes()

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


	def remove_volume(self, volume_uuid):
		if not self.is_open:
			return False

		self.db.remove_volume_files(volume_uuid)
		self.db.remove_volume(volume_uuid)

		return True






	# def __load_files(self, volume=None):
	# 	if not self.is_open:
	# 		return []
	#
	# 	if volume:
	# 		files = self.db.get_volume_files(volume)
	# 	else:
	# 		files = self.db.get_files_all()
	#
	#
	# 	return files

	



	def create_volume_row(self, vdata, commit=False):
		volume_id = self.db.create_volume_row(vdata, commit)
		return volume_id


	def create_file_row(self, fdata, commit=False):
		file_id = self.db.create_file_row(fdata, commit)
		return file_id

	def update_volume_row(self, vdata, commit=False):
		self.db.update_volume_row(vdata, commit)

		dbus.emit(dbus.STORAGE_VOLUME_UPDATED, vdata["uuid"])


	def commit(self):
		self.db.commit()


	def get_volumes(self):
		return self.volumes

	def get_files(self):
		return self.files


	def find_childrens(self, parent_id):
		result = [file for file in self.files if file[FRow.PARENT] == parent_id]
		return result

	def find_volume_items(self, volume_id, parent_id):
		result = [file for file in self.files if (file[FRow.PARENT] == parent_id) and (file[FRow.VOLUME] == volume_id)]
		return result



	def find_items(self, term, is_file=True, is_folder=False):

		pre_fnodes = self.db.find_by_name(term)

		fnodes = []
		for fnode in pre_fnodes:
			if is_file and fnode.is_file():
				fnodes.append(fnode)

			if is_folder and fnode.is_dir():
				fnodes.append(fnode)

		pre_fnodes = None

		result = finder.find_top_items(self.db, fnodes)

		return result


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