#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Header import Header
# from Dict import Dict
from Data import DataRecord, Data
import gzip

class Reader(object):
	def __init__(self, file_path):
		self.file_path = file_path


		fd = gzip.open(file_path, "rb")

		bheader = fd.read(Header.SIZE)
		self.header = Header(bheader)

		fd.seek(self.header.data_start)
		bin_data = fd.read(self.header.data_size)

		self.fdata = Data(bin_data)
		fd.close()


	def print_root_files(self):
		

		self.header.print_header()
		
		for record in self.fdata.records:
			# print("{} : {:>8} {:>8}".format(record.name, record.size, record.st_ctime))
			if record.pid == 0:
	# 			start = r.daddr
	# 			size = r.dsize
	# 			self.__fd.seek(start)
	# 			bfile_data = self.__fd.read(size)
	# 			record = DataRecord(bfile_data)
				print("{} : {:>8} {:>8}".format(record.name, record.size, record.st_ctime))


	def print_tree(self):
		print("tree")
		self.header.print_header()

		Reader.reprint(self.fdata, 0, 0)


	@staticmethod
	def reprint(fdata, parent_id, ind):

		for record in fdata.records:
			if record.pid == parent_id:
				print(ind*"\t" + record.name + str(record.ftype))
				

				if record.ftype == 2:
					Reader.reprint(fdata, record.fid, ind+1)