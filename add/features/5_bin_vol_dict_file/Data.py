#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
import gzip

class DataRecord(object):
	STRUCT_STR = "<IIIIIfffI"
	HEAD_SIZE = 36
	def __init__(self, bdata=None):

		self.fid = 0
		self.pid = 0



		self.ftype = 1
		self.size = 0
		self.name = ""

		self.st_mode = 0
		self.st_uid = 0
		self.st_gid = 0

		self.st_ctime = 0
		self.st_atime = 0
		self.st_mtime = 0

		# self.__bdata = bdata
		if bdata:
			self.unpack(bdata)

	
	def pack(self):
		
		name_bdata = self.name.encode(encoding="utf-8")
		name_len = len(name_bdata)


		dataset = (
			self.ftype,			# 0
			self.size,			# 1

			self.st_mode,		# 2
			self.st_uid,		# 3
			self.st_gid,		# 4

			self.st_ctime,		# 5
			self.st_atime,		# 6
			self.st_mtime,		# 7

			name_len,			# 8

		)

		
		main_bdata = struct.pack(self.STRUCT_STR, *dataset)
		
		bdata = b"".join([main_bdata, name_bdata])

		# flat:  134, gip:  135
		# flat:   90, gip:  103
		# flat:   69, gip:   83
		# flat:   30, gip:   45
		# flat:   17, gip:   32
		# gzip_bdata = gzip.compress(bdata)
		# print("flat: {:>4}, gip: {:>4}".format(len(bdata), len(gzip_bdata)))

		return bdata



	def unpack(self, bdata):
		
		bhead = bdata[0:self.HEAD_SIZE]
		head_dataset = struct.unpack(self.STRUCT_STR, bhead)
		self.ftype = head_dataset[0]
		self.size = head_dataset[1]

		self.st_mode = head_dataset[2]
		self.st_uid = head_dataset[3]
		self.st_gid = head_dataset[4]

		self.st_ctime = head_dataset[5]
		self.st_atime = head_dataset[6]
		self.st_mtime = head_dataset[7]

		name_len = head_dataset[8]

		bname = bdata[self.HEAD_SIZE: len(bdata) + 1]
		
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