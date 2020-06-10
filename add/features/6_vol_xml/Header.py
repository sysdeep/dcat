#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import gzip
import xml.etree.ElementTree as etree

class Header(object):
	FILE_NAME = "header.xml"
	def __init__(self, db_path: str):
		self.__db_path = db_path



	def save(self):
		full_path = os.path.join(self.__db_path, self.FILE_NAME)
		

		xroot = etree.Element("catalog", {"name": "оглавление", "description": "catalog description"})



		with open(full_path, "wb") as fd:
			fd.write(etree.tostring(xroot, encoding="utf-8"))


	def start(self) -> bool:
		full_path = os.path.join(self.__db_path, self.FILE_NAME)

		with open(full_path, "rb") as fd:
			xroot = etree.fromstring(fd.read())

			print(xroot)

		return True