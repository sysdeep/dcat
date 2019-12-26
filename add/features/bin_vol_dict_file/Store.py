#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import os.path
import gzip

from Header import Header
from Dict import Dict
from Data import Data, DataRecord

"""
dict_start: 3582 
dict_size: 2080 
data_start: 32 
data_size: 3550


data writed, cur pos:  3582
"""

class Store(object):
	def __init__(self):
		
		self.header = Header()
		self.fdata = Data()
		self.fdict = Dict()

		self.__fd = None





	def make_db(self, scan_path, out_file):
		print("make_db")
		print(scan_path)
		print(out_file)

		self.__fd = open(out_file, "wb")
		self.__fd.seek(Header.SIZE)



		#--- write files data
		# fdict = []

		self.__start_scan(scan_path, self.__fd, self.fdict)


		end_of_data_addr = self.__fd.tell()

		print("data writed, cur pos: ", self.__fd.tell())




		bin_fdict = self.fdict.pack()


		

		self.__fd.write(bin_fdict)


		self.header.data_start = Header.SIZE
		self.header.data_size = end_of_data_addr - Header.SIZE
		self.header.dict_start = end_of_data_addr
		self.header.dict_size = self.fdict.get_bdata_size()
		print(self.header)

		bin_header = self.header.pack()
		self.__fd.seek(0)
		self.__fd.write(bin_header)
		self.__fd.close()
		self.__fd = None

		# header = Header()
		# fdict = Dict()
		# fdata = Data()

		# self.__start_scan(scan_path, fdata)


		# print(len(fdata.records))

		# #--- make dict
		# for record in fdata.records:
		# 	fdict.append_record(record.fid, record.pid)

		# print(len(fdict.records_map))



		# #--- update header data
		# header.dict_start = Header.SIZE
		# header.dict_size = fdict.get_bdata_size()

		# header.data_start = Header.SIZE + header.dict_size


		# # fdata_bin = fdata.pack()
		# # header.data_size = len(fdata_bin)


		# #--- 
		# fdata_bin = b""
		# # fdata_start = header.data_start
		# fdata_start = 0
		# for record in fdata.records:
		# 	rb = record.pack()

		# 	#--- update dict addr
		# 	fdict.set_addr(record.fid, fdata_start, len(rb))

		# 	fdata_bin += rb
		# 	fdata_start += len(rb)

		# header.data_size = len(fdata_bin)



		# # flat: 1496, gzip: 8182
		# # gzip_fdata_bin = gzip.compress(fdata_bin,9)

		# # print("-"*80)
		# # print("flat: {:>4}, gzip: {:>4}".format(len(gzip_fdata_bin), len(fdata_bin)))
		# # print("-"*80)

		# #--- make binary
		# bdata = b""
		# bdata += header.pack()
		# bdata += fdict.pack()
		# bdata += fdata_bin
		



		# #--- write file
		# with open(out_file, "wb") as fd:
		# 	fd.write(bdata)


	# def __start_scan(self, scan_path, fdata: Data):
	# 	Store.rescan(scan_path, fdata, 0)

	def __start_scan(self, scan_path, fd, fdict: Dict):
		
		
		
		Store.rescan(scan_path, fd, fdict, self.fdata, 0)



	@staticmethod
	def rescan(spath, fd, fdict: Dict, fdata: Data, parent_id):
		for f in os.listdir(spath):

			full_path = os.path.join(spath, f)

			if os.path.isfile(full_path):
				record = fdata.append_file(f, parent_id)
				brecord = record.pack()

				#--- make index
				curr_pos = fd.tell()
				fdict.append_record(record.fid, record.pid, curr_pos, len(brecord))

				#--- write bdata
				fd.write(brecord)

			else:
				record = fdata.append_dir(f, parent_id)
				brecord = record.pack()

				#--- make index
				curr_pos = fd.tell()
				fdict.append_record(record.fid, record.pid, curr_pos, len(brecord))

				#--- write bdata
				fd.write(brecord)



				Store.rescan(full_path, fd, fdict, fdata, record.fid)







	def read_db(self, file_path):
		print("read_db")
		print(file_path)

		#--- open file
		with open(file_path, "rb") as fd:
			
			#--- header
			bheader = fd.read(Header.SIZE)
			header = Header(bheader)
			print(header)

			#--- dict
			fd.seek(header.dict_start)
			bdict = fd.read(header.dict_size)
			fdict = Dict(bdict)
			# for r in fdict.records_map.values():
			# 	print(r)
			

			#--- data
			# for r in fdict.records_map.values():
			# 	if r.pid == 0:
			# 		# print(r.fid, r.pid)
			# 		start = r.daddr
			# 		size = r.dsize
			# 		fd.seek(start)
			# 		bfile_data = fd.read(size)
			# 		record = DataRecord(bfile_data)
			# 		print(record)

			Store.reprint(fd, fdict, 0, 0)


			# bdata = fd.read(header.data_size)
			# fdata = Data(bdata)

			# print()
			# print("root files: ")
			# for r in fdict.records_map.values():
			# 	if r.pid == 0:
			# 		ff = fdata.get_record(r.daddr, r.dsize)
			# 		print(ff)


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
					Store.reprint(fd, fdict, r.fid, ind+1)