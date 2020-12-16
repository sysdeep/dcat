import gzip
import re
import base64
import struct
import time
import os.path
from io import BytesIO

from .models import VNode
from . import db_worker
from .defs import VOLUME_ICONS, MAGIC, VERSION






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



class RowData:
	def __init__(self):
		self.ftype = 0
		self.size = 0
		self.ctime = 0
		self.rights = 0
		self.uuid = 0
		self.parent_id = 0
		
		self.text_data_pos = 0
		self.text_data_size = 0			# v2
	
	def set_data(self, row_data: dict):
		
		#--- type 			[ushort 2]	- тип файла(каталог - 0/файл - 1)
		self.ftype = row_data["ftype"]
		
		#--- size 			[ulong 8]	- размер записи
		self.size = row_data["size"]
		
		#--- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
		self.ctime = int(row_data["ctime"])
		
		#--- rights 		[ushort 2]	- код доступа(unix 777)
		self.rights = row_data["rights"]
		
		#--- fid 			[uint 4]	- id записи
		# bdata += uint4(0)					# TODO
		self.uuid = row_data["uuid"]
		
		#--- pid 			[uint 4]	- id родителя(0 - корень)
		# bdata += uint4(0)					# TODO
		self.parent_id = row_data["parent_id"]
		
		
	def make(self) -> BytesIO:
		buf = BytesIO()
		
		#--- type 			[ushort 2]	- тип файла(каталог - 0/файл - 1)
		buf.write(ushort2(self.ftype))
		
		#--- size 			[ulong 8]	- размер записи
		buf.write(ulong8(self.size))
		
		#--- ctime 		[ulong 8]	- дата создания файла(unix timestamp)
		buf.write(ulong8(self.ctime))
		
		#--- rights 		[ushort 2]	- код доступа(unix 777)
		buf.write(ushort2(self.rights))
		
		#--- fid 			[uint 4]	- id записи
		buf.write(uint4(self.uuid))
		
		#--- pid 			[uint 4]	- id родителя(0 - корень)
		buf.write(uint4(self.parent_id))
		
		#--- text_data local offset 			[uint 4]
		buf.write(uint4(self.text_data_pos))
		buf.write(uint4(self.text_data_size))		# v2
		
		return buf




class Header:
	def __init__(self):
		self.magic = MAGIC
		self.version = VERSION
		self.icon_id = 0
		self.timestamp = 0
		self.records_len = 0
		self.name = ""
		self.path = ""
		self.description = ""
		
		self.section_table_len = 0
		self.section_text_len = 0
		
		
	def set_vol_info(self, data: dict):
		try:
			time_tuple = time.strptime(data["created"], "%Y-%m-%d %H:%M:%S")
			self.timestamp = int(time.mktime(time_tuple))
		except Exception as e:
			print(e)
			self.timestamp = 0
			
		self.icon_id = VOLUME_ICONS.get(data["vtype"], 14)			# or other
		
		
		#--- [name]
		self.name = data["name"] or ""
		
		#--- [scan_path]
		self.path = data["path"] or ""
		
		#--- [description]
		self.description = data["description"] or ""


	def make(self) -> BytesIO:
		buf = BytesIO()
		
		
	
		#--- [created](8)
		buf.write(ulong8(self.timestamp))
		
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








class NodeConverter:
	def __init__(self, connection, vnode: VNode, dest_path: str):
		self.__connection = connection
		self.__vnode = vnode
		self.__dest_path = dest_path


	def start(self):
		print("start convert: ", self.__vnode.name)

		#--- get all files
		fnodes = db_worker.get_volume_files(self.__connection, self.__vnode.uuid)
		
		files_list = []
		for fnode in fnodes:
			result = fnode.make_data_dict()
			files_list.append(result)

		#--- convert files(fid/pid)
		self.__convert_files(files_list)

		#--- make sections
		sdata, tdata = self.__create_sections(files_list)




		#--- make header
		header = Header()
		header.set_vol_info(self.__vnode.make_data_dict())
		header.records_len = len(files_list)
		header.section_table_len = len(sdata.getbuffer())
		header.section_text_len = len(tdata.getbuffer())
		hdata = header.make()
		


		
		file_name = self.__vnode.name + ".gz"
		file_path = os.path.join(self.__dest_path, file_name)
		fd = gzip.open(file_path, "wb")
		
		magic = ushort2(MAGIC)
		#--- [magic](2)
		fd.write(magic)
		
		#--- [version](2)
		fd.write(ushort2(VERSION))
		
		
		header_len = len(hdata.getbuffer())
		# header = __vol_info(vol_info, len(files_list))
		print("header len: ", header_len)
		#--- [header_len](2)
		fd.write(ushort2(header_len))
		
		# #--- [header_struct]
		# fd.write(header)
		#
		# #--- [magic](2)
		# fd.write(magic)
		#
		
		
		
		
		#--- write header
		fd.write(hdata.getbuffer())
		
		#--- write data
		fd.write(sdata.getbuffer())

		#--- write text
		fd.write(tdata.getbuffer())
		
		
		
		hdata.close()
		sdata.close()
		tdata.close()
		
		
		
		
		# for fdata in files_list:
		#
		# 	try:
		# 		row_data = __format_row(fdata)
		# 	except Exception as e:
		# 		print(e)
		# 		print("+"*10)
		# 		print(fdata)
		# 		print("+"*10)
		# 		break
		#
		# 	#--- [row_len]
		# 	fd.write(ushort2(len(row_data)))
		#
		# 	#--- [row_struct]
		# 	fd.write(row_data)
		#
		#--- [magic](2)
		fd.write(magic)
		
		
		fd.flush()
		fd.close()

		print("done export")


	def __convert_files(self, files: list):
		"""переводим файлы в новую структуру"""
		
		omap = {
			"0"	: 0,
		}			# uuid: new id
		
		
		new_id = 1
		
		#--- fix root parent
		# for row in files:
		# 	if row["parent_id"] == "0":
		# 		row["parent_id"] = 0
		
		#--- update fid
		for row in files:
			omap[row["uuid"]] = new_id
			row["uuid"] = new_id
			new_id += 1
			
		#--- update parents
		for row in files:
			try:
				new_parent_id = omap[row["parent_id"]]
			except:
				print("!!! no found parent in omap")
				continue
				
			row["parent_id"] = new_parent_id






	def __create_sections(self, files_list: list) -> (BytesIO, BytesIO):
		section_data = BytesIO()
		section_text = BytesIO()
		
		
		for fdata in files_list:
			
			text_local_pos = section_text.tell()
			
			
			rd = RowData()
			rd.set_data(fdata)
			rd.text_data_pos = text_local_pos
			
			
			
			
			bname = fdata["name"].encode(encoding="utf-8")
			rd.text_data_size = len(bname)
			
			# td = TextData()
			# td.set_data(fdata)
			
			
			
			
			
			# try:
			# 	row_data = __format_row(fdata)
			# except Exception as e:
			# 	print(e)
			# 	print("+"*10)
			# 	print(fdata)
			# 	print("+"*10)
			# 	break
			#
			#--- [row_len]
			# fd.write(ushort2(len(row_data)))
			
			
			
			# btd = td.make()
			# section_text.write(btd.getbuffer())
			section_text.write(bname)
			
			
			
			
			
			brd = rd.make()
			section_data.write(brd.getbuffer())
			
			
			brd.close()
			# btd.close()


		# section_data.close()
		
		return section_data, section_text