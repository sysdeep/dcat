# -*- coding: utf-8 -*-
import datetime
import struct
from io import BytesIO

from .BReader import BReader



def ushort2(v) -> bytes:
	return struct.pack("<H", v)

def uint4(v) -> bytes:
	return struct.pack("<I", v)

def ulong8(v) -> bytes:
	return struct.pack("<Q", v)

def pack_str(text: str):
	bstr = text.encode(encoding="utf-8")
	str_len = len(bstr)
	bdata = ushort2(str_len)
	bdata += bstr
	return bdata




class VolumeHeader:
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
		self.created = reader.read_ulong()
		
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
	
	
		# self.created = datetime.datetime.fromtimestamp(created)
		

	def pack(self) -> BytesIO:
		buf = BytesIO()
		
		
	
		#--- [created](8)
		buf.write(ulong8(self.created))
		
		#--- [icon](2)
		buf.write(ushort2(self.icon_id))
		
		#--- [records](8)
		buf.write(ulong8(self.records_len))
		
		
		buf.write(ulong8(self.section_table_len))
		buf.write(ulong8(self.section_text_len))
		
		#--- [name]
		buf.write(pack_str(self.name))
		
		#--- [scan_path]
		buf.write(pack_str(self.path))
		
		#--- [description]
		buf.write(pack_str(self.description))
		
		# buf.close()
		
		return buf


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
	