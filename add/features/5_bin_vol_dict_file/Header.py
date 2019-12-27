#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct


class Header(object):
	SIZE = 36
	STRUCT_STR = "<IIIIIIIII"
	def __init__(self, bdata=None):
		
		self.version = 0
		self.created = 0
		self.updated = 0
		self.vtype = 0

		self.dict_start = 0
		self.dict_size = 0

		self.data_start = 0
		self.data_size = 0

		self.total_records = 0

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
			self.total_records,		# 8
		)
		bdata  += struct.pack(self.STRUCT_STR, *dataset)

		return bdata


	def unpack(self, bdata):
		dataset = struct.unpack(self.STRUCT_STR, bdata)

		self.dict_start = dataset[4]
		self.dict_size = dataset[5]

		self.data_start = dataset[6]
		self.data_size = dataset[7]

		self.total_records = dataset[8]



	def __str__(self):
		
		text = "dict_start: {} \ndict_size: {} \ndata_start: {} \ndata_size: {} \n".format(self.dict_start, self.dict_size, self.data_start, self.data_size)
		text += "total_records: {}".format(self.total_records)

		return text


	def print_header(self):
		text = "="*30 + "\n"
		text += "{:<16}: {:>12}\n".format("data_start", self.data_start)
		text += "{:<16}: {:>12}\n".format("data_size", self.data_size)
		text += "\n"
		text += "{:<16}: {:>12}\n".format("dict_start", self.dict_start)
		text += "{:<16}: {:>12}\n".format("dict_size", self.dict_size)
		text += "\n"
		text += "{:<16}: {:>12}\n".format("total_records", self.total_records)

		text += "="*30 


		print(text)