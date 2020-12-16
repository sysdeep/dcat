
import sqlite3
from .NodeConverter import NodeConverter
from . import db_worker


class Converter:
	def __init__(self):
		self.__src_file_path = None
		self.__dest_path = None
		self.__connection = None


	def start(self, src_file_path, dest_path):
		print("start")
		self.__src_file_path = src_file_path
		self.__dest_path = dest_path


		self.__connection = sqlite3.connect(self.__src_file_path)
		self.__connection.row_factory = sqlite3.Row

		#--- get all volumes
		volumes = db_worker.get_volumes(self.__connection)
		
		for volume in volumes:
			node_converter = NodeConverter(self.__connection, volume, self.__dest_path)
			node_converter.start()
			
			# TODO
			break


		


		

		
		
		
		
		




		# TODO: close db
		self.__connection.close()



	