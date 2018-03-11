#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QFontDatabase

from .VolumesList import VolumesList
from .FilesList import FilesList


class Explorer(QWidget):
	def __init__(self, parent=None):
		super(Explorer, self).__init__(parent)

		self.main_layout = QHBoxLayout(self)


		self.volumes_list = VolumesList()
		self.files_list = FilesList()

		self.main_layout.addWidget(self.volumes_list)
		self.main_layout.addWidget(self.files_list)



	def refresh(self):
		print("need...")
		# self.f_list.clear()
		# self.v_list.reload_volumes()
