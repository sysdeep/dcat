#!/usr/bin/env python3
# -*- coding: utf-8 -*-



from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QListWidget
from PyQt5.QtGui import QFontDatabase


class VolumesList(QWidget):
	def __init__(self, parent=None):
		super(VolumesList, self).__init__(parent)

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.ilist = QListWidget()
		self.main_layout.addWidget(self.ilist)