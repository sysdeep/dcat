#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
- type 			[ushort 2]	- тип файла(каталог - 0/файл - 1)
- size 			[ulong 8]	- размер записи
- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
- rights 		[ushort 2]	- код доступа(unix 777)
- fid 			[uint 4]	- id записи
- pid 			[uint 4]	- id родителя(0 - корень)
- npos			[uint 4] 	- позиция названия в куче
- nsize			[ushort 2] 	- размер названия в куче
- dpos			[uint 4] 	- позиция описания в куче
- dsize			[ushort 2] 	- размер описания в куче
"""
import struct
from io import BytesIO

class FileRecord:
	BDATA_SIZE = 40
	def __init__(self):
		self.ftype = 0				# тип записи
		self.size = 0
		self.ctime = 0
		self.rights = 0
		self.fid = 0
		self.pid = 0
		self.npos = 0
		self.nsize = 0
		self.dpos = 0
		self.dsize = 0
	
		self.name = ""
		self.description = ""
	
	
	
	#--- bin data -------------------------------------------------------------
	def unpack(self, bdata: bytes):
		
		row_tuple = struct.unpack("<HQQHIIIHIH", bdata)
		
		self.ftype = row_tuple[0]
		self.size = row_tuple[1]
		self.ctime = row_tuple[2]
		self.right = row_tuple[3]
		self.fid = row_tuple[4]
		self.pid = row_tuple[5]
		self.npos = row_tuple[6]
		self.nsize = row_tuple[7]
		self.dpos = row_tuple[8]
		self.dsize = row_tuple[9]
		
		
	
	def pack(self) -> bytes:
		
		
		
		
		
		row_tuple = (
			self.ftype,
			self.size,
			self.ctime,
			self.rights,
			self.fid,
			self.pid,
			self.npos,
			self.nsize,
			self.dpos,
			self.dsize,
		)
		
		bdata = struct.pack("<HQQHIIIHIH", *row_tuple)
		
		return bdata
	
	
	
	
	
	
	def write_heap(self, heap: BytesIO):
		
		# if self.pid == 0:
		# 	print("write heap: ", self.name)
		b_name = self.name.encode(encoding="utf-8")
		b_description = self.description.encode(encoding="utf-8")


		self.nsize = len(b_name)
		self.npos = heap.tell()
		heap.write(b_name)

		self.dsize = len(b_description)
		self.dpos = heap.tell()
		heap.write(b_description)
		
		
	def read_heap(self, heap: BytesIO):
		
		heap.seek(self.npos)
		b_name = heap.read(self.nsize)
		self.name = b_name.decode(encoding="utf-8")
		
		heap.seek(self.dpos)
		b_description = heap.read(self.dsize)
		self.description = b_description.decode(encoding="utf-8")
		
	#--- bin data -------------------------------------------------------------
