#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import time

from app import log

from . import migrations
from . import sql
# from . import models
from .models import loader



VERSION = "2"

def now_date():
	return time.strftime("%Y-%m-%d %H:%M:%S")

# def make_volume(volume_data):
# 	vnode = models.VNode()
# 	vnode.uuid = volume_data["uuid"]
# 	vnode.name = volume_data["name"]
# 	vnode.vtype = volume_data["vtype"]
# 	vnode.path = volume_data["path"]
# 	vnode.created = volume_data["created"]
# 	return vnode


# def make_volumes(volumes_array):
# 	result = []
# 	for volume_data in volumes_array:
# 		result.append(make_volume(volume_data))

# 	return result



# def make_fnode(file_data):
# 	fnode = models.FNode()
# 	fnode.uuid = file_data["uuid"]
# 	fnode.volume_id = file_data["volume_id"]
# 	fnode.parent_id = file_data["parent_id"]
# 	fnode.name = file_data["name"]
# 	fnode.size = file_data["size"]
# 	fnode.ctime = file_data["ctime"]
# 	fnode.ftype = file_data["type"]
# 	return fnode


# def make_fnodes(files_array):
# 	result = []
# 	for file_data in files_array:
# 		result.append(make_fnode(file_data))

# 	return result









class DB(object):
	def __init__(self, db_path=None):
		self.db_path = db_path
		self.connection = None
		self.cursor = None
		if db_path:
			self.__connect()

	def __connect(self):
		self.connection = sqlite3.connect(self.db_path)
		# self.connection = sqlite3.connect(self.db_path, row_factory=sqlite3.Row)
		self.connection.row_factory = sqlite3.Row


	def open_db(self, db_path):
		
		if self.connection:
			self.connection.close()

		self.db_path = db_path
		self.__connect()

		self.migrate()


	def close_db(self):
		if self.connection:
			self.connection.close()


	def create_db(self, db_path):
		"""создание новой базы данных"""
		self.db_path = db_path
		self.__connect()
		self.cursor = self.connection.cursor()
		self.cursor.execute(sql.CREATE_TABLE_FILES)
		self.cursor.execute(sql.CREATE_TABLE_VOLUMES)
		self.cursor.execute(sql.CREATE_TABLE_SYSTEM)
		self.cursor.execute(sql.CREATE_VERSION, (VERSION,))
		self.cursor.execute(sql.CREATE_TIMESTAMP_CREATED, (now_date(),))
		self.cursor.execute(sql.CREATE_TIMESTAMP_UPDATED, (now_date(),))
		self.connection.commit()



	def get_version(self):
		cursor = self.connection.cursor()
		cursor.execute("SELECT value FROM system WHERE key = 'version'")
		row = cursor.fetchone()
		if row is None:
			return "0"
		return row[0]


	def get_system(self):
		"""получить системную информацию о базе"""
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM system")
		rows = cursor.fetchall()
		return rows


	def get_volumes(self):
		"""получить список всех томов"""
		cursor = self.connection.cursor()
		cursor.execute(sql.GET_VOLUMES)
		rows = cursor.fetchall()
		# result = make_volumes(rows)
		result = loader.make_vnodes(rows)
		return result
		


	# def get_files_all(self):
	# 	cursor = self.connection.cursor()
	# 	cursor.execute(sql.GET_FILES_ALL)
	# 	rows = cursor.fetchall()
	# 	return rows


	# def get_volume_files(self, volume_id):
	# 	cursor = self.connection.cursor()
	# 	cursor.execute("SELECT * FROM files WHERE volume_id=?", (volume_id, ))
	# 	rows = cursor.fetchall()
	# 	return rows


	def get_volume_root_files(self, volume_id):
		"""получить список файлов первого уровня для заданного тома"""
		cursor = self.connection.cursor()
		cursor.execute(sql.GET_VOLUME_ROOT_FILES, (volume_id, ))
		rows = cursor.fetchall()
		# result = make_fnodes(rows)
		result = loader.make_fnodes(rows)
		return result


	def get_parent_files(self, parent_id):
		"""получить список файлов для заданной директории"""
		cursor = self.connection.cursor()
		cursor.execute(sql.GET_PARENT_FILES, (parent_id, ))
		rows = cursor.fetchall()
		# result = make_fnodes(rows)
		result = loader.make_fnodes(rows)
		return result



	def get_file(self, file_id):
		"""получить заданную запись файла"""
		SQL = "SELECT * FROM files WHERE uuid = ?"
		cursor = self.connection.cursor()
		cursor.execute(SQL, (file_id, ))
		row = cursor.fetchone()

		if row is None:
			return None
		# result = make_fnode(row)
		result = loader.make_fnode(row)
		return result
		# return None


	def create_volume_row(self, vdata, commit=False):
		ivalues = (
			vdata["uuid"],
			vdata["name"],
			vdata["path"],
			vdata["vtype"],
			vdata["created"],
		)
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO volumes(uuid, name, path, vtype, created) VALUES(?,?,?,?,?)", ivalues)
		volume_id = cursor.lastrowid
		
		if commit:
			self.connection.commit()

		return volume_id



	def update_volume_row(self, vdata, commit=False):
		ivalues = (
			vdata["name"],
			vdata["vtype"],
			vdata["uuid"]
		)
		cursor = self.connection.cursor()
		cursor.execute("UPDATE volumes SET name=?, vtype=? WHERE uuid=?", ivalues)

		if commit:
			self.connection.commit()


	def update_version(self):
		log.info("обновление версии базы")
		cursor = self.connection.cursor()
		cursor.execute("UPDATE system SET value=? WHERE key='version'", (VERSION, ))

		


	def create_file_row(self, fdata, commit=False):
		ivalues = (
			fdata["volume_id"],
			fdata["parent_id"],
			fdata["uuid"],
			fdata["name"],
			fdata["type"],

			fdata["rights"],

			fdata["owner"],
			fdata["group"],
			
			fdata["size"],

			fdata["ctime"],
			fdata["atime"],
			fdata["mtime"],
			fdata["category"],
			fdata["description"]

		)

		cursor = self.connection.cursor()
		# cursor.execute("INSERT INTO files(volume_id, parent_id, uuid, name, type) VALUES(?,?,?,?,?)", ivalues)
		cursor.execute(sql.CREATE_FILE_ROW, ivalues)
		row_id = cursor.lastrowid

		if commit:
			self.connection.commit()

		return row_id


	


	def find_by_name(self, term):
		# SQL = "SELECT * FROM files WHERE name LIKE '%?%'";
		SQL = "SELECT * FROM files WHERE name LIKE '%" + term + "%'";
		
		cursor = self.connection.cursor()
		# cursor.execute(SQL, (term,))
		cursor.execute(SQL)
		rows = cursor.fetchall()
		# result = make_fnodes(rows)
		result = loader.make_fnodes(rows)
		# result = []
		return result



	def remove_volume_files(self, volume_uuid):
		cursor = self.connection.cursor()
		cursor.execute(sql.REMOVE_VOLUME_FILES, (volume_uuid, ))
		self.connection.commit()

	def remove_volume(self, volume_uuid):
		cursor = self.connection.cursor()
		cursor.execute(sql.REMOVE_VOLUME, (volume_uuid, ))
		self.connection.commit()


	def commit(self):
		self.connection.commit()





	def migrate(self):
		log.info("проверка версии базы")
		db_version = self.get_version()
		log.info("тек. версия: {}, необходима: {}".format(db_version, VERSION))

		if db_version == VERSION:
			log.info("версия базы подходящая")
			return True

		log.warning("необходима миграция")
		self.update_version()



		migration_steps = []

		if db_version == "1.0":
			migration_steps.append(migrations.up1_to_2)
		# 	migration_steps.append(migrations.up2_to_3)
		# elif db_version == "2":
		# 	migration_steps.append(migrations.up2_to_3)
			


		for action in migration_steps:
			action(self.connection)



		self.connection.commit()

		db_version = self.get_version()
		log.info("тек. версия: {}".format(db_version))



