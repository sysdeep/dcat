#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import re
import time
import datetime
import struct
import os.path
from io import BytesIO


def timeit(func):
	def timed(*args, **kwargs):
		ts = time.time()
		result = func(*args, **kwargs)
		te = time.time()

		print("timeit: ", te - ts)
		return result

	return timed

PATH = "/home/nia/Development/_Python/_DCat/Export10"
FILE = "Video.bm.gz"
# FILE = "Apps.bss.gz"
# FILE = "_DNote.bss.gz"

FULL_PATH = os.path.join(PATH, FILE)


def __ushort2(v: bytes) -> int:
	return struct.unpack("<H", v)[0]

def __uint4(v: bytes) -> int:
	return struct.unpack("<I", v)[0]

def __ulong8(v: bytes) -> int:
	return struct.unpack("<Q", v)[0]




class BReader(object):
	def __init__(self, bdata):
		self.bdata = bdata
		self.__ptr = 0
		

	def read_ushort(self) -> int:
		if self.__ptr > len(self.bdata):
			throw("owerflow")

		v = struct.unpack("<H", self.bdata[self.__ptr:self.__ptr+2])[0]
		self.__ptr += 2
		return v

	def read_uint(self) -> int:
		if self.__ptr > len(self.bdata):
			throw("owerflow")

		v = struct.unpack("<I", self.bdata[self.__ptr:self.__ptr+4])[0]
		self.__ptr += 4
		return v

	def read_ulong(self) -> int:
		if self.__ptr > len(self.bdata):
			throw("owerflow")

		v = struct.unpack("<Q", self.bdata[self.__ptr:self.__ptr+8])[0]
		self.__ptr += 8
		return v

	def read_string(self) -> str:
		if self.__ptr > len(self.bdata):
			throw("owerflow")
		str_len = struct.unpack("<H", self.bdata[self.__ptr:self.__ptr+2])[0]
		self.__ptr += 2

		if self.__ptr > len(self.bdata):
			throw("owerflow")
		result = self.bdata[self.__ptr:self.__ptr+str_len].decode("utf-8")
		self.__ptr += str_len
		
		return result






def __un_header(bdata) -> int:
	reader = BReader(bdata)

	#--- [created](8)
	created = reader.read_ulong()
	
	#--- [icon](2)
	icon = reader.read_ushort()
	
	#--- [records](8)
	records = reader.read_ulong()
	
	section_data_len = reader.read_ulong()
	section_text_len = reader.read_ulong()
	
	#--- [name]
	name = reader.read_string()
	
	#--- [scan_path]
	path = reader.read_string()
	
	#--- [description]
	description = reader.read_string()


	created_s = datetime.datetime.fromtimestamp(created)
	# print(created_s)

	print("=== header ===")
	print("volume name: ", name)
	print("volume path: ", path)
	# print("created: ", created)
	print("icon: ", icon)
	print("total records: ", records)
	print("section data len: ", section_data_len)
	print("section text len: ", section_text_len)
	print("description: ", description)
	print("created: ", created_s)
	print("=== header ===")

	return records
	


def __un_row(bdata):
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



S_DATA = b''
T_DATA = b''

@timeit
def unpack():
	fd = gzip.open(FULL_PATH, "rb")


	#--- [magic](2)
	magic = __ushort2(fd.read(2))
	print("-"*10)
	print("magic: ", magic)
	print("-"*10)

	#--- [version](2)
	version = __ushort2(fd.read(2))
	print("version: ", version)

	#--- [header_len](2)
	header_len = __ushort2(fd.read(2))
	print("header_len: ", header_len)




	#--- [header_struct]
	header_data = fd.read(header_len)
	total_records = __un_header(header_data)



	#--- data section
	



	
	# #--- [magic](2)
	# magic = __ushort2(fd.read(2))
	# print("-"*10)
	# print("magic: ", magic)
	# print("-"*10)

	# current_file = 0
	# while True:
	# 	#--- [row_len](2)
	# 	try:
	# 		chunk = fd.read(2)
	# 	except Exception as e:
	# 		print(e)
	# 		break
	#
	# 	if not chunk:
	# 		break
	#
	# 	row_len = __ushort2(chunk)
	# 	if row_len == magic:
	# 		print("last magic!!! - done")
	# 		break
	# 	#--- [row_struct]
	# 	row_data = fd.read(row_len)
	# 	__un_row(row_data)
	#
	# 	current_file += 1
	#
	# 	if current_file > total_records:
	# 		print("ERROR!!!")
	# 		print("processed records > total records - break")
	# 		print(current_file, " > ", total_records)
	# 		break



	fd.close()





if __name__ == "__main__":

	unpack()