#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
import gzip

class DataRecord(object):
	def __init__(self, bdata=None):

		self.fid = 0
		self.pid = 0



		self.ftype = 1
		self.size = 0
		self.name = ""

		# self.__bdata = bdata
		if bdata:
			self.unpack(bdata)

	
	def pack(self):
		
		# 8b
		dataset = (
			self.ftype,
			self.size,
		)

		bdata = b""
		bdata  += struct.pack("<II", *dataset)


		bstr = self.name.encode(encoding="utf-8")
		bdata += bstr

		# flat:  134, gip:  135
		# flat:   90, gip:  103
		# flat:   69, gip:   83
		# flat:   30, gip:   45
		# flat:   17, gip:   32
		# gzip_bdata = gzip.compress(bdata)
		# print("flat: {:>4}, gip: {:>4}".format(len(bdata), len(gzip_bdata)))

		return bdata



	def unpack(self, bdata):
		# print("rbdata len: ", len(bdata))
		bhead = bdata[0:8]
		head_dataset = struct.unpack("<II", bhead)
		self.ftype = head_dataset[0]
		self.size = head_dataset[1]

		bname = bdata[8: len(bdata) + 1]
		# print(bdata)
		self.name = bname.decode(encoding="utf-8")
		

	def __str__(self):
		return "{}".format(self.name)


class Data(object):
	def __init__(self, bdata=None):
		
		self.parent_id = 0
		self.current_id = 1

		self.records = []

		self.__bdata = bdata





	def get_record(self, start, size):
		brecord = self.__bdata[start : start + size]

		record = DataRecord(brecord)
		return record



	def pack(self):

		bdata = b""
		return bdata


	def append_file(self, name, parent_id):
		print("append file: ", name)
		record = DataRecord()
		record.name = name
		record.ftype = 1
		record.pid = parent_id
		record.fid = self.current_id

		# self.records.append(record)

		self.current_id += 1

		# return record.fid
		return record

	def append_dir(self, name, parent_id=0):
		print("append dir: ", name)

		record = DataRecord()
		record.name = name
		record.ftype = 2
		record.pid = parent_id
		record.fid = self.current_id

		# self.records.append(record)

		self.current_id += 1

		# return record.fid
		return record