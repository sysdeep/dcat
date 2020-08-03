#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
from enum import Enum
import time

DET = "-"*10

class Sections(Enum):
	header = 0
	body = 1




class Record(object):
	def __init__(self):
		self.name = ""
		self.uuid = ""
		self.parent = ""

		self.childrens = []


	def append(self, ch):
		self.childrens.append(ch)


def parse_record(line: str) -> Record:
	try:
		fields = line.split("|")
	except Exception as e:
		print(e)
		return None
	
	r = Record()
	r.name = fields[0]
	r.uuid = fields[10]
	r.parent = fields[9]
	
	return r







class Volume(object):
	def __init__(self, full_path):
		self.path = full_path
		
		self.name = "undefined"
		
		
		self.__tree = []
		self.__tmap = {}
		self.__roots = []
		
		
	def read_header(self):
		fd = gzip.open(self.path, "rt", encoding="utf-8")
		
		sheader = []
		section = Sections.header
		c = 1000
		while True:
		
			line = fd.readline().strip()
			if not line:
				print("null line")
				break
			
			if section == Sections.header:
				if line == DET:
					break
				else:
					sheader.append(line)
			
			
			c -= 1
			if c < 0:
				print("emerg")
				break
			
		fd.close()


		for line in sheader:
			print(line)
			chunks = line.split(":")
			
			if chunks[0] == "name":
				self.name = chunks[1]
				break



	def read_body(self):
		self.__tree = []
		self.__tmap = {}
		fd = gzip.open(self.path, "rt", encoding="utf-8")
		
		t1 = time.time()
		
		section = Sections.header
		c = 10000000000
		while True:
		
			line = fd.readline().strip()
			if not line:
				print("null line")
				break
			
			if section == Sections.header:
				if line == DET:
					section = Sections.body
				else:
					# pass header
					pass
			elif section == Sections.body:
				# print(line)
				
				record = parse_record(line)
				# self.__tree.append(record)
				
				self.__tmap[record.uuid] = record
				if record.parent == "0":
					self.__roots.append(record)
			else:
				pass
				
			
			
			
			
			c -= 1
			if c < 0:
				print("emerg")
				break
		print("*"*20)
		print("files: ", c)
		print("*"*20)
		fd.close()
		
		
		t2 = time.time()
		
		print("parse body time: ", t2-t1)
		
		
		self.__link()


	def __link(self):
		for r in self.__tmap.values():
			if r.parent == "0":
				continue
			
			parent_node = self.__tmap.get(r.parent)
			if parent_node:
				parent_node.append(r)
			


	def get_root(self) -> list:
		
		# return [r for r in self.__tree if r.parent == "0"]
		return self.__roots
	