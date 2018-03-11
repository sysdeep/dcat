#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QTreeWidget
from PyQt5.QtGui import QFontDatabase


from .FilesListNav import FilesListNav


class FilesList(QWidget):
	def __init__(self, parent=None):
		super(FilesList, self).__init__(parent)

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.nav_bar = FilesListNav()
		self.main_layout.addWidget(self.nav_bar)


		self.ilist = QTreeWidget()
		self.main_layout.addWidget(self.ilist)