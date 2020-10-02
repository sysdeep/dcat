#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
from io import BytesIO

from .FileHeader import FileHeader
from .VolumeHeader import VolumeHeader



class Volume:
	def __init__(self):
		
		self.file_header = FileHeader()
		self.volume_header = VolumeHeader()
		self.records = []
		
		self.current_path = ""
		
		
	#--- public ---------------------------------------------------------------
	def load(self, volume_path: str):
		"""загрузить базу из файла"""
		self.current_path = volume_path
		fd = gzip.open(self.current_path, "rb")
		
		#--- read file header
		bdata = fd.read(self.file_header.BDATA_SIZE)
		self.file_header.unpack(bdata)
		print(self.file_header)
		
		
		
		#--- read volume header
		b_volume_header = fd.read(self.volume_header.BDATA_SIZE)
		self.volume_header.unpack(b_volume_header)
		
		
		
		#--- read records
		b_records = fd.read(self.volume_header.table_len)
		
		#--- read heap
		b_heap = fd.read(self.volume_header.heap_len)
		__heap = BytesIO(b_heap)
		

		self.volume_header.read_heap(__heap)
		self.volume_header.print_header()
		
		
		
		
		
		
		fd.close()
	
	
	
	def save(self, volume_path: str):
		"""выгрузить базу в файл"""
		
		
		
		__heap = BytesIO()
		
		
		#--- make file header
		b_file_header = self.file_header.pack()
		
		
		#--- make volume header
		self.volume_header.write_heap(__heap)
	
		
		
		#--- make records table
		__buffer = BytesIO()
		for record in self.records:
			record.write_heap(__heap)
			b_record = record.pack()
			__buffer.write(b_record)
			
		
		b_records = __buffer.getbuffer()
		self.volume_header.table_len = len(b_records)
		self.volume_header.records = len(self.records)
		
		
		b_heap = __heap.getbuffer()
		self.volume_header.heap_len = len(b_heap)
		
		
		b_volume_header = self.volume_header.pack()
		
		
		
		
		#--- write
		fd = gzip.open(volume_path, "wb")
		
		fd.write(b_file_header)
		fd.write(b_volume_header)
		fd.write(b_records)
		fd.write(b_heap)
		
		# __heap.close()
		# __buffer.close()
		
		fd.flush()
		fd.close()
	#--- public ---------------------------------------------------------------