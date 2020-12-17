#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import signal
from abc import ABC, abstractmethod

class AppAbstract(ABC):
	def __init__(self):

		#--- перехват системных сигналов
		signal.signal(signal.SIGINT, self.__signal_handler)			# обработка Ctrl+C

	#--- interface ------------------------------------------------------------
	@abstractmethod
	def start(self, db_path=None):
		"""
		
		:param db_path: - путь до базы(каталога или файла)
		:return:
		"""
		pass

	@abstractmethod
	def stop(self):
		pass
	#--- interface ------------------------------------------------------------





	def __signal_handler(self, signum, frame):
		"""обработчик сигнала завершения от системы"""
		print("перехвачен сигнал SIGINT(Ctrl+C)")
		print("запрос на выход из cmd")
		self.stop()
