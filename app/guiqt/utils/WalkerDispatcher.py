#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	http://code.activestate.com/recipes/578299-pyqt-pyside-thread-safe-global-queue-main-loop-int/
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QEvent, pyqtSignal
from app.rc import QUE_WALKER
from app import log
# from .Event import Event

class WalkerDispatcher(QThread):

	msg = pyqtSignal(dict)

	def __init__(self, parent=None):
		super(WalkerDispatcher, self).__init__()
		self.parent = parent



	def run(self):
		log.debug("starting WalkerDispatcher")

		while True:

			data = QUE_WALKER.get()
			if data is None:
				break


			# print(data)
			# QApplication.postEvent(self.parent, Event(data))
			self.msg.emit(data)


	def stop(self):
		QUE_WALKER.put(None)
		self.wait()




#
#
#
#
# class QReader(QThread):
#
# 	msg = pyqtSignal(dict)
#
# 	def __init__(self, que):
# 		super(QReader, self).__init__()
# 		self.que = que
#
#
# 	def run(self):
#
# 		while True:
# 			data = self.que.get()
# 			self.msg.emit(data)
#
#
#





#
#
#
# class Event(QEvent):
# 	EVENT_TYPE = QEvent.Type(QEvent.registerEventType())
#
# 	def __init__(self, data):
# 		#thread-safe
# 		QEvent.__init__(self, Event.EVENT_TYPE)
# 		self.data = data