#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict_start: 3550 
dict_size: 2080 
data_start: 32 
data_size: 3518


data writed, cur pos:  3550
"""
import os
import os.path
# import gzip

from Header import Header
from Dict import Dict
from Data import DataRecord

class Writer(object):
	def __init__(self, scan_path, out_file):
		self.scan_path = scan_path
		self.out_file = out_file

		self.header = Header()
		self.fdict = Dict()


	def start(self):
		fd = open(self.out_file, "wb")
		fd.seek(Header.SIZE)

		Writer.rescan(self.scan_path, fd, self.fdict, 0, 1)

		end_of_data_addr = fd.tell()

		print("data writed, cur pos: ", end_of_data_addr)
		print("files: ", len(self.fdict.records_map))


		bin_fdict = self.fdict.pack()


		fd.write(bin_fdict)


		self.header.data_start = Header.SIZE
		self.header.data_size = end_of_data_addr - Header.SIZE
		self.header.dict_start = end_of_data_addr
		self.header.dict_size = self.fdict.get_bdata_size()

		bin_header = self.header.pack()
		fd.seek(0)
		fd.write(bin_header)

		fd.close()



	@staticmethod
	def rescan(scan_path, fd, fdict: Dict, parent_id, last_id):

		fid = last_id

		for f in os.listdir(scan_path):
		
			full_path = os.path.join(scan_path, f)
			
			if os.path.isfile(full_path):
				record = Writer.make_file(f, parent_id, fid)
				brecord = record.pack()

				#--- make index
				curr_pos = fd.tell()
				fdict.append_record(record.fid, record.pid, curr_pos, len(brecord))

				#--- write bdata
				fd.write(brecord)
				
				fid += 1

			elif os.path.isdir(full_path):
				record = Writer.make_dir(f, parent_id, fid)
				brecord = record.pack()

				#--- make index
				curr_pos = fd.tell()
				fdict.append_record(record.fid, record.pid, curr_pos, len(brecord))

				#--- write bdata
				fd.write(brecord)
				fid +=1

				fid = Writer.rescan(full_path, fd, fdict, record.fid, fid)
			else:
				pass
			
		return fid




	@staticmethod
	def make_file(name, pid, fid):
		# print(fid)
		record = DataRecord()
		record.name = name
		record.ftype = 1
		record.pid = pid
		record.fid = fid

		# record.fid = self.current_id

		# self.records.append(record)

		# self.current_id += 1

		# return record.fid
		return record


	@staticmethod
	def make_dir(name, pid, fid):
		# print(fid)
		record = DataRecord()
		record.name = name
		record.ftype = 2
		record.pid = pid
		record.fid = fid
		
		# record.fid = self.current_id

		# self.records.append(record)

		# self.current_id += 1

		# return record.fid
		return record