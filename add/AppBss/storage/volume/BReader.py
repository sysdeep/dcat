#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct


class BReader(object):
	def __init__(self, bdata):
		self.bdata = bdata
		self.__ptr = 0
		

	def read_ushort(self) -> int:
		if self.__ptr > len(self.bdata):
			raise("owerflow")

		v = struct.unpack("<H", self.bdata[self.__ptr:self.__ptr+2])[0]
		self.__ptr += 2
		return v

	def read_uint(self) -> int:
		if self.__ptr > len(self.bdata):
			raise("owerflow")

		v = struct.unpack("<I", self.bdata[self.__ptr:self.__ptr+4])[0]
		self.__ptr += 4
		return v

	def read_ulong(self) -> int:
		if self.__ptr > len(self.bdata):
			raise("owerflow")

		v = struct.unpack("<Q", self.bdata[self.__ptr:self.__ptr+8])[0]
		self.__ptr += 8
		return v

	def read_string(self) -> str:
		if self.__ptr > len(self.bdata):
			raise("owerflow")
		str_len = struct.unpack("<H", self.bdata[self.__ptr:self.__ptr+2])[0]
		self.__ptr += 2

		if self.__ptr > len(self.bdata):
			raise("owerflow")
		result = self.bdata[self.__ptr:self.__ptr+str_len].decode("utf-8")
		self.__ptr += str_len
		
		return result

