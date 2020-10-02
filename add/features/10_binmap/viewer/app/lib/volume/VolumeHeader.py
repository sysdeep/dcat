#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
- created	(8)				- дата создания(unix timestamp)
- icon		(2)				- icon_id
- records	(8)				- кол-во записей в базе
- table_len	(8)				- длина секции табличных данных
- heap_len	(8)				- длина секции кучи
- npos			[uint 4] 	- позиция названия в куче
- nsize			[ushort 2] 	- размер названия в куче
- ppos			[uint 4] 	- позиция пути сканирования в куче
- psize			[ushort 2] 	- размер пути сканирования в куче
- dpos			[uint 4] 	- позиция описания в куче
- dsize			[ushort 2] 	- размер описания в куче


def ushort2(v: bytes) -> int:
	return struct.unpack("<H", v)[0]

def uint4(v: bytes) -> int:
	return struct.unpack("<I", v)[0]

def ulong8(v: bytes) -> int:
	return struct.unpack("<Q", v)[0]
"""
import struct
from io import BytesIO

class VolumeHeader:
	BDATA_SIZE = 52
	def __init__(self):
		self.created = 0			# 0
		self.icon = 0				# 1
		self.records = 0			# 2
		self.table_len = 0			# 3
		self.heap_len = 0			# 4
		self.npos = 0				# 5
		self.nsize = 0				# 6
		self.ppos = 0				# 7
		self.psize = 0				# 8
		self.dpos = 0				# 9
		self.dsize = 0				# 10
		
		self.name = ""
		self.scan_path = ""
		self.description = ""
		
	#--- bin data -------------------------------------------------------------
	def unpack(self, bdata: bytes):
		
		row_tuple = struct.unpack("<QHQQQIHIHIH", bdata)
		
		self.created = row_tuple[0]
		self.icon = row_tuple[1]
		self.records = row_tuple[2]
		self.table_len = row_tuple[3]
		self.heap_len = row_tuple[4]
		self.npos = row_tuple[5]
		self.nsize = row_tuple[6]
		self.ppos = row_tuple[7]
		self.psize = row_tuple[8]
		self.dpos = row_tuple[9]
		self.dsize = row_tuple[10]
		
		
	
	def pack(self) -> bytes:
		
		
		
		
		
		row_tuple = (
			self.created,
			self.icon,
			self.records,
			self.table_len,
			self.heap_len,
			self.npos,
			self.nsize,
			self.ppos,
			self.psize,
			self.dpos,
			self.dsize,
		)
		
		bdata = struct.pack("<QHQQQIHIHIH", *row_tuple)
		
		return bdata
	
	
	def write_heap(self, heap: BytesIO):
		
		b_name = self.name.encode(encoding="utf-8")
		b_scan_path = self.scan_path.encode(encoding="utf-8")
		b_description = self.description.encode(encoding="utf-8")


		self.nsize = len(b_name)
		self.psize = heap.tell()
		heap.write(b_name)

		self.psize = len(b_scan_path)
		self.ppos = heap.tell()
		heap.write(b_scan_path)

		self.dsize = len(b_description)
		self.dpos = heap.tell()
		heap.write(b_description)
		
		
	def read_heap(self, heap: BytesIO):
		
		heap.seek(self.npos)
		b_name = heap.read(self.nsize)
		self.name = b_name.decode(encoding="utf-8")
		
		heap.seek(self.ppos)
		b_scan_path = heap.read(self.psize)
		self.scan_path = b_scan_path.decode(encoding="utf-8")
		
		heap.seek(self.dpos)
		b_description = heap.read(self.dsize)
		self.description = b_description.decode(encoding="utf-8")
		
		
	#--- bin data -------------------------------------------------------------


	# def __str__(self):
	# 	return "magic: {}, version: {}".format(self.magic, self.version)


	def print_header(self):
		print("=== header ===")
		
		print("created: ", self.created)
		print("icon: ", self.icon)
		print("total records: ", self.records)
		
		print("table_len: ", self.table_len)
		print("heap_len: ", self.heap_len)
		print("name_data: {}:{}".format(self.npos, self.nsize))
		print("path_data: {}:{}".format(self.ppos, self.psize))
		print("description_data: {}:{}".format(self.dpos, self.dsize))
		print("volume name: ", self.name)
		print("scan path: ", self.scan_path)
		print("description: ", self.description)
		print("=== header ===")