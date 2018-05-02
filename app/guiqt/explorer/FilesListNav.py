#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QTreeWidget
from PyQt5.QtGui import QFontDatabase


class FilesListNav(QWidget):
	def __init__(self, parent=None):
		super(FilesListNav, self).__init__(parent)

		self.main_layout = QHBoxLayout(self)

		self.btn_root = QPushButton("root")

		self.main_layout.addWidget(self.btn_root)
		self.main_layout.addStretch()




	def reinit(self):
		print("FilesLisNav - reinit!!!")