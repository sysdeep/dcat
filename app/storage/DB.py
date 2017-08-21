#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from . import sql



def make_result(rows):
	result = []
	for row in rows:
		result.append(dict(row))

	return result






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


	def close_db(self):
		if self.connection:
			self.connection.close()


	def create_db(self, db_path):
		self.db_path = db_path
		self.__connect()
		self.cursor = self.connection.cursor()
		self.cursor.execute(sql.CREATE_TABLE_FILES)
		self.cursor.execute(sql.CREATE_TABLE_VOLUMES)
		self.connection.commit()




	def get_volumes(self):
		cursor = self.connection.cursor()
		cursor.execute(sql.GET_VOLUMES)
		rows = cursor.fetchall()
		result = make_result(rows)
		return result


	def get_files_all(self):
		cursor = self.connection.cursor()
		cursor.execute(sql.GET_FILES_ALL)
		rows = cursor.fetchall()
		return rows


	def get_volume_files(self, volume_id):
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM files WHERE volume_id=?", (volume_id, ))
		rows = cursor.fetchall()
		return rows


	def get_volume_root_files(self, volume_id):
		cursor = self.connection.cursor()
		cursor.execute(sql.GET_VOLUME_ROOT_FILES, (volume_id, ))
		# cursor.execute("SELECT * FROM files WHERE volume_id=? AND parent_id='0'", (volume_id, ))
		rows = cursor.fetchall()
		return rows


	def get_parent_files(self, parent_id):
		cursor = self.connection.cursor()
		cursor.execute(sql.GET_PARENT_FILES, (parent_id, ))
		# cursor.execute("SELECT * FROM files WHERE volume_id=? AND parent_id='0'", (volume_id, ))
		rows = cursor.fetchall()
		return rows


	def create_volume_row(self, vdata, commit=False):
		ivalues = (
			vdata["uuid"],
			vdata["name"]
		)
		cursor = self.connection.cursor()
		cursor.execute("INSERT INTO volumes(uuid, name) VALUES(?,?)", ivalues)
		volume_id = cursor.lastrowid
		
		if commit:
			self.connection.commit()

		return volume_id


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

