#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import time

from app import log
from app.lib.fdate import sql_date

from . import migrations
from . import sql
from .models import loader
from . import defs
from . import sbus



#--- BD module version
VERSION = "3"







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

		self.cursor = self.connection.cursor()


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
		self.cursor.execute(sql.CREATE_TIMESTAMP_CREATED, (sql_date(),))
		self.cursor.execute(sql.CREATE_TIMESTAMP_UPDATED, (sql_date(),))
		self.cursor.execute(sql.CREATE_SYSTEM_DESCRIPTION, ("init",))
		self.commit()


	def vacuum(self):
		"""уплотнение базы"""
		self.cursor = self.connection.cursor()
		self.cursor.execute("VACUUM")
		self.commit()


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


	def get_system_value(self, key):
		"""получить тек. значение системной информации"""
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM system WHERE key = '" + key + "'")
		row = cursor.fetchone()

		if row is None:
			return "---"

		return row["value"]

		# system_data = cache.get_system()
		# return system_data.get(key, "not found")


	def get_volumes(self):
		"""получить список всех томов"""
		cursor = self.connection.cursor()
		cursor.execute(sql.GET_VOLUMES)
		rows = cursor.fetchall()
		# result = make_volumes(rows)
		result = loader.make_vnodes(rows)
		return result


	def get_volume(self, volume_id):
		"""получить данные по заданному тому"""
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM volumes WHERE uuid=?", (volume_id, ))
		row = cursor.fetchone()

		if row is None:
			return None

		result = loader.make_vnode(row)
		return result




	# def get_files_all(self):
	# 	cursor = self.connection.cursor()
	# 	cursor.execute(sql.GET_FILES_ALL)
	# 	rows = cursor.fetchall()
	# 	return rows


	def get_volume_all_files(self, volume_id):
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM files WHERE volume_id=?", (volume_id, ))
		rows = cursor.fetchall()
		result = loader.make_fnodes(rows)
		return result


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
		# # cursor = self.connection.cursor()
		# self.cursor.execute(sql.GET_PARENT_FILES, (parent_id, ))
		# rows = self.cursor.fetchall()
		# # result = make_fnodes(rows)
		# result = loader.make_fnodes(rows)
		# return result


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
			vdata["description"]
		)
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO volumes(uuid, name, path, vtype, created, description) VALUES(?,?,?,?,?,?)", ivalues)
		volume_id = cursor.lastrowid
		self.update_db_timestamp()
		
		if commit:
			self.commit()

		return volume_id


	#--- updates --------------------------------------------------------------
	def update_volume_row(self, vdata, commit=False):
		ivalues = (
			vdata["name"],
			vdata["vtype"],
			vdata["description"],
			sql_date(),
			vdata["uuid"]
		)
		cursor = self.connection.cursor()
		cursor.execute("UPDATE volumes SET name=?, vtype=?, description=?, updated=? WHERE uuid=?", ivalues)
		self.update_db_timestamp()

		if commit:
			self.commit()


	def update_version(self):
		log.info("обновление версии базы")
		cursor = self.connection.cursor()
		cursor.execute("UPDATE system SET value=? WHERE key='version'", (VERSION, ))
		self.update_db_timestamp()


	def update_system(self, key, value):
		log.info("обновление системной информации:")
		log.info("\t{}: {}".format(key, value))
		cursor = self.connection.cursor()
		cursor.execute("UPDATE system SET value=? WHERE key=?", (value, key))
		self.update_db_timestamp()

	def update_db_timestamp(self):
		cursor = self.connection.cursor()
		cursor.execute("UPDATE system SET value=? WHERE key=?", (sql_date(), defs.SYS_KEY_UPDATED))
	#--- updates --------------------------------------------------------------



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

		self.update_db_timestamp()
		if commit:
			self.commit()

		return row_id





	def find_by_name(self, term, volume_id=None):
		"""поиск файлов по имени"""
		SQL = "SELECT * FROM files WHERE name LIKE '%{}%'".format(term)
		if volume_id:
			SQL += " AND volume_id = '" + volume_id + "'"

		cursor = self.connection.cursor()
		cursor.execute(SQL)
		rows = cursor.fetchall()
		result = loader.make_fnodes(rows)
		return result



	def remove_volume_files(self, volume_uuid):
		cursor = self.connection.cursor()
		cursor.execute(sql.REMOVE_VOLUME_FILES, (volume_uuid, ))
		self.update_db_timestamp()
		self.commit()


	def remove_volume(self, volume_uuid):
		cursor = self.connection.cursor()
		cursor.execute(sql.REMOVE_VOLUME, (volume_uuid, ))
		self.update_db_timestamp()
		self.commit()


	def remove_file(self, file_uuid, commit=False):
		"""удаление заданной записи файла"""

		cursor = self.connection.cursor()
		cursor.execute("DELETE FROM files WHERE uuid=?", (file_uuid, ))

		if commit:
			print("commit file")
			self.commit()


	def remove_files(self, files_uuid_list):
		cursor = self.connection.cursor()
		cursor.executemany("DELETE FROM files WHERE uuid=?", files_uuid_list)


	def commit(self):
		"""выполнить коммит и сообщить всем"""
		self.update_db_timestamp()
		self.connection.commit()
		sbus.emit(sbus.DB_COMMITTED)





	def migrate(self):
		log.info("проверка версии базы")
		db_version = self.get_version()
		log.info("тек. версия: {}, необходима: {}".format(db_version, VERSION))

		if db_version == VERSION:
			log.info("версия базы подходящая")
			return True

		log.warning("необходима миграция")
		

		migration_steps = []

		if db_version == "1.0":
			migration_steps.append(migrations.up1_to_2)
			migration_steps.append(migrations.up2_to_3)
		elif db_version == "2":
			migration_steps.append(migrations.up2_to_3)



		for action in migration_steps:
			action(self.connection)



		self.update_version()
		self.update_db_timestamp()
		self.commit()

		db_version = self.get_version()
		log.info("тек. версия: {}".format(db_version))

		sbus.emit(sbus.DB_MIGRATED)



