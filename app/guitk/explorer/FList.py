#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import tkinter
from tkinter import ttk
from tkinter import messagebox

from app.storage import get_storage
from app.lib import dbus, tools
from app.lib.fsize import naturalsize
from ..utils import conv, ticons

from .LNode import LNode
from .NavBar import NavBar




class FList(ttk.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(FList, self).__init__(parent, *args, **kwargs)


		self.nav_bar = NavBar(self)
		self.nav_bar.pack(side="top", fill="x")
		self.nav_bar.set_cb_go(self.__go_history)
		self.nav_bar.set_cb_root(self.__go_root)
		self.nav_bar.cb_show_info = self.__show_info

		self.__sort_dir = False

		columns=('size', 
			# 'rights', "owner", "group", 
			"ctime", 
			# "atime", "mtime"
			)
		self.__tree = ttk.Treeview(self, show="tree headings", selectmode='browse', columns=columns)
		# self.__tree.heading("size", text="Размер", command=lambda c="size": self.__sort(c))
		self.__tree.heading("size", text="Размер")
		# self.__tree.heading("rights", text="Права")
		# self.__tree.heading("owner", text="Владелец")
		# self.__tree.heading("group", text="Группа")
		self.__tree.heading("ctime", text="Создание")
		# self.__tree.heading("atime", text="Доступ")
		# self.__tree.heading("mtime", text="Модификация")
		self.__tree.heading('#0', text='Название')

		self.__tree.column("#0", minwidth=200, width=200)
		self.__tree.column("size", minwidth=90, width=90)
		# self.__tree.column("rights", minwidth=40, width=50)
		# self.__tree.column("owner", minwidth=80, width=80)
		# self.__tree.column("group", minwidth=80, width=80)
		self.__tree.column("ctime", minwidth=200, width=200)
		# self.__tree.column("atime", minwidth=90, width=90)
		# self.__tree.column("mtime", minwidth=100, width=100)


		# for c in columns:
		# 	self.__tree.heading(c, text=c, command=lambda c=c: self.__sort(c))

		self.__tree.pack(side="left", expand=True, fill="both")


		#--- vertical scroll
		ysb = ttk.Scrollbar(self, orient="vertical", command= self.__tree.yview)
		self.__tree['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")

		self.__tree.column("#0", width=300)
		self.__tree.tag_bind("simple", "<<TreeviewSelect>>", self.__select_row)
		self.__tree.bind("<Double-1>", self.__open_row)
		# self.__tree.tag_bind("simple", "<<TreeviewOpen>>", self.__open_row)
		self.__tree.bind("<Button-3>", self.__make_cmenu)



		self.cmenu = tkinter.Menu(self, tearoff=0)
		self.cmenu.add_command(label="Свойства", command=self.__show_info, image=ticons.ticon(ticons.INFO), compound="left")
		# self.cmenu.add_command(label="Экспорт", command=self.__show_export, image=ticons.ticon(ticons.I_EXPORT), compound="left")
		self.cmenu.add_command(label="Удалить", command=self.__show_remove, image=ticons.ticon(ticons.TRASH), compound="left")
		# self.cmenu.add_command(label="Изменить", command=self.__show_edit, image=self.__icon_menu_edit, compound="left")


		#--- хранилище
		self.storage = get_storage()



		#--- тек. объекты тома и папки
		self.current_vnode = None
		self.current_fnode = None


		#--- карта загруженных нод для поиска при событиях от дерева
		self.litems = {}


		# dbus.eon(dbus.SHOW_REMOVE_FTREE_OK, self.__on_ftree_removed)








	#--- public ---------------------------------------------------------------
	def show_volume(self, vnode):
		"""отобразить содержимое тома"""

		self.current_vnode = vnode
		self.current_fnode = None

		self.nav_bar.reinit()					# обновление панели навигации

		self.update_view()						# перестройка вида


	def show_folder(self, fnode):
		"""отобразить содержимое папки"""

		self.current_fnode = fnode

		self.update_view()						# перестройка вида


	def clear(self):
		"""запрос очистки содержимого"""
		self.__clear()

	#--- public ---------------------------------------------------------------





	#--- view controls --------------------------------------------------------
	def update_view(self):
		"""обновление списка отображаемых элементов"""

		#--- очистка
		self.__clear()


		if self.current_fnode:			# если отображался каталог
			self.__show_folder_items()
		else:							# иначе том
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




	def __clear(self):
		"""очистка содержимого таблицы"""
		for row in self.__tree.get_children():
			self.__tree.delete(row)

		self.litems = {}



	def __insert_file(self, fnode):
		"""добавление строки в дерево"""

		if fnode.is_dir():								# папка
			icon = ticons.ficon(ticons.F_FOLDER)
			size = ""
		else:											# файл
			icon = ticons.ficon(ticons.F_EMPTY)
			size = naturalsize(fnode.size)

		ivalues = (
				size,
				# file_row[FRow.RIGHTS],
				# file_row[FRow.OWNER],
				# file_row[FRow.GROUP],
				conv.convert_ctime(fnode.ctime),
				# conv.convert_ctime(file_row[FRow.ATIME]),
				# conv.convert_ctime(file_row[FRow.MTIME]),
			)


		self.__tree.insert("", 'end', fnode.uuid, text=fnode.name, tags=("simple", ), image=icon, values=ivalues)

		#--- создаём карту нод
		self.litems[fnode.uuid] = fnode



	def __make_cmenu(self, e):
		"""отображение контекстного меню"""
		cmenu_selection = self.__tree.identify_row(e.y)		# тек. елемент под курсором

		if cmenu_selection:
			self.__tree.selection_set(cmenu_selection)				# выделяем его
			# self.__select_row(None)									# выполняем действия по отображению выбора

			#--- отображение меню
			# self.cmenu.post(e.x_root, e.y_root)
			self.cmenu.tk_popup(e.x_root, e.y_root)					# автозакрытие при потере фокуса(https://stackoverflow.com/questions/21200516/python3-tkinter-popup-menu-not-closing-automatically-when-clicking-elsewhere)

	#--- view controls --------------------------------------------------------























	#--- navbar events --------------------------------------------------------
	def __go_root(self):
		"""перейти в корень тома"""
		self.show_volume(self.current_vnode)

	def __go_history(self, fnode):
		"""перейти в корень заданного каталога"""
		self.show_folder(fnode)
	#--- navbar events --------------------------------------------------------



	



	












	#--- tree events ----------------------------------------------------------

	def __get_selected_fnode(self):
		"""получить объект fnode из выбора виджета дерева"""
		selection = self.__tree.selection()
		if len(selection) == 0:
			return None

		selected_item = self.__tree.selection()[0]
		fnode = self.litems[selected_item]

		return fnode





	def __select_row(self, e):
		"""выбор файла - пока пусто(использовался для оперативного отображения информации о ноде)"""
		# fnode = self.__get_selected_fnode()
		pass


	def __open_row(self, e):
		"""открытие папки"""

		fnode = self.__get_selected_fnode()

		if fnode is None:
			return False

		if fnode.is_file():
			return False

		self.show_folder(fnode)								# отображаем папку
		self.nav_bar.history_push(fnode)					# обновляем панель навигации

	#--- tree events ----------------------------------------------------------
	















	#--- cmenu actions --------------------------------------------------------
	def __show_info(self):
		"""отобразить информацию о ноде"""
		fnode = self.__get_selected_fnode()

		if fnode is None:
			return False

		dbus.emit(dbus.SHOW_ABOUT_FILE, fnode)



	def __show_export(self):
		"""
			экспорт заданного поддерева
			TODO: не завершено...
		"""

		fnode = self.__get_selected_fnode()

		if fnode is None:
			return False

		dbus.emit(dbus.SHOW_EXPORT_FTREE, fnode)



	def __show_remove(self):
		"""удаление элемента или ветви"""
		fnode = self.__get_selected_fnode()

		if fnode is None:
			return False




		result = messagebox.askyesno("Подтверждение удаления", "Удалить выбранный элемент?")
		if result is False:
			return False

		# @tools.dtimeit
		# def get_all_branch_gen(fnode):
		# 	"""
		# 		2.68
		# 		index - 0.10822153091430664
		# 	"""
		# 	print("get branch gen")
		# 	for item in self.storage.fetch_parent_files_all(fnode.uuid):
		# 		self.storage.remove_file(item.uuid)
		# 		# print("removed: ", item.name)
		#
		#
		#
		#
		# @tools.dtimeit
		# def get_all_branch_rec(fnode):
		# 	"""
		# 		2.27
		# 		index - 0.06787323951721191
		# 	"""
		# 	print("get branch rec")
		# 	def qqq(fnode):
		#
		# 		self.storage.remove_file(fnode.uuid)
		# 		files = self.storage.fetch_parent_files(fnode.uuid)
		#
		# 		for f in files:
		# 			qqq(f)
		#
		# 	qqq(fnode)
		#
		# get_all_branch_gen(fnode)
		# # get_all_branch_rec(fnode)



		#--- удаляем заданный
		self.storage.remove_file(fnode.uuid)
		# print("removed: ", fnode.name)

		#--- удаляем все вложенные элементы
		for item in self.storage.fetch_parent_files_all(fnode.uuid):
			self.storage.remove_file(item.uuid)
			# print("removed: ", item.name)





		#--- тестирование удаления одним махом списка удаляемых(время примерно такоеже...)
		# ritems = [(fnode.uuid,)]
		# # self.storage.remove_file(fnode.uuid)
		# # print("removed: ", fnode.name)
		#
		# #--- удаляем все вложенные элементы
		# for item in self.storage.fetch_parent_files_all(fnode.uuid):
		# 	# self.storage.remove_file(item.uuid)
		# 	# print("removed: ", item.name)
		# 	ritems.append( (item.uuid,) )
		#
		# self.storage.remove_files(ritems)

		#--- сохраняем изменения
		self.storage.commit()

		self.update_view()



		# dbus.emit(dbus.SHOW_REMOVE_FTREE, fnode)
	#--- cmenu actions --------------------------------------------------------






	#--- bus events -----------------------------------------------------------
	# def __on_ftree_removed(self):
	# 	"""событие об удалении ветви"""
	#
	# 	self.update_view()
	#--- bus events -----------------------------------------------------------









	def __sort_nodes(self, nodes):
		"""сортировка"""

		dir_nodes = [fnode for fnode in nodes if fnode.is_dir()]			# каталоги
		file_nodes = [fnode for fnode in nodes if fnode.is_file()]			# файлы


		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', key.name)]
		# nodes.sort(key=alphanum_key)

		dir_nodes.sort(key=alphanum_key)
		file_nodes.sort(key=alphanum_key)

		return dir_nodes + file_nodes

