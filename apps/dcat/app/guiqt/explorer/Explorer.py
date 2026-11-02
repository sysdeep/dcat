#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QFontDatabase

from app.storage import get_storage

from .VolumesList import VolumesList
from .FilesList import FilesList


class Explorer(QWidget):
	def __init__(self, parent=None):
		super(Explorer, self).__init__(parent)

		self.main_layout = QHBoxLayout(self)


		self.volumes_list = VolumesList()
		self.volumes_list.selected.connect(self.__on_volume_selected)
		self.files_list = FilesList()

		self.main_layout.addWidget(self.volumes_list)
		self.main_layout.addWidget(self.files_list)


		self.__volumes_map = {}
		self.current_volume = None



	def reload(self):
		"""сброс вида к дефолтному"""


		volumes = get_storage().fetch_volumes()

		self.volumes_list.reload(volumes)
		self.files_list.clear_list()

		self.__volumes_map = {}
		for v in volumes:
			self.__volumes_map[v.uuid] = v



	def __on_volume_selected(self, volume_uuid):
		self.current_volume = self.__volumes_map[volume_uuid]


		self.files_list.show_volume(self.current_volume)