
import gzip
from io import BytesIO
from app.lib.logger import log

from .FileWorkerAbstract import FileWorkerAbstract, Volume

class HmapWorker(FileWorkerAbstract):
	def __init__(self):
		pass


	def load(self, model: Volume, file_path: str):
		"""читаем данные из файла"""
		
		# volume = Volume()
		#
		# fd = gzip.open(volume_path, "rb")
		#
		# #--- read file header
		# bdata = fd.read(volume.file_header.BDATA_SIZE)
		# volume.file_header.unpack(bdata)
		# print(volume.file_header)
		#
		#
		#
		# #--- read volume header
		# b_volume_header = fd.read(volume.volume_header.BDATA_SIZE)
		# volume.volume_header.unpack(b_volume_header)
		#
		#
		#
		# #--- read records
		# b_records = fd.read(volume.volume_header.table_len)
		#
		# #--- read heap
		# b_heap = fd.read(volume.volume_header.heap_len)
		# __heap = BytesIO(b_heap)
		#
		#
		# volume.volume_header.read_heap(__heap)
		# volume.volume_header.print_header()
		#
		#
		#
		#
		#
		#
		# fd.close()

		pass






	def save(self, model: Volume, file_path: str):
		"""записываем данные в файл"""
		
		# log.info("запись тома {} в файл: {}".format(volume.volume_header.name, volume_path))
		#
		#
		# __heap = BytesIO()
		#
		#
		# #--- make file header
		# b_file_header = volume.file_header.pack()
		#
		#
		# #--- make volume header
		# volume.volume_header.write_heap(__heap)
		#
		#
		#
		# #--- make records table
		# __buffer = BytesIO()
		# for record in volume.records:
		# 	record.write_heap(__heap)
		# 	b_record = record.pack()
		# 	__buffer.write(b_record)
		#
		#
		# b_records = __buffer.getbuffer()
		# volume.volume_header.table_len = len(b_records)
		# volume.volume_header.records = len(volume.records)
		#
		#
		# b_heap = __heap.getbuffer()
		# volume.volume_header.heap_len = len(b_heap)
		#
		#
		# b_volume_header = volume.volume_header.pack()
		#
		#
		#
		#
		# #--- write
		# fd = gzip.open(volume_path, "wb")
		#
		# fd.write(b_file_header)
		# fd.write(b_volume_header)
		# fd.write(b_records)
		# fd.write(b_heap)
		#
		# # __heap.close()
		# # __buffer.close()
		#
		# fd.flush()
		# fd.close()
		pass