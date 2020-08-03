#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import signal
from PyQt5.QtWidgets import QApplication
from .gui.MainWindow import MainWindow
from .storage.Storage import Storage
from .shared import get_storage
TMP_STORAGE = "/home/nia/Development/_Python/_DCat/ExportB/gz"

class AppQT(object):
	def __init__(self):



		#--- перехват системных сигналов
		signal.signal(signal.SIGINT, self.__signal_handler)			# обработка Ctrl+C


		
		get_storage().read_dir(TMP_STORAGE)

		self.app = QApplication(sys.argv)
		self.gui = MainWindow(None)




	def start(self):

		sys.exit(self.app.exec_())



	def __signal_handler(self, signum, frame):
		"""обработчик сигнала завершения от системы"""
		print("перехвачен сигнал SIGINT(Ctrl+C)")
		print("запрос на выход из cmd")
		self.gui.act_exit()


if __name__ == "__main__":
	app = AppQT()
	app.start()
	
	