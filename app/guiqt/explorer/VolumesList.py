#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFontDatabase, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

from app.storage import get_storage

from app.guiqt.icons import get_volume_icon

class VolumesList(QWidget):
	selected = pyqtSignal(str)
	def __init__(self, parent=None):
		super(VolumesList, self).__init__(parent)

		self.setFixedWidth(200)

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.ilist = QListWidget()
		self.ilist.pressed.connect(self.__on_selected)
		self.main_layout.addWidget(self.ilist)


		self.current_vnode_uuid = None



	def reload(self, volumes):
		"""обновление списка томов"""
		self.__clear()
		self.current_vnode_uuid = None
		# self.current_volume_id = None
		# self.__volumes_map = {}
		self.__insert_volumes(volumes)
		# self.is_locked = True



	def __clear(self):
		self.ilist.clear()



	def __insert_volumes(self, volumes):
		# self.volume_icons = []
		# volumes = get_storage().fetch_volumes()


		# abdig_sort = lambda var: [int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var.name)]

		# volumes.sort(key=lambda vnode: vnode.name)
		# volumes.sort(key=abdig_sort)
		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', key.name)]
		volumes.sort(key=alphanum_key)


		#
		# names = [x.name for x in volumes]
		# print(natsorted(names))



		for vnode in volumes:

			list_item = QListWidgetItem(vnode.name)
			icon = get_volume_icon(vnode.vtype)
			list_item.setData(Qt.UserRole + 1, vnode.uuid)
			list_item.setIcon(icon)

		# ivolume = volume_icon(vnode.vtype)
		# ivolume = ticons.vicon(vnode.vtype)
		# self.volume_icons.append(ivolume)
		# self.__list.insert('', 'end', vnode.uuid, text=vnode.name, tags=("simple", ), image=ivolume)
		# self.__volumes_map[vnode.uuid] = vnode

			self.ilist.addItem(list_item)


	def __on_selected(self, list_item):
		uuid = list_item.data(Qt.UserRole + 1)
		if uuid == self.current_vnode_uuid:
			return False

		self.current_vnode_uuid = uuid

		self.selected.emit(self.current_vnode_uuid)