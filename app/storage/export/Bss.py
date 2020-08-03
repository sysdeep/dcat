#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import re
import base64
import struct
from app.lib import tools


MAGIC = 0xfafb
VERSION = 1


def __ushort2(v) -> bytes:
	return struct.pack("<H", v)

def __uint4(v) -> bytes:
	return struct.pack("<I", v)

def __ulong8(v) -> bytes:
	return struct.pack("<Q", v)

def __pack_str(text: str):
	bstr = text.encode(encoding="utf-8")
	str_len = len(bstr)
	bdata = __ushort2(str_len)
	bdata += bstr
	return bdata







def __vol_info(data: dict, records_len: int):
	"""
	{'created': '2017-09-27 11:05:42', 'name': 'oxygen_16x16', 'description': None,
	'updated': None, 'uuid': '3a618114-f766-4767-a058-79d3a1b1da07', 'vtype': 'cd', 'path': '/home/nia/Development/_Python/_DCat/oxygen_16x16'}
	
	"""
	
	bdata = b''
	
	#--- [created](8)
	bdata += __ulong8(0)				# TODO
	
	#--- [icon](2)
	bdata += __ushort2(1)				# TODO
	
	#--- [records](8)
	bdata += __ulong8(records_len)
	
	#--- [name]
	bdata += __pack_str(data["name"])
	
	#--- [scan_path]
	bdata += __pack_str(data["path"])
	
	#--- [description]
	bdata += __pack_str(data["description"])
	
	return bdata







def __format_row(row_data: dict) -> bytes:
	"""
	{'name': 'k3b.png', 'size': 998,
	'rights': 0, 'group': '',
	'category': 0, 'owner': '', 'ctime': 1481536946.5915499,
	'ftype': 1,
	'volume_id': '3a618114-f766-4767-a058-79d3a1b1da07',
	'parent_id': '73fc11a5-5c81-4f05-83b5-3b42baadc91c', 'uuid': '90d897f9-9803-4fe3-a006-7df326438a4c',
	'description': '', 'mtime': 0, 'atime': 0}
	
	
	len_frame
	frame
	
	"""
	
	bdata = b''
	
	#--- type 			[ushort 2]	- тип файла(каталог/файл...)
	bdata += __ushort2(1)				# TODO
	
	#--- size 			[ulong 8]	- размер записи
	bdata += __ulong8(row_data["size"])
	
	#--- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
	bdata += __ulong8(0)				# TODO
	
	#--- rights 		[ushort 2]	- код доступа(unix 777)
	bdata += __ushort2(row_data["rights"])
	
	#--- fid 			[uint 4]	- id записи
	bdata += __uint4(0)					# TODO
	
	#--- pid 			[uint 4]	- id родителя(0 - корень)
	bdata += __uint4(0)					# TODO
	
	#--- name 			[bstr]		- название
	bdata += __pack_str(row_data["name"])
	
	#--- description 	[bstr]		- произвольное описание
	bdata += __pack_str(row_data["description"])

	
	return bdata




@tools.dtimeit
def start_export(vol_info: dict, files_list: list, file_path: str):
	
	
	
	fd = gzip.open(file_path + ".gz", "wb")
	
	magic = __ushort2(MAGIC)
	#--- [magic](2)
	fd.write(magic)
	
	#--- [version](2)
	fd.write(__ushort2(VERSION))
	
	
	header = __vol_info(vol_info, len(files_list))
	print("header len: ", len(header))
	#--- [header_len](2)
	fd.write(__ushort2(len(header)))
	
	#--- [header_struct]
	fd.write(header)
	
	#--- [magic](2)
	fd.write(magic)
	
	for fdata in files_list:
		
		try:
			row_data = __format_row(fdata)
		except Exception as e:
			print(e)
			print("+"*10)
			print(fdata)
			print("+"*10)
			break
		
		#--- [row_len]
		fd.write(__ushort2(len(row_data)))
		
		#--- [row_struct]
		fd.write(row_data)
	
	#--- [magic](2)
	fd.write(magic)
	
	
	fd.flush()
	fd.close()
	
	