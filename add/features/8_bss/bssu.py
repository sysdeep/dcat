#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import re
import time
import struct


def timeit(func):
	def timed(*args, **kwargs):
		ts = time.time()
		result = func(*args, **kwargs)
		te = time.time()

		print("timeit: ", te - ts)
		return result

	return timed


FILE = "Video.bss.gz"
FILE = "Apps.bss.gz"


class BReader(object):
	def __init__(self, bdata):
		self.bdata = bdata
		self.ptr = 0
		self.result = []

	def read_int(self):
		v = struct.unpack("<I", self.bdata[self.ptr:self.ptr+4])[0]
		self.ptr += 4
		self.result.append(v)
		return self

	def read_str(self):
		str_len = struct.unpack("<I", self.bdata[self.ptr:self.ptr+4])[0]
		self.ptr += 4

		result = self.bdata[self.ptr:self.ptr+str_len].decode("utf-8")
		self.ptr += str_len
		self.result.append(result)
		
		return self


def __un_str(bdata) -> str:
	str_len = struct.unpack("<I", bdata[0:4])

	result = bdata[4:].decode("utf-8")
	return result

def __un_header(bdata):
	reader = BReader(bdata)
	reader \
			.read_int() \
			.read_int() \
			.read_int() \
			.read_str() \
			.read_str()

	print(reader.result)
	# ints = struct.unpack("<III", bdata[0:12])
	# print(ints)

	# name = __un_str(bdata[12:])
	# print(name)


def __un_row(bdata):
	reader = BReader(bdata)
	reader.read_int().read_int().read_int().read_int().read_int().read_int()
	reader.read_str().read_str().read_str().read_str().read_str().read_str()

	print(reader.result)

@timeit
def unpack():
	fd = gzip.open(FILE, "rb")

	header_size = struct.unpack("<I", fd.read(4))[0]
	print(header_size)

	bheader = fd.read(header_size)
	__un_header(bheader)

	while True:
		blen = fd.read(4)
		if not blen:
			break
		else:
			row_len = struct.unpack("<I", blen)[0]
			bdata = fd.read(row_len)
			__un_row(bdata)

	

	fd.close()





if __name__ == "__main__":

	unpack()