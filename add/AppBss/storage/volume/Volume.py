#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
from enum import Enum
import struct
import datetime
from .BReader import BReader

def ushort2(v: bytes) -> int:
	return struct.unpack("<H", v)[0]

def uint4(v: bytes) -> int:
	return struct.unpack("<I", v)[0]

def ulong8(v: bytes) -> int:
	return struct.unpack("<Q", v)[0]




DET = "-"*10

class Sections(Enum):
	header = 0
	body = 1




class Record(object):
	def __init__(self):
		self.name = ""
		self.uuid = ""
		self.parent = ""
		self.ftype = 0				# 0-dir, 1-file

		self.childrens = []


	def append(self, ch):
		self.childrens.append(ch)


def parse_record(line: str) -> Record:
	try:
		fields = line.split("|")
	except Exception as e:
		print(e)
		return None
	
	r = Record()
	r.name = fields[0]
	r.uuid = fields[10]
	r.parent = fields[9]
	
	return r







class Volume(object):
	def __init__(self, full_path):
		self.path = full_path
		
		self.name = "undefined"
		
		self.__body_start = 0
		self.__magic = 0
		self.__total_records = 0
		
		self.__tree = []
		self.__tmap = {}
		self.__roots = []
		
		
	def read_header(self):
		fd = gzip.open(self.path, "rb")
		
		
		
		#--- [magic](2)
		self.__magic = ushort2(fd.read(2))
		print("-"*10)
		print("magic: ", self.__magic)
		print("-"*10)
	
		#--- [version](2)
		version = ushort2(fd.read(2))
		print("version: ", version)
	
		#--- [header_len](2)
		header_len = ushort2(fd.read(2))
		print("header_len: ", header_len)
	
		#--- [header_struct]
		header_data = fd.read(header_len)
		self.__total_records = self.__un_header(header_data)
		
		#--- [magic](2)
		magic = ushort2(fd.read(2))
		print("-"*10)
		print("magic: ", magic)
		print("-"*10)
		
		
		self.__body_start = (2 * 4) + header_len
		
		
		
		
		
		
		# sheader = []
		# section = Sections.header
		# c = 1000
		# while True:
		#
		# 	line = fd.readline().strip()
		# 	if not line:
		# 		print("null line")
		# 		break
		#
		# 	if section == Sections.header:
		# 		if line == DET:
		# 			break
		# 		else:
		# 			sheader.append(line)
		#
		#
		# 	c -= 1
		# 	if c < 0:
		# 		print("emerg")
		# 		break
		#
		# fd.close()
		#
		#
		# for line in sheader:
		# 	print(line)
		# 	chunks = line.split(":")
		#
		# 	if chunks[0] == "name":
		# 		self.name = chunks[1]
		# 		break



	def read_body(self):
		fd = gzip.open(self.path, "rb")
		fd.seek(self.__body_start)
		
		
		current_file = 0
		while True:
			#--- [row_len](2)
			try:
				chunk = fd.read(2)
			except Exception as e:
				print(e)
				break
	
			if not chunk:
				break
	
			row_len = ushort2(chunk)
			if row_len == self.__magic:
				print("last magic!!! - done")
				break
			#--- [row_struct]
			row_data = fd.read(row_len)
			record = self.__un_row(row_data)		# TODO
			
			self.__tmap[record.uuid] = record
			if record.parent == 0:
				self.__roots.append(record)
	
			current_file += 1
	
			if current_file > self.__total_records:
				print("ERROR!!!")
				print("processed records > total records - break")
				print(current_file, " > ", self.__total_records)
				break
			
		fd.close()
		
		self.__link()


	def __link(self):
		for r in self.__tmap.values():
			if r.parent == 0:
				continue
			
			parent_node = self.__tmap.get(r.parent)
			if parent_node:
				parent_node.append(r)
			


	def get_root(self) -> list:
		
		# return [r for r in self.__tree if r.parent == "0"]
		return self.__roots
	
	
	
	
	def __un_header(self, bdata) -> int:
		reader = BReader(bdata)
	
		#--- [created](8)
		created = reader.read_ulong()
		
		#--- [icon](2)
		icon = reader.read_ushort()
		
		#--- [records](8)
		records = reader.read_ulong()
		
		#--- [name]
		name = reader.read_string()
		
		#--- [scan_path]
		path = reader.read_string()
		
		#--- [description]
		description = reader.read_string()
	
	
		created_s = datetime.datetime.fromtimestamp(created)
		print(created_s)
	
		print("=== header ===")
		print("volume name: ", name)
		print("volume path: ", path)
		print("created: ", created)
		print("icon: ", icon)
		print("total records: ", records)
		print("description: ", description)
	
	
	
		self.name = name
	
		return records
	
	
	
	def __un_row(self, bdata) -> Record:
		reader = BReader(bdata)
	
		#--- type 			[ushort 2]	- тип файла(каталог/файл...)
		row_type = reader.read_ushort()
		
		#--- size 			[ulong 8]	- размер записи
		file_size = reader.read_ulong()
		
		#--- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
		created = reader.read_ulong()
		
		#--- rights 		[ushort 2]	- код доступа(unix 777)
		rights = reader.read_ushort()
		
		#--- fid 			[uint 4]	- id записи
		fid = reader.read_uint()
		
		#--- pid 			[uint 4]	- id родителя(0 - корень)
		pid = reader.read_uint()				# TODO
		
		#--- name 			[bstr]		- название
		name = reader.read_string()
		
		#--- description 	[bstr]		- произвольное описание
		description = reader.read_string()
	
		# print("\t", name)
	
	
		r = Record()
		r.name = name
		r.uuid = fid
		r.parent = pid
		r.ftype = row_type
		
		return r