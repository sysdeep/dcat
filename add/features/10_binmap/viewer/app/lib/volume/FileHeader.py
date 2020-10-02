#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct


class FileHeader:
	MAGIC = 0xfafb
	VERSION = 1
	BDATA_SIZE = 4
	def __init__(self):
		self.magic = 0xfafb
		self.version = 1






	#--- bin data -------------------------------------------------------------
	def unpack(self, bdata: bytes):
		self.magic, self.version = struct.unpack("<HH", bdata)
	
	def pack(self) -> bytes:
		row_tuple = (self.magic, self.version)
		bdata = struct.pack("<HH", *row_tuple)
		return bdata
		
		
	#--- bin data -------------------------------------------------------------


	def __str__(self):
		return "magic: {}, version: {}".format(self.magic, self.version)