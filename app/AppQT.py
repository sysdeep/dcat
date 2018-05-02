#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import signal
from PyQt5.QtWidgets import QApplication
from .guiqt.MainWindow import MainWindow


class AppQT(object):
	def __init__(self):



		#--- перехват системных сигналов
		signal.signal(signal.SIGINT, self.__signal_handler)			# обработка Ctrl+C



		self.app = QApplication(sys.argv)
		self.gui = MainWindow()




	def start(self):

		sys.exit(self.app.exec_())



	def __signal_handler(self, signum, frame):
		"""обработчик сигнала завершения от системы"""
		print("перехвачен сигнал SIGINT(Ctrl+C)")
		print("запрос на выход из cmd")
		self.gui.act_exit()
