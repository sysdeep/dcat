# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QGridLayout


from app.lib.models.Volume import Volume

from ..frames.VolumeInfo import VolumeInfo
from ..frames.explorer.Explorer import Explorer

class MainFrame(QWidget):
	def __init__(self, parent=None):
		super(MainFrame, self).__init__(parent)
		layout = QVBoxLayout()
		self.setLayout(layout)


		self.__volume_info = VolumeInfo()
		self.__explorer = Explorer()



		layout.addWidget(self.__volume_info)
		layout.addWidget(self.__explorer)



	def set_volume(self, volume: Volume):
		


		self.__volume_info.set_info(volume.volume_header)
		self.__explorer.set_volume(volume)