#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from typing import List

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QGridLayout, \
	QVBoxLayout, QWidget, QTreeWidget, QTreeWidgetItem, QHeaderView, QListWidget, QListWidgetItem, QPushButton

from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

from app.lib.models.FileRecord import FileRecord
# from app.storage import get_storage
# from app.lib.fsize import naturalsize
# from app.utils import conv

# from ..icons import get_ftype_icon

# from .FilesListNav import FilesListNav


from ....shared import get_storage
from ....rc import get_icon_path
from ....ui_common.utils import convert_ctime

class NodeInfo(QWidget):
	def __init__(self, parent=None):
		super(NodeInfo, self).__init__(parent)

		self.__node = None

		layout = QGridLayout()
		self.setLayout(layout)


		self.__name = QLabel()

		btn_rm = QPushButton("rm")
		btn_rm.clicked.connect(self.__rm_node)

		row = 0
		layout.addWidget(QLabel("Name"), row, 0)
		layout.addWidget(self.__name, row, 1)

		row += 1
		layout.addWidget(btn_rm, row, 0)


	def set_node(self, node):
		self.__node = node
		self.__name.setText(node.name)


	def __rm_node(self):
		storage = get_storage()
		storage.volume.rm_node(self.__node)



class FilesList(QWidget):
	sopen = pyqtSignal(int)					# node id
	sback = pyqtSignal()
	selected = pyqtSignal(int)				# node id
	
	def __init__(self, parent=None):
		super(FilesList, self).__init__(parent)

		self.main_layout = QVBoxLayout(self)
		self.main_layout.setContentsMargins(0, 0, 0, 0)

		# self.nav_bar = FilesListNav()
		# self.nav_bar.go_root_signal.connect(self.__go_root)
		# self.nav_bar.go_node_signal.connect(self.show_folder)

		# self.main_layout.addWidget(self.nav_bar)

		self.btn_back = QPushButton("Back")
		self.btn_back.clicked.connect(self.__on_back)


		self.ilist = QTreeWidget()
		self.ilist.setColumnCount(3)
		self.ilist.setHeaderLabels(("Название", "Размер", "Создание"))
		self.ilist.setRootIsDecorated(False)									# hide first margin
		self.ilist.header().setStretchLastSection(False)
		self.ilist.header().setSectionResizeMode(0, QHeaderView.Stretch)
		self.ilist.setColumnWidth(1, 100)
		self.ilist.setColumnWidth(2, 150)
		self.ilist.pressed.connect(self.__on_selected)
		self.ilist.doubleClicked.connect(self.__on_open)
		
		
		self.main_layout.addWidget(self.ilist)
		
		self.main_layout.addWidget(self.btn_back)


		self.node_info = NodeInfo()
		self.main_layout.addWidget(self.node_info)
		#--- хранилище
		# self.storage = get_storage()


		#--- тек. объекты тома и папки
		# self.current_fnode = None
		# self.current_vnode = None
		#
		self.current_fnode_uuid = None
		#
		#
		#--- карта загруженных нод для поиска при событиях от дерева
		self.litems = {}		# uuid: vnode


		self.__history = [0]










	def __on_back(self):
		self.sback.emit()
		# if len(self.__history) < 2:
		# 	print("null history")
		# 	return None
		#
		# self.__history.pop()
		#
		# parent_id = self.__history[-1]
		#
		# storage = get_storage()
		# records = storage.volume.get_files(parent_id)
		# self.set_items(records)
		






	#--- public ---------------------------------------------------------------
	def clear_list(self):
		"""очистка содержимого таблицы"""
		self.ilist.clear()



	def set_items(self, items_list: List[FileRecord]):
		self.clear_list()
		
		for row in items_list:
			
			
			if row.ftype == 0:					# dir
				
				icon_file = get_icon_path("ftypes", "folder.png")
			else:
				
				icon_file = get_icon_path("ftypes", "empty.png")
			
			# # QListWidgetItem(str(row.ftype), self.ilist)
			# wi = QTreeWidgetItem(name, self.ilist)
			# wi.setData(Qt.UserRole + 1, row.uid)
			
			time_text = convert_ctime(row.ctime)
			
			# TODO: назначить атрибуты другим колонкам
			tree_item = QTreeWidgetItem([row.name, str(row.size), time_text])
			tree_item.setIcon(0, QIcon(icon_file))
			tree_item.setData(0, Qt.UserRole + 1, row.fid)
			tree_item.setData(0, Qt.UserRole + 2, row.ftype)
			self.ilist.addTopLevelItem(tree_item)




			
			self.litems[row.fid] = row
			
			# self.ilist.
			
			



	# def show_volume(self, vnode):
	# 	"""отобразить содержимое тома"""
	#
	# 	self.current_vnode = vnode
	# 	self.current_fnode = None
	#
	# 	self.nav_bar.reinit()  # обновление панели навигации
	#
	# 	self.update_view()  # перестройка вида
	#
	#
	# def show_folder(self, fnode):
	# 	"""отобразить содержимое папки"""
	#
	#
	# 	self.current_fnode = fnode
	#
	# 	self.update_view()						# перестройка вида
	#
	# #--- public ---------------------------------------------------------------
	#
	#
	# # --- view controls --------------------------------------------------------
	# def update_view(self):
	# 	"""обновление списка отображаемых элементов"""
	#
	# 	# --- очистка
	# 	self.clear_list()
	#
	# 	if self.current_fnode:  # если отображался каталог
	# 		self.__show_folder_items()
	# 	else:  # иначе том
	# 		self.__show_volume_items()
	#
	#
	#
	# def __show_volume_items(self):
	# 	"""отобразить строки тома"""
	#
	# 	items = self.storage.fetch_volume_files(self.current_vnode.uuid)
	# 	self.__sort_nodes(items)
	# 	for item in items:
	# 		self.__insert_file(item)
	#
	#
	#
	# def __show_folder_items(self):
	# 	"""отобразить строки папки"""
	#
	# 	items = self.storage.fetch_parent_files(self.current_fnode.uuid)
	#
	# 	# fnodes = self.__sort_nodes(fnodes)
	# 	self.__sort_nodes(items)
	#
	# 	# if self.current_fnode_uuid:
	# 	# 	self.__insert_go_parent()
	#
	# 	for item in items:
	# 		self.__insert_file(item)
	#
	#
	# # def __insert_go_parent(self):
	# # 	tree_item = QTreeWidgetItem(["..", "", ""])
	# # 	# tree_item.setIcon(0, icon)
	# # 	# tree_item.setData(0, Qt.UserRole + 1, fnode.uuid)
	# # 	self.ilist.addTopLevelItem(tree_item)
	#
	# def insert_file(self, name):
	# 	"""TMP public добавление строки в дерево"""
	#
	# 	size = "0"
	# 	ctime = "0"
	#
	# 	# if fnode.is_dir():  # папка
	# 	# 	# icon = ticons.ficon(ticons.F_FOLDER)
	# 	# 	# icon = get_ftype_icon("folder")
	# 	# 	# size = ""
	# 	# else:  # файл
	# 	# 	# icon = ticons.ficon(ticons.F_EMPTY)
	# 	# 	# icon = get_ftype_icon("empty")
	# 	# 	# size = naturalsize(fnode.size)
	#
	# 	# ctime = conv.convert_ctime(fnode.ctime)
	#
	# 	# ivalues = (
	# 	# 	size,
	# 	# 	# file_row[FRow.RIGHTS],
	# 	# 	# file_row[FRow.OWNER],
	# 	# 	# file_row[FRow.GROUP],
	# 	# 	conv.convert_ctime(fnode.ctime),
	# 	# 	# strings.cut_text(fnode.description, 15)
	# 	# 	# conv.convert_ctime(file_row[FRow.ATIME]),
	# 	# 	# conv.convert_ctime(file_row[FRow.MTIME]),
	# 	# )
	# 	#
	# 	# self.__tree.insert("", 'end', fnode.uuid, text=fnode.name, tags=("simple",), image=icon, values=ivalues)
	#
	# 	tree_item = QTreeWidgetItem([name, size, ctime])
	# 	# tree_item.setIcon(0, icon)
	# 	tree_item.setData(0, Qt.UserRole + 1, name)
	# 	self.ilist.addTopLevelItem(tree_item)
	#
	#
	# 	# --- создаём карту нод
	# 	# self.litems[fnode.uuid] = fnode
	#
	#
	# def insert_record(self, r):
	# 	"""TMP public добавление строки в дерево"""
	#
	# 	size = "0"
	# 	ctime = "0"
	#
	# 	# if fnode.is_dir():  # папка
	# 	# 	# icon = ticons.ficon(ticons.F_FOLDER)
	# 	# 	# icon = get_ftype_icon("folder")
	# 	# 	# size = ""
	# 	# else:  # файл
	# 	# 	# icon = ticons.ficon(ticons.F_EMPTY)
	# 	# 	# icon = get_ftype_icon("empty")
	# 	# 	# size = naturalsize(fnode.size)
	#
	# 	# ctime = conv.convert_ctime(fnode.ctime)
	#
	# 	# ivalues = (
	# 	# 	size,
	# 	# 	# file_row[FRow.RIGHTS],
	# 	# 	# file_row[FRow.OWNER],
	# 	# 	# file_row[FRow.GROUP],
	# 	# 	conv.convert_ctime(fnode.ctime),
	# 	# 	# strings.cut_text(fnode.description, 15)
	# 	# 	# conv.convert_ctime(file_row[FRow.ATIME]),
	# 	# 	# conv.convert_ctime(file_row[FRow.MTIME]),
	# 	# )
	# 	#
	# 	# self.__tree.insert("", 'end', fnode.uuid, text=fnode.name, tags=("simple",), image=icon, values=ivalues)
	#
	# 	tree_item = QTreeWidgetItem([r.name, size, ctime])
	# 	# tree_item.setIcon(0, icon)
	# 	tree_item.setData(0, Qt.UserRole + 1, r.uuid)
	# 	self.ilist.addTopLevelItem(tree_item)
	#
	#
	# 	# print(r.childrens)
	# 	for node in r.childrens:
	# 		self.__re_insert(node, tree_item)
	# 		# ti = QTreeWidgetItem([node.name, size, ctime])
	# 		# tree_item.addChild(ti)
	#
	# 	# --- создаём карту нод
	# 	# self.litems[fnode.uuid] = fnode
	#
	#
	# def __re_insert(self, node, parentw):
	#
	# 	for cnode in node.childrens:
	# 		ti = QTreeWidgetItem([cnode.name, "0", "0"])
	# 		parentw.addChild(ti)
	#
	#
	# 		self.__re_insert(cnode, ti)
	#
	#
	# def __insert_file(self, fnode):
	# 	"""добавление строки в дерево"""
	# 	pass
	# 	# if fnode.is_dir():  # папка
	# 	# 	# icon = ticons.ficon(ticons.F_FOLDER)
	# 	# 	icon = get_ftype_icon("folder")
	# 	# 	size = ""
	# 	# else:  # файл
	# 	# 	# icon = ticons.ficon(ticons.F_EMPTY)
	# 	# 	icon = get_ftype_icon("empty")
	# 	# 	size = naturalsize(fnode.size)
	# 	#
	# 	# ctime = conv.convert_ctime(fnode.ctime)
	# 	#
	# 	# # ivalues = (
	# 	# # 	size,
	# 	# # 	# file_row[FRow.RIGHTS],
	# 	# # 	# file_row[FRow.OWNER],
	# 	# # 	# file_row[FRow.GROUP],
	# 	# # 	conv.convert_ctime(fnode.ctime),
	# 	# # 	# strings.cut_text(fnode.description, 15)
	# 	# # 	# conv.convert_ctime(file_row[FRow.ATIME]),
	# 	# # 	# conv.convert_ctime(file_row[FRow.MTIME]),
	# 	# # )
	# 	# #
	# 	# # self.__tree.insert("", 'end', fnode.uuid, text=fnode.name, tags=("simple",), image=icon, values=ivalues)
	# 	#
	# 	# tree_item = QTreeWidgetItem([fnode.name, size, ctime])
	# 	# tree_item.setIcon(0, icon)
	# 	# tree_item.setData(0, Qt.UserRole + 1, fnode.uuid)
	# 	# self.ilist.addTopLevelItem(tree_item)
	# 	#
	# 	#
	# 	# # --- создаём карту нод
	# 	# self.litems[fnode.uuid] = fnode
	#
	# # def __make_cmenu(self, e):
	# # 	"""отображение контекстного меню"""
	# # 	cmenu_selection = self.__tree.identify_row(e.y)  # тек. елемент под курсором
	# #
	# # 	if cmenu_selection:
	# # 		self.__tree.selection_set(cmenu_selection)  # выделяем его
	# # 		# self.__select_row(None)									# выполняем действия по отображению выбора
	# #
	# # 		# --- отображение меню
	# # 		# self.cmenu.post(e.x_root, e.y_root)
	# # 		self.cmenu.tk_popup(e.x_root,
	# # 							e.y_root)  # автозакрытие при потере фокуса(https://stackoverflow.com/questions/21200516/python3-tkinter-popup-menu-not-closing-automatically-when-clicking-elsewhere)
	#
	# # --- view controls --------------------------------------------------------
	#
	#
	#
	#
	#
	# # --- navbar events --------------------------------------------------------
	# def __go_root(self):
	# 	"""перейти в корень тома"""
	# 	self.show_volume(self.current_vnode)
	#
	# def __go_history(self, fnode):
	# 	"""перейти в корень заданного каталога"""
	# 	self.show_folder(fnode)
	#
	# # --- navbar events --------------------------------------------------------
	#
	#
	#
	#
	#
	#
	#
	# #--- tree events ----------------------------------------------------------
	def __on_selected(self, tree_item):
		uuid = tree_item.data(Qt.UserRole + 1)
		self.selected.emit(uuid)
		# if self.current_fnode_uuid == uuid:
		# 	return False
		# self.current_fnode_uuid = uuid
		# print("select node: ", self.current_fnode_uuid)
		#
		# node = self.litems[uuid]
		#
		# self.node_info.set_node(node)
	
	
	def __on_open(self, tree_item):
		fid = tree_item.data(Qt.UserRole + 1)
		ftype = tree_item.data(Qt.UserRole + 2)
		
		#--- if catalog
		if ftype == FileRecord.FTYPE_CATALOG:
			self.sopen.emit(fid)




		
		
		
		
		
		
		
		
		# self.show_folder(fnode)  # отображаем папку
		# self.nav_bar.history_push(fnode)  # обновляем панель навигации
	# #--- tree events ----------------------------------------------------------
	#
	#
	#
	# #--- cmenu actions --------------------------------------------------------
	# # def __show_info(self):
	# # 	"""отобразить информацию о ноде"""
	# # 	fnode = self.__get_selected_fnode()
	# #
	# # 	if fnode is None:
	# # 		return False
	# #
	# # 	self.modal_about = AboutFile(fnode, master=self)
	# # 	self.modal_about.cb_updated = self.__on_file_updated
	# #
	# #
	# #
	# #
	# #
	# #
	# #
	# # def __show_export(self):
	# # 	"""
	# # 		экспорт заданного поддерева
	# # 		TODO: не завершено...
	# # 	"""
	# #
	# # 	fnode = self.__get_selected_fnode()
	# #
	# # 	if fnode is None:
	# # 		return False
	# #
	# # 	dbus.emit(dbus.SHOW_EXPORT_FTREE, fnode)
	# #
	# #
	# #
	# # def __show_remove(self):
	# # 	"""удаление элемента или ветви"""
	# # 	fnode = self.__get_selected_fnode()
	# #
	# # 	if fnode is None:
	# # 		return False
	# #
	# #
	# #
	# #
	# # 	result = messagebox.askyesno("Подтверждение удаления", "Удалить выбранный элемент?")
	# # 	if result is False:
	# # 		return False
	# #
	# #
	# # 	#--- удаляем заданный
	# # 	self.storage.remove_file(fnode.uuid)
	# # 	# print("removed: ", fnode.name)
	# #
	# # 	#--- удаляем все вложенные элементы
	# # 	for item in self.storage.fetch_parent_files_all(fnode.uuid):
	# # 		self.storage.remove_file(item.uuid)
	# # 		# print("removed: ", item.name)
	# #
	# #
	# #
	# # 	#--- сохраняем изменения
	# # 	self.storage.commit()
	# #
	# # 	self.update_view()
	# #
	# #
	# #
	# # 	# dbus.emit(dbus.SHOW_REMOVE_FTREE, fnode)
	# #
	# #
	#
	#
	#
	# #--- cmenu actions --------------------------------------------------------
	#
	#
	#
	#
	# #--- events ---------------------------------------------------------------
	# def __on_file_updated(self):
	# 	"""событие от модального окна файла об обновлении"""
	# 	self.update_view()
	# 	self.modal_about.destroy()
	# 	self.modal_about = None
	# #--- events ---------------------------------------------------------------
	#
	#
	#
	# def __sort_nodes(self, nodes):
	# 	"""сортировка"""
	#
	# 	dir_nodes = [fnode for fnode in nodes if fnode.is_dir()]  # каталоги
	# 	file_nodes = [fnode for fnode in nodes if fnode.is_file()]  # файлы
	#
	# 	convert = lambda text: int(text) if text.isdigit() else text
	# 	alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', key.name)]
	# 	# nodes.sort(key=alphanum_key)
	#
	# 	dir_nodes.sort(key=alphanum_key)
	# 	file_nodes.sort(key=alphanum_key)
	#
	# 	return dir_nodes + file_nodes
