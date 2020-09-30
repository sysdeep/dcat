#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import re
import base64
import struct
from io import BytesIO
from app.lib import tools
import time


MAGIC = 0xfafb
VERSION = 1


def ushort2(v) -> bytes:
	return struct.pack("<H", v)

def uint4(v) -> bytes:
	return struct.pack("<I", v)

def ulong8(v) -> bytes:
	return struct.pack("<Q", v)

def pack_str(text: str):
	bstr = text.encode(encoding="utf-8")
	str_len = len(bstr)
	bdata = ushort2(str_len)
	bdata += bstr
	return bdata


VOLUME_ICONS = {
	"cd"        : 1,
	"dvd"       : 2,
	"bdrom"		: 3,
	"crypted"	: 4,
	"folder"    : 5,
	
	"audio_cd"  : 6,
	"hdd"       : 7,
	"hdd_usb"   : 8,
	"flash"     : 9,
	"sd"        : 10,
	"floppy"    : 11,
	"net"       : 12,
	"tape"      : 13,
	"other"     : 14,
	
}






def __vol_info(data: dict, records_len: int):
	"""
	{'created': '2017-09-27 11:05:42', 'name': 'oxygen_16x16', 'description': None,
	'updated': None, 'uuid': '3a618114-f766-4767-a058-79d3a1b1da07',
	'vtype': 'cd', 'path': '/home/nia/Development/_Python/_DCat/oxygen_16x16'}
	
	
	
	 %Y  Year with century as a decimal number.
    %m  Month as a decimal number [01,12].
    %d  Day of the month as a decimal number [01,31].
    %H  Hour (24-hour clock) as a decimal number [00,23].
    %M  Minute as a decimal number [00,59].
    %S  Second as a decimal number [00,61].
    %z  Time zone offset from UTC.
    %a  Locale's abbreviated weekday name.
    %A  Locale's full weekday name.
    %b  Locale's abbreviated month name.
    %B  Locale's full month name.
    %c  Locale's appropriate date and time representation.
    %I  Hour (12-hour clock) as a decimal number [01,12].
    %p  Locale's equivalent of either AM or PM.

	
	"""
	try:
		time_tuple = time.strptime(data["created"], "%Y-%m-%d %H:%M:%S")
		timestamp = int(time.mktime(time_tuple))
	except Exception as e:
		print(e)
		timestamp = 0
		
	icon_id = VOLUME_ICONS.get(data["vtype"], 14)			# or other
	
	
	bdata = b''
	
	#--- [created](8)
	bdata += ulong8(timestamp)
	
	#--- [icon](2)
	bdata += ushort2(icon_id)
	
	#--- [records](8)
	bdata += ulong8(records_len)
	
	#--- [name]
	bdata += pack_str(data["name"])
	
	#--- [scan_path]
	bdata += pack_str(data["path"])
	
	#--- [description]
	bdata += pack_str(data["description"])
	
	return bdata


class Header:
	def __init__(self):
		self.magic = MAGIC
		self.version = VERSION
		self.icon_id = 0
		self.timestamp = 0
		self.records_len = 0
		self.name = ""
		self.path = ""
		self.description = ""
		
		self.section_table_len = 0
		self.section_text_len = 0
		
		
	def set_vol_info(self, data: dict):
		try:
			time_tuple = time.strptime(data["created"], "%Y-%m-%d %H:%M:%S")
			self.timestamp = int(time.mktime(time_tuple))
		except Exception as e:
			print(e)
			self.timestamp = 0
			
		self.icon_id = VOLUME_ICONS.get(data["vtype"], 14)			# or other
		
		
		#--- [name]
		self.name = data["name"]
		
		#--- [scan_path]
		self.path = data["path"]
		
		#--- [description]
		self.description = data["description"]


	def make(self) -> BytesIO:
		buf = BytesIO()
		
		
	
		#--- [created](8)
		buf.write(ulong8(self.timestamp))
		
		#--- [icon](2)
		buf.write(ushort2(self.icon_id))
		
		#--- [records](8)
		buf.write(ulong8(self.records_len))
		
		
		buf.write(ulong8(self.section_table_len))
		buf.write(ulong8(self.section_text_len))
		
		#--- [name]
		buf.write(pack_str(self.name))
		
		#--- [scan_path]
		buf.write(pack_str(self.path))
		
		#--- [description]
		buf.write(pack_str(self.description))
		
		# buf.close()
		
		return buf



class RowData:
	def __init__(self):
		self.ftype = 0
		self.size = 0
		self.ctime = 0
		self.rights = 0
		self.uuid = 0
		self.parent_id = 0
		
		self.text_data_pos = 0
	
	def set_data(self, row_data: dict):
		
		#--- type 			[ushort 2]	- тип файла(каталог - 0/файл - 1)
		self.ftype = row_data["ftype"]
		
		#--- size 			[ulong 8]	- размер записи
		self.size = row_data["size"]
		
		#--- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
		self.ctime = int(row_data["ctime"])
		
		#--- rights 		[ushort 2]	- код доступа(unix 777)
		self.rights = row_data["rights"]
		
		#--- fid 			[uint 4]	- id записи
		# bdata += uint4(0)					# TODO
		self.uuid = row_data["uuid"]
		
		#--- pid 			[uint 4]	- id родителя(0 - корень)
		# bdata += uint4(0)					# TODO
		self.parent_id = row_data["parent_id"]
		
		
	def make(self) -> BytesIO:
		buf = BytesIO()
		
		#--- type 			[ushort 2]	- тип файла(каталог - 0/файл - 1)
		buf.write(ushort2(self.ftype))
		
		#--- size 			[ulong 8]	- размер записи
		buf.write(ulong8(self.size))
		
		#--- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
		buf.write(ulong8(self.ctime))
		
		#--- rights 		[ushort 2]	- код доступа(unix 777)
		buf.write(ushort2(self.rights))
		
		#--- fid 			[uint 4]	- id записи
		buf.write(uint4(self.uuid))
		
		#--- pid 			[uint 4]	- id родителя(0 - корень)
		buf.write(uint4(self.parent_id))
		
		#--- text_data local offset 			[uint 4]
		buf.write(uint4(self.text_data_pos))
		
		return buf



class TextData:
	def __init__(self):
		self.name = ""
		self.description = ""

	def set_data(self, fdata: dict):
		self.name = fdata["name"]
		self.description = fdata["description"]
		
	def make(self) -> BytesIO:
		buf = BytesIO()
		
		#--- name 			[bstr]		- название
		buf.write(pack_str(self.name))

		#--- description 	[bstr]		- произвольное описание
		# buf.write(pack_str(self.description))
		
		return buf


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
	
	#--- type 			[ushort 2]	- тип файла(каталог - 0/файл - 1)
	bdata += ushort2(row_data["ftype"])
	
	#--- size 			[ulong 8]	- размер записи
	bdata += ulong8(row_data["size"])
	
	#--- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
	bdata += ulong8(int(row_data["ctime"]))
	
	#--- rights 		[ushort 2]	- код доступа(unix 777)
	bdata += ushort2(row_data["rights"])
	
	#--- fid 			[uint 4]	- id записи
	# bdata += uint4(0)					# TODO
	bdata += uint4(row_data["uuid"])
	
	#--- pid 			[uint 4]	- id родителя(0 - корень)
	# bdata += uint4(0)					# TODO
	bdata += uint4(row_data["parent_id"])
	
	# #--- name 			[bstr]		- название
	# bdata += pack_str(row_data["name"])
	#
	# #--- description 	[bstr]		- произвольное описание
	# bdata += pack_str(row_data["description"])

	
	return bdata




def __convert_files(files: list):
	
	omap = {
		"0"	: 0,
	}			# uuid: new id
	
	
	new_id = 1
	
	#--- fix root parent
	# for row in files:
	# 	if row["parent_id"] == "0":
	# 		row["parent_id"] = 0
	
	#--- update fid
	for row in files:
		omap[row["uuid"]] = new_id
		row["uuid"] = new_id
		new_id += 1
		
	#--- update parents
	for row in files:
		try:
			new_parent_id = omap[row["parent_id"]]
		except:
			print("!!! no found parent in omap")
			continue
			
		row["parent_id"] = new_parent_id








def __create_sections(files_list: list) -> (BytesIO, BytesIO):
	section_data = BytesIO()
	section_text = BytesIO()
	
	
	for fdata in files_list:
		
		
		text_local_pos = section_text.tell()
		
		
		rd = RowData()
		rd.set_data(fdata)
		rd.text_data_pos = text_local_pos
		
		
		
		
		
		
		td = TextData()
		td.set_data(fdata)
		
		
		# try:
		# 	row_data = __format_row(fdata)
		# except Exception as e:
		# 	print(e)
		# 	print("+"*10)
		# 	print(fdata)
		# 	print("+"*10)
		# 	break
		#
		#--- [row_len]
		# fd.write(ushort2(len(row_data)))
		
		
		
		btd = td.make()
		section_text.write(btd.getbuffer())
		
		
		
		
		
		brd = rd.make()
		section_data.write(brd.getbuffer())
		
		
		brd.close()
		btd.close()


	# section_data.close()
	
	return section_data, section_text








@tools.dtimeit
def start_export(vol_info: dict, files_list: list, file_path: str):
	
	
	
	
	
	
	
	
	
	#--- convert files(fid/pid)
	__convert_files(files_list)
	
	
	
	
	
	
	
	
	
	
	#--- make sections
	sdata, tdata = __create_sections(files_list)
	
	
	#--- make header
	header = Header()
	header.set_vol_info(vol_info)
	header.records_len = len(files_list)
	header.section_table_len = len(sdata.getbuffer())
	header.section_text_len = len(tdata.getbuffer())
	hdata = header.make()
	
	
	
	
	
	
	
	
	fd = gzip.open(file_path + ".gz", "wb")
	
	magic = ushort2(MAGIC)
	#--- [magic](2)
	fd.write(magic)
	
	#--- [version](2)
	fd.write(ushort2(VERSION))
	
	
	header_len = len(hdata.getbuffer())
	# header = __vol_info(vol_info, len(files_list))
	print("header len: ", header_len)
	#--- [header_len](2)
	fd.write(ushort2(header_len))
	
	# #--- [header_struct]
	# fd.write(header)
	#
	# #--- [magic](2)
	# fd.write(magic)
	#
	
	
	
	
	#--- write header
	fd.write(hdata.getbuffer())
	
	#--- write data
	fd.write(sdata.getbuffer())

	#--- write text
	fd.write(tdata.getbuffer())
	
	
	
	hdata.close()
	sdata.close()
	tdata.close()
	
	
	
	
	# for fdata in files_list:
	#
	# 	try:
	# 		row_data = __format_row(fdata)
	# 	except Exception as e:
	# 		print(e)
	# 		print("+"*10)
	# 		print(fdata)
	# 		print("+"*10)
	# 		break
	#
	# 	#--- [row_len]
	# 	fd.write(ushort2(len(row_data)))
	#
	# 	#--- [row_struct]
	# 	fd.write(row_data)
	#
	#--- [magic](2)
	fd.write(magic)
	
	
	fd.flush()
	fd.close()
	
	
	
