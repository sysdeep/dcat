#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from Header import Header
from Dict import Dict
from Data import DataRecord


class Reader(object):
	def __init__(self, file_path):
		self.file_path = file_path

		self.__fd = open(file_path, "rb")

		bheader = self.__fd.read(Header.SIZE)
		self.header = Header(bheader)


		self.__fd.seek(self.header.dict_start)
		bdict = self.__fd.read(self.header.dict_size)

		self.fdict = Dict(bdict)


	def print_root_files(self):
		
		for r in self.fdict.records_map.values():
			if r.pid == 0:
				start = r.daddr
				size = r.dsize
				self.__fd.seek(start)
				bfile_data = self.__fd.read(size)
				record = DataRecord(bfile_data)
				print(record.name)


	def print_tree(self):

		Reader.reprint(self.__fd, self.fdict, 0, 0)


	@staticmethod
	def reprint(fd, fdict, parent_id, ind):

		for r in fdict.records_map.values():
			if r.pid == parent_id:
				start = r.daddr
				size = r.dsize
				fd.seek(start)
				bfile_data = fd.read(size)
				record = DataRecord(bfile_data)
				print(ind*"\t" + record.name)
				

				if record.ftype == 2:
					Reader.reprint(fd, fdict, r.fid, ind+1)