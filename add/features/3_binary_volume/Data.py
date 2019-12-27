#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct
import gzip

class DataRecord(object):
	STRUCT_STR = "<IIIIIIIfffI"
	HEAD_SIZE = 44
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
			self.fid,			# 0
			self.pid,			# 1

			self.ftype,			# 2
			self.size,			# 3

			self.st_mode,		# 4
			self.st_uid,		# 5
			self.st_gid,		# 6

			self.st_ctime,		# 7
			self.st_atime,		# 8
			self.st_mtime,		# 9

			name_len,			# 10

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
		
		
		self.fid = head_dataset[0]
		self.pid = head_dataset[1]
		
		self.ftype = head_dataset[2]
		self.size = head_dataset[3]

		self.st_mode = head_dataset[4]
		self.st_uid = head_dataset[5]
		self.st_gid = head_dataset[6]

		self.st_ctime = head_dataset[7]
		self.st_atime = head_dataset[8]
		self.st_mtime = head_dataset[9]

		name_len = head_dataset[10]

		bname = bdata[self.HEAD_SIZE: len(bdata) + 1]
		
		self.name = bname.decode(encoding="utf-8")


	def unpack_header(self, bdata):
		
		bhead = bdata[0:self.HEAD_SIZE]
		head_dataset = struct.unpack(self.STRUCT_STR, bhead)
		
		
		self.fid = head_dataset[0]
		self.pid = head_dataset[1]
		
		self.ftype = head_dataset[2]
		self.size = head_dataset[3]

		self.st_mode = head_dataset[4]
		self.st_uid = head_dataset[5]
		self.st_gid = head_dataset[6]

		self.st_ctime = head_dataset[7]
		self.st_atime = head_dataset[8]
		self.st_mtime = head_dataset[9]

		name_len = head_dataset[10]

		return name_len
		
	def unpack_name(self, bname):
		self.name = bname.decode(encoding="utf-8")

	def __str__(self):
		return "{}".format(self.name)















class Data(object):
	def __init__(self, bdata=None):
		
		self.parent_id = 0
		self.current_id = 1

		self.records = []

		if bdata:
			self.unpack(bdata)





	def get_record(self, start, size):
		brecord = self.__bdata[start : start + size]

		record = DataRecord(brecord)
		return record



	def pack(self):

		bdata_list = []
		for r in self.records:
			bdata_list.append(r.pack())

		bdata = b"".join(bdata_list)
		return bdata

	def unpack(self, bdata):
		pos = 0
		while pos < len(bdata):
			start = pos
			end = start + DataRecord.HEAD_SIZE
			rec_header = bdata[start : end]
			# print(len(rec_header))
			# print(start, end)
			rec = DataRecord()
			name_len = rec.unpack_header(rec_header)
			
			end_name = end + name_len
			bin_name = bdata[end : end_name]
			# print(bin_name)
			rec.unpack_name(bin_name)

			self.records.append(rec)
			pos = end_name



	def append_file(self, name, pid, fid, st):
		record = Data.make_ffile(name, pid, fid, st, 1)
		self.records.append(record)
		return record

	def append_dir(self, name, pid, fid, st):
		record = Data.make_ffile(name, pid, fid, st, 2)
		self.records.append(record)
		return record



	@staticmethod
	def make_ffile(name, pid, fid, st, ftype):
		record = DataRecord()
		record.name = name
		record.ftype = ftype
		record.pid = pid
		record.fid = fid

		record.size = st.st_size
		record.st_mode = st.st_mode

		record.st_uid = st.st_uid
		record.st_gid = st.st_gid

		record.st_ctime = st.st_ctime
		record.st_atime = st.st_atime
		record.st_mtime = st.st_mtime
	
		return record