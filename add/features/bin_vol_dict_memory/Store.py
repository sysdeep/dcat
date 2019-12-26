#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import os.path
import gzip

from Header import Header
from Dict import Dict
from Data import Data



class Store(object):
	def __init__(self):
		pass



	def make_db(self, scan_path, out_file):
		print("make_db")
		print(scan_path)
		print(out_file)

		header = Header()
		fdict = Dict()
		fdata = Data()

		self.__start_scan(scan_path, fdata)


		print(len(fdata.records))

		#--- make dict
		for record in fdata.records:
			fdict.append_record(record.fid, record.pid)

		print(len(fdict.records_map))



		#--- update header data
		header.dict_start = Header.SIZE
		header.dict_size = fdict.get_bdata_size()

		header.data_start = Header.SIZE + header.dict_size


		# fdata_bin = fdata.pack()
		# header.data_size = len(fdata_bin)


		#--- 
		fdata_bin = b""
		# fdata_start = header.data_start
		fdata_start = 0
		for record in fdata.records:
			rb = record.pack()

			#--- update dict addr
			fdict.set_addr(record.fid, fdata_start, len(rb))

			fdata_bin += rb
			fdata_start += len(rb)

		header.data_size = len(fdata_bin)



		# flat: 1496, gzip: 8182
		# gzip_fdata_bin = gzip.compress(fdata_bin,9)

		# print("-"*80)
		# print("flat: {:>4}, gzip: {:>4}".format(len(gzip_fdata_bin), len(fdata_bin)))
		# print("-"*80)

		#--- make binary
		bdata = b""
		bdata += header.pack()
		bdata += fdict.pack()
		bdata += fdata_bin
		



		#--- write file
		with open(out_file, "wb") as fd:
			fd.write(bdata)


	def __start_scan(self, scan_path, fdata: Data):
		Store.rescan(scan_path, fdata, 0)



	@staticmethod
	def rescan(spath, fdata: Data, parent_id):
		for f in os.listdir(spath):

			full_path = os.path.join(spath, f)

			if os.path.isfile(full_path):
				fdata.append_file(f, parent_id)
			else:
				pid = fdata.append_dir(f, parent_id)

				Store.rescan(full_path, fdata, pid)







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
			bdict = fd.read(header.dict_size)
			fdict = Dict(bdict)
			# for r in fdict.records_map.values():
			# 	print(r)
			# print(fdict)

			#--- data
			bdata = fd.read(header.data_size)
			fdata = Data(bdata)

			print()
			print("root files: ")
			for r in fdict.records_map.values():
				if r.pid == 0:
					ff = fdata.get_record(r.daddr, r.dsize)
					print(ff)


