# -*- coding: utf-8 -*-



import sys
import signal
from PyQt5.QtWidgets import QApplication
from .gui.MainWindow import MainWindow
from .storage.Storage import Storage
from .shared import get_storage


# TMP_STORAGE = "/home/nia/Development/_Python/_DCat/ExportB/gz"


# DB_PATH = "/home/nia/Development/_Python/_DCat/Export10/Video.bm.gz"
# DB_PATH = "/home/nia/Development/_Python/_DCat/Export10/Apps.bm.gz"
# FILE = "Video.bm.gz"




class App(object):
	def __init__(self, db_path):


		self.db_path = db_path
		#--- перехват системных сигналов
		signal.signal(signal.SIGINT, self.__signal_handler)			# обработка Ctrl+C



		# read_dir = store_path if store_path else TMP_STORAGE

		
		

		self.app = QApplication(sys.argv)
		self.gui = MainWindow(None)




	def start(self):


		get_storage().open_volume(self.db_path)
		# self.gui.explorer.start()

		sys.exit(self.app.exec_())



	def __signal_handler(self, signum, frame):
		"""обработчик сигнала завершения от системы"""
		print("перехвачен сигнал SIGINT(Ctrl+C)")
		print("запрос на выход из cmd")
		self.gui.act_exit()


	