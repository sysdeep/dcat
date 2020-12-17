#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
from enum import Enum
import struct
import datetime
import time
from io import BytesIO
from .BReader import BReader

from .VolumeHeader import VolumeHeader

def ushort2(v: bytes) -> int:
	return struct.unpack("<H", v)[0]

def uint4(v: bytes) -> int:
	return struct.unpack("<I", v)[0]

def ulong8(v: bytes) -> int:
	return struct.unpack("<Q", v)[0]

def timeit(func):
	def timed(*args, **kwargs):
		ts = time.time()
		result = func(*args, **kwargs)
		te = time.time()

		print("timeit: ", te - ts)
		return result

	return timed


DET = "-"*10

class Sections(Enum):
	header = 0
	body = 1


#
#
# class Record(object):
# 	def __init__(self):
# 		self.name = ""
# 		self.uuid = ""
# 		self.parent = ""
# 		self.ftype = 0				# 0-dir, 1-file
#
# 		self.childrens = []
#
#
# 	def append(self, ch):
# 		self.childrens.append(ch)

#
# def parse_record(line: str) -> Record:
# 	try:
# 		fields = line.split("|")
# 	except Exception as e:
# 		print(e)
# 		return None
#
# 	r = Record()
# 	r.name = fields[0]
# 	r.uuid = fields[10]
# 	r.parent = fields[9]
#
# 	return r





class Header:
	def __init__(self):
		self.magic = 0
		self.version = 0
		self.icon_id = 0
		self.created= 0
		self.records_len = 0
		self.name = ""
		self.path = ""
		self.description = ""
		
		self.section_table_len = 0
		self.section_text_len = 0
		
	def unpack(self, bdata: bytes):
		reader = BReader(bdata)
	
		#--- [created](8)
		created = reader.read_ulong()
		
		#--- [icon](2)
		self.icon_id = reader.read_ushort()
		
		#--- [records](8)
		self.records_len = reader.read_ulong()
		
		self.section_table_len = reader.read_ulong()
		self.section_text_len = reader.read_ulong()
		
		
		
		#--- [name]
		self.name = reader.read_string()
		
		#--- [scan_path]
		self.path = reader.read_string()
		
		#--- [description]
		self.description = reader.read_string()
	
	
		self.created = datetime.datetime.fromtimestamp(created)
		
	def print_header(self):
		
		print("=== header ===")
		print("volume name: ", self.name)
		print("volume path: ", self.path)
		print("created: ", self.created)
		print("icon: ", self.icon_id)
		print("total records: ", self.records_len)
		print("description: ", self.description)
		print("s data len: ", self.section_table_len)
		print("t data len: ", self.section_text_len)
		print("=== header ===")
	
	
class Record:
	def __init__(self):
		self.ftype = 0			# 0
		self.size = 0			# 1
		self.ctime = 0			# 2
		self.rights = 0			# 3
		self.uid = 0			# 4
		self.parent_id = 0		# 5
		self.name_pos = 0		# 6
		self.name_size = 0		# 7
		
		
	def unpack(self, bdata: bytes):
		row_tuple = struct.unpack("<HQQHIIII", bdata)
		self.ftype = row_tuple[0]
		self.size = row_tuple[1]
		self.ctime = row_tuple[2]
		self.right = row_tuple[3]
		self.uid = row_tuple[4]
		self.parent_id = row_tuple[5]
		self.name_pos = row_tuple[6]
		self.name_size = row_tuple[7]



	def pack(self) -> bytes:

		row_tuple = (self.ftype, self.size, self.ctime, self.right, self.uid, self.parent_id, self.name_pos)


		bdata = struct.pack("<HQQHIII", *row_tuple)
		return bdata
		
		
class Records:
	# RECORD_LEN = 32			# длина бинарных данных 1 записи
	RECORD_LEN = 36			# длина бинарных данных 1 записи
	def __init__(self):
		self.__buffer = BytesIO()
		self.items_count = 0
		self.items = []
	
	def set_bdata(self, bdata: bytes):
		self.__buffer.write(bdata)
	
	@timeit
	def unpack(self):
		
		
		
		for i in range(self.items_count):
			pos = self.RECORD_LEN * i
			self.__buffer.seek(pos)
			
			b_row = self.__buffer.read(self.RECORD_LEN)
			
			record = Record()
			record.unpack(b_row)
			
			
			self.items.append(record)
	
	
	
	def pack(self) -> BytesIO:
		buffer = BytesIO()

		for record in self.items:
			buffer.write(record.pack())
		
		return buffer
	
	
class Texts:
	def __init__(self):
		self.__buffer = BytesIO()
	
	def set_bdata(self, bdata: bytes):
		# print("text data len: ", len(bdata))
		self.__buffer.write(bdata)
	
	
	def get_item(self, pos):
		# print("pos", pos)
		self.__buffer.seek(pos)
		
		blen = self.__buffer.read(2)
		
		
		str_len = struct.unpack("<H", blen)[0]
		# print("--", str_len)
		
		str_bdata = self.__buffer.read(str_len)
		
		return str_bdata.decode("utf-8")


	def get_item_v2(self, pos, size):
		# print("pos", pos)
		self.__buffer.seek(pos)
		
		
		str_bdata = self.__buffer.read(size)
		
		return str_bdata.decode("utf-8")
	
	
	
	
	
	
	
class VRecord:
	"""полный набор данных записи - формируется налету"""
	def __init__(self):
		self.ftype = 0
		self.name = ""
		self.uid = 0
	

class Volume(object):
	def __init__(self, full_path):
		self.path = full_path
		
		self.name = "undefined"
		
		self.__body_start = 0
		self.__magic = 0
		self.__total_records = 0
		
		self.__tree = []
		self.__tmap = {}
		self.__roots = []
		
		
		self.volume_header = VolumeHeader()


		self.records = Records()
		self.texts = Texts()
		


	@staticmethod
	@timeit
	def test_unpack_texts(records, texts):
		print("unpack all texts")
		for r in records:
			name = texts.get_item_v2(r.name_pos, r.name_size)
			r.qqqname = name
			# print(name)


	# @staticmethod
	# @timeit
	# def test_unpack_texts(records, texts):
	# 	print("unpack all texts")
	# 	for r in records:
	# 		name = texts.get_item(r.name_pos)
	# 		r.qqqname = name
	# 		# print(name)

		
	def load(self):
		fd = gzip.open(self.path, "rb")
		
		fd.seek(0, 2)			# end
		data_size = fd.tell()
		print("data size: ", data_size)					# 2184
		fd.seek(0)
		
		#--- [magic](2)
		self.__magic = ushort2(fd.read(2))
		print("-"*10)
		print("magic: ", self.__magic)
		print("-"*10)
	
		#--- [version](2)
		version = ushort2(fd.read(2))
		print("version: ", version)
	
		#--- [header_len](2)
		header_len = ushort2(fd.read(2))
		print("header_len: ", header_len)
	
		#--- [header_struct]
		header_data = fd.read(header_len)
		
		
		
		self.volume_header.unpack(header_data)
		self.volume_header.print_header()
		
		# pos = 2 + 2 + 2 + header_len
		#
		# fd.seek(pos)
		
		#--- records
		self.records.items_count = self.volume_header.records_len
		self.records.set_bdata(fd.read(self.volume_header.section_table_len))
		self.records.unpack()
		
		
		#--- texts
		section_texts = fd.read(self.volume_header.section_text_len)
		print("section_texts need read:", self.volume_header.section_text_len)
		print("section_texts readed len:", len(section_texts))
		self.texts.set_bdata(section_texts)
		


		self.test_unpack_texts(self.records.items, self.texts)



		# self.__total_records = self.__un_header(header_data)
		
		# #--- [magic](2)
		# magic = ushort2(fd.read(2))
		# print("-"*10)
		# print("magic: ", magic)
		# print("-"*10)
		
		
		# self.__body_start = (2 * 4) + header_len
		
		
		
		
		
		
		# sheader = []
		# section = Sections.header
		# c = 1000
		# while True:
		#
		# 	line = fd.readline().strip()
		# 	if not line:
		# 		print("null line")
		# 		break
		#
		# 	if section == Sections.header:
		# 		if line == DET:
		# 			break
		# 		else:
		# 			sheader.append(line)
		#
		#
		# 	c -= 1
		# 	if c < 0:
		# 		print("emerg")
		# 		break
		#
		# fd.close()
		#
		#
		# for line in sheader:
		# 	print(line)
		# 	chunks = line.split(":")
		#
		# 	if chunks[0] == "name":
		# 		self.name = chunks[1]
		# 		break





	@timeit
	def get_vrecords(self, parent_id: int) -> list:
		"""получить список готовых записей"""
		print("get vrecords")
		result = []
		
		for r in self.records.items:
			if r.parent_id == parent_id:
			
				# print(r.name_pos)
				#
				# name = self.texts.get_item(r.name_pos)
				# print(name)
				
				vr = VRecord()
				vr.ftype = r.ftype
				# vr.name = self.texts.get_item(r.name_pos)
				vr.name = self.texts.get_item_v2(r.name_pos, r.name_size)
				vr.uid = r.uid
				result.append(vr)
		
		return result



	def rm_node(self, node: VRecord) -> bool:


		self.save()
		return True


	def save(self):
		
		

		volume_header_buffer = self.volume_header.pack()
		print(volume_header_buffer)

		records_buffer = self.records.pack()








	# def read_body(self):
	# 	print("read body of: ", self.name)
	# 	print("files to read: ", self.__total_records)
	# 	self.__roots = []
	# 	self.__tmap = {}
		
	# 	fd = gzip.open(self.path, "rb")
	# 	fd.seek(self.__body_start)
		
	# 	t1 = time.time()
		
	# 	current_file = 0
	# 	while True:
	# 		#--- [row_len](2)
	# 		try:
	# 			chunk = fd.read(2)
	# 		except Exception as e:
	# 			print(e)
	# 			break
	
	# 		if not chunk:
	# 			break
	
	# 		row_len = ushort2(chunk)
	# 		if row_len == self.__magic:
	# 			print("last magic!!! - done")
	# 			break
	# 		#--- [row_struct]
	# 		row_data = fd.read(row_len)
	# 		record = self.__un_row(row_data)		# TODO
	# 		# record = Record()
	# 		# record.name = "q1"
	# 		# record.parent_id = 0
	# 		# record.uuid = 234
			
	# 		self.__tmap[record.uuid] = record
	# 		if record.parent == 0:
	# 			self.__roots.append(record)
	
	# 		current_file += 1
	
	# 		if current_file > self.__total_records:
	# 			print("ERROR!!!")
	# 			print("processed records > total records - break")
	# 			print(current_file, " > ", self.__total_records)
	# 			break
		

	# 	print("read files: ", current_file)

	# 	fd.close()
	# 	t2 = time.time()
		
	# 	print("parse body time: ", t2-t1)
		
	# 	self.__link()

	# 	# print("tmap len: ", len(self.__tmap))

	# @timeit
	# def __link(self):
	# 	for r in self.__tmap.values():
	# 		if r.parent == 0:
	# 			continue
			
			
	# 		parent_node = self.__tmap.get(r.parent)
	# 		if parent_node:
	# 			parent_node.append(r)
	# 		else:
	# 			print("node not found...")
			


	# def get_root(self) -> list:
		
	# 	# return [r for r in self.__tree if r.parent == "0"]
	# 	return self.__roots
	
	
	
	
	# def __un_header(self, bdata) -> int:
	# 	reader = BReader(bdata)
	
	# 	#--- [created](8)
	# 	created = reader.read_ulong()
		
	# 	#--- [icon](2)
	# 	icon = reader.read_ushort()
		
	# 	#--- [records](8)
	# 	records = reader.read_ulong()
		
	# 	s_data_len = reader.read_ulong()
	# 	t_data_len = reader.read_ulong()
		
		
		
	# 	#--- [name]
	# 	name = reader.read_string()
		
	# 	#--- [scan_path]
	# 	path = reader.read_string()
		
	# 	#--- [description]
	# 	description = reader.read_string()
	
	
	# 	created_s = datetime.datetime.fromtimestamp(created)
	# 	print(created_s)
	
	# 	print("=== header ===")
	# 	print("volume name: ", name)
	# 	print("volume path: ", path)
	# 	print("created: ", created)
	# 	print("icon: ", icon)
	# 	print("total records: ", records)
	# 	print("description: ", description)
	# 	print("s data len: ", s_data_len)
	# 	print("t data len: ", t_data_len)
	
	
	
	# 	self.name = name
	
	# 	return records
	
	
	
	# def __un_row(self, bdata) -> Record:


	# 	# res = struct.unpack("<H", bdata[0:2])
	# 	# res = struct.unpack("<Q", bdata[2:2+8])
	# 	# res = struct.unpack("<Q", bdata[2+8:2+8+8])
	# 	# res = struct.unpack("<H", bdata[2+8+8:2+8+8+2])
	# 	# res = struct.unpack("<I", bdata[2+8+8+2:2+8+8+2+4])
	# 	# res = struct.unpack("<I", bdata[2+8+8+2+4:2+8+8+2+4+4])

	# 	# r = Record()
	# 	# r.name = "name"
	# 	# r.uuid = 1
	# 	# r.parent = 0
	# 	# r.ftype = 1

	# 	# return r


	# 	reader = BReader(bdata)
	
	# 	#--- type 			[ushort 2]	- тип файла(каталог/файл...)
	# 	row_type = reader.read_ushort()
		
	# 	#--- size 			[ulong 8]	- размер записи
	# 	file_size = reader.read_ulong()
		
	# 	#--- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
	# 	created = reader.read_ulong()
		
	# 	#--- rights 		[ushort 2]	- код доступа(unix 777)
	# 	rights = reader.read_ushort()
		
	# 	#--- fid 			[uint 4]	- id записи
	# 	fid = reader.read_uint()
		
	# 	#--- pid 			[uint 4]	- id родителя(0 - корень)
	# 	pid = reader.read_uint()				# TODO
		
	# 	#--- name 			[bstr]		- название
	# 	# name = reader.read_string()
	# 	name = "Name"
	# 	#--- description 	[bstr]		- произвольное описание
	# 	# description = reader.read_string()
	
	# 	# print("\t", name)
	
	
	# 	r = Record()
	# 	r.name = name
	# 	r.uuid = fid
	# 	r.parent = pid
	# 	r.ftype = row_type
		
	# 	return r