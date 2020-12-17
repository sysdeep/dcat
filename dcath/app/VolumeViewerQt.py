# -*- coding: utf-8 -*-
import sys
import signal
from PyQt5.QtWidgets import QApplication
from .ui_qt.VolumeViewer.MainWindow import MainWindow
from .storage.Storage import Storage
from .shared import get_storage
from .AppAbstract import AppAbstract


# TMP_STORAGE = "/home/nia/Development/_Python/_DCat/ExportB/gz"


# DB_PATH = "/home/nia/Development/_Python/_DCat/Export10/Video.bm.gz"
# DB_PATH = "/home/nia/Development/_Python/_DCat/Export10/Apps.bm.gz"
# FILE = "Video.bm.gz"




class VolumeViewerQt(AppAbstract):
	def __init__(self):
		super(VolumeViewerQt, self).__init__()

		self.app = QApplication(sys.argv)
		self.gui = MainWindow(None)




	def start(self, db_path=None):

		# if db_path:
		# 	get_storage().open_volume(db_path)
		self.gui.start(db_path)
		# self.gui.explorer.start()

		sys.exit(self.app.exec_())

	
	def stop(self):
		self.gui.act_exit()
