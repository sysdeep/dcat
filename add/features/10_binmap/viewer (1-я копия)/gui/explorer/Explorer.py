#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QFontDatabase

# from app.storage import get_storage

from .VolumesList import VolumesList
from .FilesList import FilesList
from .VolumeInfo import VolumeInfo
from ...shared import get_storage

Vnode = namedtuple("Vnode", "name uuid")


class Explorer(QWidget):
	def __init__(self, storage=None, parent=None):
		super(Explorer, self).__init__(parent)

		storage = get_storage()
		
		
		volumes = []
		for vol in storage.volumes:
			# print(vol.name)
			v = Vnode(vol.name, vol.name)
			volumes.append(v)
		
		

		self.main_layout = QHBoxLayout(self)

		self.volume_info = VolumeInfo()

		# self.volumes_list = VolumesList()
		# self.volumes_list.selected.connect(self.__on_volume_selected)
		self.files_list = FilesList()

		self.main_layout.addWidget(self.volume_info)
		# self.main_layout.addWidget(self.volumes_list)
		self.main_layout.addWidget(self.files_list)


		self.__volumes_map = {}
		self.current_volume = None

		
		# self.volumes_list.reload(volumes)

		#--- load data
		self.volume_info.set_info(storage.volume.header)
		self.files_list.set_items(storage.volume.get_vrecords(0))




	def reload(self):
		"""сброс вида к дефолтному"""


		# volumes = get_storage().fetch_volumes()
		#
		# self.volumes_list.reload(volumes)
		# self.files_list.clear_list()
		#
		# self.__volumes_map = {}
		# for v in volumes:
		# 	self.__volumes_map[v.uuid] = v

		pass


	def __on_volume_selected(self, volume_uuid):
		pass
		#
		# # print(volume_uuid)
		#
		# storage = get_storage()
		# fvol = None
		# for vol in storage.volumes:
		# 	if vol.name == volume_uuid:
		# 		fvol = vol
		# 		break
		#
		# if fvol:
		# 	self.files_list.clear_list()
		# 	fvol.read_body()
		# 	records = fvol.get_root()
		#
		# 	# print("-"*20)
		# 	for r in records:
		# 		# print(r.name)
		# 		# self.files_list.insert_file(r.name)
		# 		self.files_list.insert_record(r)
		# 	# print("-"*20)
		#
		#
		#
		# # self.current_volume = self.__volumes_map[volume_uuid]
		# #
		# #
		# # self.files_list.show_volume(self.current_volume)