#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct


class Header(object):
	SIZE = 32
	def __init__(self, bdata=None):
		
		self.version = 0
		self.created = 0
		self.updated = 0
		self.vtype = 0
		self.dict_start = 0
		self.dict_size = 0

		self.data_start = 0
		self.data_size = 0

		if bdata:
			self.unpack(bdata)


	def pack(self):
		bdata = b""
       
		#--- 32b
		dataset = (
			self.version,			# 0
			self.created,			# 1
			self.updated,			# 2
			self.vtype,				# 3
			self.dict_start,		# 4
			self.dict_size,			# 5
			self.data_start,		# 6
			self.data_size,			# 7
		)
		bdata  += struct.pack("<IIIIIIII", *dataset)

		return bdata


	def unpack(self, bdata):
		dataset = struct.unpack("<IIIIIIII", bdata)

		self.dict_start = dataset[4]
		self.dict_size = dataset[5]

		self.data_start = dataset[6]
		self.data_size = dataset[7]



	def __str__(self):
		return "dict_start: {} \ndict_size: {} \ndata_start: {} \ndata_size: {}".format(self.dict_start, self.dict_size, self.data_start, self.data_size)