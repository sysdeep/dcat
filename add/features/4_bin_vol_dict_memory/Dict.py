#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct

class DictRecord(object):
	SIZE = 16
	def __init__(self, bdata=None):
		self.fid = 0
		self.pid = 0
		self.daddr = 0
		self.dsize = 0

		if bdata:
			self.unpack(bdata)

	#12b
	def pack(self):
		dataset = (
			self.fid,
			self.pid,
			self.daddr,
			self.dsize
		)

		bdata = b""
		bdata  += struct.pack("<IIII", *dataset)
		return bdata

	def unpack(self, bdata):
		dataset = struct.unpack("<IIII", bdata)
		self.fid = dataset[0]
		self.pid = dataset[1]
		self.daddr = dataset[2]
		self.dsize = dataset[3]


	def __str__(self):
		return "fid: {}, pid: {}, addr: {}, size: {}".format(self.fid, self.pid, self.daddr, self.dsize)



class Dict(object):
	def __init__(self, bdata=None):
		self.records_map = {}


		if bdata:
			self.unpack(bdata)
		


	def pack(self):

		bdata = b""
		for record in self.records_map.values():
			bdata += record.pack()

		return bdata


	def unpack(self, bdata):
		
		print(len(bdata) / DictRecord.SIZE)

		for i in range(int(len(bdata) / DictRecord.SIZE)):
			start = i * DictRecord.SIZE
			end = start + DictRecord.SIZE
			brecord = bdata[start : end]
			record = DictRecord(brecord)
			self.records_map[record.fid] = record


	def append_record(self, fid, pid):

		record = DictRecord()
		record.fid = fid
		record.pid = pid

		# self.records.append(record)
		self.records_map[fid] = record
	
	def get_bdata_size(self):
		return len(self.records_map) * DictRecord.SIZE



	def set_addr(self, fid, addr, size):
		record = self.records_map[fid]
		record.daddr = addr
		record.dsize = size



	# def __str__(self):
	# 	return "{}\n".format(len(self.records_map))