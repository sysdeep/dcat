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
from tools import dtimeit, ETimer


FILES_LIST = []

class Writer(object):
	def __init__(self, scan_path, out_file):
		self.scan_path = scan_path
		self.out_file = out_file

		self.header = Header()
		self.fdict = Dict()


	def start(self):
		fd = open(self.out_file, "wb")
		fd.seek(Header.SIZE)

		etimer = ETimer()
		# Writer.rescan(self.scan_path, fd, self.fdict, 0, 1)
		self.__start_scan(self.scan_path, fd, self.fdict, 0, 1)
		etimer.elapsed("finish scan")

		end_of_data_addr = fd.tell()

		print("data writed, cur pos: ", end_of_data_addr)
		print("files: ", self.fdict.records_count)

		etimer.elapsed("start pack dict")
		bin_fdict = self.fdict.pack()
		etimer.elapsed("finish pack dict")
		# print(len(bin_fdict))

		# etimer.elapsed("start pack files")
		# bbb = b""
		# vvv = []
		# for r in FILES_LIST:
		# 	# bbb += 
		# 	vvv.append(r.pack())

		# bbb.join(vvv)
		# etimer.elapsed("finish pack files")


		fd.write(bin_fdict)


		self.header.data_start = Header.SIZE
		self.header.data_size = end_of_data_addr - Header.SIZE
		self.header.dict_start = end_of_data_addr
		self.header.dict_size = self.fdict.get_bdata_size()
		self.header.total_records = self.fdict.records_count

		self.header.print_header()

		bin_header = self.header.pack()
		fd.seek(0)
		fd.write(bin_header)

		fd.close()


	@dtimeit
	def __start_scan(self, scan_path, fd, fdict: Dict, parent_id, last_id):
		Writer.rescan(scan_path, fd, fdict, parent_id, last_id)



	@staticmethod
	def rescan(scan_path, fd, fdict: Dict, parent_id, last_id):

		
		fid = last_id

		for f in os.listdir(scan_path):
		
			full_path = os.path.join(scan_path, f)
			
			
			if os.path.isfile(full_path):
				st = os.stat(full_path)		
				record = Writer.make_file(f, parent_id, fid, st)
				brecord = record.pack()

				#--- make index
				curr_pos = fd.tell()
				fdict.append_record(record.fid, record.pid, curr_pos, len(brecord))

				#--- write bdata
				fd.write(brecord)
				
				fid += 1

			elif os.path.isdir(full_path):
				st = os.stat(full_path)	
				record = Writer.make_dir(f, parent_id, fid, st)
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
	def make_file(name, pid, fid, st):
		return Writer.make_ffile(name, pid, fid, st, 1)


	@staticmethod
	def make_dir(name, pid, fid, st):
		return Writer.make_ffile(name, pid, fid, st, 2)


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
