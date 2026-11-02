#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import namedtuple

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtGui import QFontDatabase

# from app.storage import get_storage

from .VolumesList import VolumesList
from .FilesList import FilesList
from ..NodeInfo import NodeInfo
# from .VolumeInfo import VolumeInfo
from ....shared import get_storage
from app.lib.models.Volume import Volume
from app.lib.logger import log




Vnode = namedtuple("Vnode", "name uuid")









class Explorer(QWidget):
	def __init__(self, storage=None, parent=None):
		super(Explorer, self).__init__(parent)

		
		self.main_layout = QHBoxLayout(self)

		#--- files list
		self.__files_list = FilesList()
		self.__files_list.sopen.connect(self.open_item)
		self.__files_list.sback.connect(self.__on_go_back)
		self.__files_list.selected.connect(self.__on_item_selected)

		#--- node info
		self.__node_info = NodeInfo()
		

		#--- vars
		self.__volume = None
		self.__path_stack = []

		# self.main_layout.addWidget(self.volume_info)
		# self.main_layout.addWidget(self.volumes_list)
		self.main_layout.addWidget(self.__files_list)
		self.main_layout.addWidget(self.__node_info)


		self.__volumes_map = {}
		self.current_volume = None

	


	def set_volume(self, volume: Volume):
		self.__volume = volume
		self.__path_stack = []
		self.open_item(0)




	def open_item(self, node_id: int):
		log.debug("открыть каталог: {}".format(node_id))
		records = self.__volume.get_files(node_id)
		self.__files_list.set_items(records)
		self.__path_stack.append(node_id)
		
	def __on_item_selected(self, fid: int):
		node = self.__volume.get_file(fid)
		self.__node_info.set_info(node)


	def __on_go_back(self):
		if len(self.__path_stack) < 2:
			log.warning("null history")
			return None

		self.__path_stack.pop()
		parent_id = self.__path_stack.pop()
		
		self.open_item(parent_id)
		
	