# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QGridLayout


from app.shared import get_storage

from .VolumeInfo import VolumeInfo
from .explorer.Explorer import Explorer

class MainFrame(QWidget):
	def __init__(self, parent=None):
		super(MainFrame, self).__init__(parent)
		layout = QVBoxLayout()
		self.setLayout(layout)


		self.__volume_info = VolumeInfo()
		self.__explorer = Explorer()



		layout.addWidget(self.__volume_info)
		layout.addWidget(self.__explorer)



	def start(self):
		storage = get_storage()


		self.__volume_info.set_info(storage.volume.volume_header)
		# self.__explorer.show_root()