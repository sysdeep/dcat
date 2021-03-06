# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QGridLayout


from app.lib.models.Volume import Volume
from app.lib.logger import log

from ..frames.VolumeInfo import VolumeInfo
from ..frames.explorer.Explorer import Explorer

class MainFrame(QWidget):
	def __init__(self, parent=None):
		super(MainFrame, self).__init__(parent)
		layout = QVBoxLayout()
		self.setLayout(layout)


		self.__volume_info = VolumeInfo()
		self.__explorer = Explorer()


		#--- controls
		controls = QHBoxLayout()
		
		btn_save = QPushButton("Save")
		btn_save.clicked.connect(self.__on_volume_save)
		
		controls.addWidget(btn_save)

		layout.addWidget(self.__volume_info)
		layout.addWidget(self.__explorer)
		layout.addLayout(controls)
		
		#--- vars
		self.__volume = None



	def set_volume(self, volume: Volume):
		
		self.__volume = volume

		self.__volume_info.set_info(volume.volume_header, volume.current_path)
		self.__explorer.set_volume(volume)
		
		
	def __on_volume_save(self):
		log.info("save volume action - start")
		
		volume_path = self.__volume.current_path
		self.__volume.save(volume_path)
		
		log.info("save volume action - end")