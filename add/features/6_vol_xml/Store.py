#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import os.path

from Header import Header
from Volume import Volume
 

class Store(object):
	def __init__(self):
		self.__db_path = None

	def create(self, db_path: str, db_name: str):

		full_path = os.path.join(db_path, db_name)
		if not os.path.exists(full_path):
			os.mkdir(full_path)
		
		header = Header(full_path)
		header.save()

		self.__db_path = full_path


	def open_db(self, db_path):
		self.__db_path = db_path
		header = Header(db_path)
		r = header.start()


	def add_volume(self, volume_name: str, scan_path: str) -> bool:

		#--- create volume
		vol = Volume(self.__db_path)
		r = vol.create(volume_name, scan_path)

		#--- update dict
		#
		return True




	def get_volumes(self):
		pass


	