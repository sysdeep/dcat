#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""
import os
import os.path
import gzip

from Header import Header
from Data import DataRecord, Data
from tools import dtimeit, ETimer



class Writer(object):
	def __init__(self, scan_path, out_file):
		self.scan_path = scan_path
		self.out_file = out_file

		self.header = Header()
		self.fdata = Data()


	def start(self):
		# fd = open(self.out_file, "wb")
		# fd.seek(Header.SIZE)

		etimer = ETimer()
		Writer.rescan(self.scan_path, self.fdata, 0, 1)
		etimer.elapsed("finish scan")

		# end_of_data_addr = fd.tell()

		# print("data writed, cur pos: ", end_of_data_addr)
		print("files: ", len(self.fdata.records))

		# etimer.elapsed("start pack dict")
		# bin_fdict = self.fdict.pack()
		# etimer.elapsed("finish pack dict")
		

		# fd.write(bin_fdict)

		bin_data = self.fdata.pack()

		self.header.data_start = Header.SIZE
		self.header.data_size = len(bin_data)
		# self.header.dict_start = end_of_data_addr
		# self.header.dict_size = self.fdict.get_bdata_size()
		self.header.total_records = len(self.fdata.records)

		self.header.print_header()

		bin_header = self.header.pack()
		# fd.seek(0)
		# fd.write(bin_header)

		# fd.close()

		#--- start write
		with gzip.open(self.out_file, "wb") as fd:
			fd.write(bin_header)
			fd.write(bin_data)

	

	@staticmethod
	def rescan(scan_path, fdata, parent_id, last_id):

		
		fid = last_id

		for f in os.listdir(scan_path):
		
			full_path = os.path.join(scan_path, f)
			
			
			if os.path.isfile(full_path):
				st = os.stat(full_path)		
				record = fdata.append_file(f, parent_id, fid, st)
				
				fid += 1

			elif os.path.isdir(full_path):
				st = os.stat(full_path)	
				record = fdata.append_dir(f, parent_id, fid, st)

				fid +=1

				fid = Writer.rescan(full_path, fdata, record.fid, fid)
			else:
				pass
			
		return fid




