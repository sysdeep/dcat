#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, \
	QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QHeaderView

from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import Qt

from app.storage import get_storage
from app.lib.fsize import naturalsize
from app.utils import conv

from ..icons import get_ftype_icon

from .FilesListNav import FilesListNav


class FilesList(QWidget):
	def __init__(self, parent=None):
		super(FilesList, self).__init__(parent)

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		self.nav_bar = FilesListNav()
		self.main_layout.addWidget(self.nav_bar)


		self.ilist = QTreeWidget()
		self.ilist.setColumnCount(3)
		self.ilist.setHeaderLabels(("Название", "Размер", "Создание"))
		self.ilist.setRootIsDecorated(False)									# hide first margin
		self.ilist.header().setStretchLastSection(False)
		self.ilist.header().setSectionResizeMode(0, QHeaderView.Stretch)
		self.ilist.setColumnWidth(1, 100)
		self.ilist.setColumnWidth(2, 150)
		self.ilist.pressed.connect(self.__on_selected)
		self.main_layout.addWidget(self.ilist)


		#--- хранилище
		self.storage = get_storage()


		#--- тек. объекты тома и папки
		self.current_fnode = None
		self.current_vnode = None

		self.current_fnode_uuid = None


		#--- карта загруженных нод для поиска при событиях от дерева
		self.litems = {}














	def clear_list(self):
		"""очистка содержимого таблицы"""
		self.ilist.clear()





	# --- public ---------------------------------------------------------------
	def show_volume(self, vnode):
		"""отобразить содержимое тома"""

		self.current_vnode = vnode
		self.current_fnode = None

		self.nav_bar.reinit()  # обновление панели навигации

		self.update_view()  # перестройка вида




	# --- view controls --------------------------------------------------------
	def update_view(self):
		"""обновление списка отображаемых элементов"""

		# --- очистка
		self.clear_list()

		if self.current_fnode:  # если отображался каталог
			self.__show_folder_items()
		else:  # иначе том
			self.__show_volume_items()



	def __show_volume_items(self):
		"""отобразить строки тома"""

		items = self.storage.fetch_volume_files(self.current_vnode.uuid)
		self.__sort_nodes(items)
		for item in items:
			self.__insert_file(item)

	def __show_folder_items(self):
		"""отобразить строки папки"""

		items = self.storage.fetch_parent_files(self.current_fnode.uuid)

		# fnodes = self.__sort_nodes(fnodes)
		self.__sort_nodes(items)

		for item in items:
			self.__insert_file(item)

	def __insert_file(self, fnode):
		"""добавление строки в дерево"""

		if fnode.is_dir():  # папка
			# icon = ticons.ficon(ticons.F_FOLDER)
			icon = get_ftype_icon("folder")
			size = ""
		else:  # файл
			# icon = ticons.ficon(ticons.F_EMPTY)
			icon = get_ftype_icon("empty")
			size = naturalsize(fnode.size)

		ctime = conv.convert_ctime(fnode.ctime)

		# ivalues = (
		# 	size,
		# 	# file_row[FRow.RIGHTS],
		# 	# file_row[FRow.OWNER],
		# 	# file_row[FRow.GROUP],
		# 	conv.convert_ctime(fnode.ctime),
		# 	# strings.cut_text(fnode.description, 15)
		# 	# conv.convert_ctime(file_row[FRow.ATIME]),
		# 	# conv.convert_ctime(file_row[FRow.MTIME]),
		# )
		#
		# self.__tree.insert("", 'end', fnode.uuid, text=fnode.name, tags=("simple",), image=icon, values=ivalues)

		tree_item = QTreeWidgetItem([fnode.name, size, ctime])
		tree_item.setIcon(0, icon)
		tree_item.setData(0, Qt.UserRole + 1, fnode.uuid)
		self.ilist.addTopLevelItem(tree_item)


		# --- создаём карту нод
		self.litems[fnode.uuid] = fnode




	def __on_selected(self, tree_item):
		uuid = tree_item.data(Qt.UserRole + 1)
		print(uuid)







	def __sort_nodes(self, nodes):
		"""сортировка"""

		dir_nodes = [fnode for fnode in nodes if fnode.is_dir()]  # каталоги
		file_nodes = [fnode for fnode in nodes if fnode.is_file()]  # файлы

		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', key.name)]
		# nodes.sort(key=alphanum_key)

		dir_nodes.sort(key=alphanum_key)
		file_nodes.sort(key=alphanum_key)

		return dir_nodes + file_nodes
