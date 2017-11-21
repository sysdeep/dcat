#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import tkinter
from tkinter import ttk, PhotoImage

from app.storage import get_storage, VRow, FRow, FType
from app.lib import dbus
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
		# self.cmenu.add_command(label="Изменить", command=self.__show_edit, image=self.__icon_menu_edit, compound="left")


		self.storage = get_storage()


		#
		
		self.current_volume = None
		# self.current_fnode = None


		self.litems = {}				# список загруженных нод
		self.open_cb = None
		self.select_cb = None



	def __make_cmenu(self, e):
		"""отображение контекстного меню"""
		cmenu_selection = self.__tree.identify_row(e.y)		# тек. елемент под курсором

		if cmenu_selection:
			self.__tree.selection_set(cmenu_selection)				# выделяем его
			# self.__select_row(None)									# выполняем действия по отображению выбора

			#--- отображение меню
			# self.cmenu.post(e.x_root, e.y_root)
			self.cmenu.tk_popup(e.x_root, e.y_root)					# автозакрытие при потере фокуса(https://stackoverflow.com/questions/21200516/python3-tkinter-popup-menu-not-closing-automatically-when-clicking-elsewhere)




	def clear(self):
		self.__clear()


	def update_volume(self, volume_uuid):
		self.current_volume = volume_uuid
		self.__clear()
		self.nav_bar.reinit()
		items = self.storage.fetch_volume_files(volume_uuid)

		self.__sort_nodes(items)
		for item in items:
			self.__insert_file(item)




	def update_folder(self, folder_uuid):
		self.__clear()
		self.__insert_parent_files(folder_uuid)



	# def set_open_cb(self, cb):
	# 	self.open_cb = cb


	def set_select_cb(self, cb):
		self.select_cb = cb







	def __go_root(self):
		self.update_volume(self.current_volume)

	def __go_history(self, fnode_uuid):
		self.update_folder(fnode_uuid)




	



	

	def __insert_file(self, fnode):

		if fnode.is_dir():
			ftype = "dir"
			icon = ticons.ficon(ticons.F_FOLDER)
			size = ""
		else:
			ftype = "file"
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

		self.litems[fnode.uuid] = fnode



	def __insert_parent_files(self, parent_id):
		fnodes = self.storage.fetch_parent_files(parent_id)


		self.__sort_nodes(fnodes)

		for fnode in fnodes:
			# print(fnode.name)
			self.__insert_file(fnode)


	
		

	
	def __update_list(self, fnode):

		if fnode.is_dir():
			self.__clear()
			self.__insert_parent_files(fnode.uuid)
			return False





	def __select_row(self, e):
		selection = self.__tree.selection()
		if len(selection) == 0:
			return False
		
		

		selected_item = self.__tree.selection()[0]
		fnode = self.litems[selected_item]

		if self.select_cb:
			self.select_cb(fnode)





	def __open_row(self, e):
		selection = self.__tree.selection()
		if len(selection) == 0:
			return False

		selected_item = self.__tree.selection()[0]
		fnode = self.litems[selected_item]

		if fnode.is_file():
			return False

		self.__update_list(fnode)
		
		self.nav_bar.history_push(fnode)


	





	def __clear(self):
		for row in self.__tree.get_children():
			self.__tree.delete(row)


		self.litems = {}




	def __show_info(self):
		selection = self.__tree.selection()
		if len(selection) == 0:
			return False



		selected_item = self.__tree.selection()[0]
		fnode = self.litems[selected_item]


		dbus.emit(dbus.SHOW_ABOUT_FILE, fnode)




	def __sort_nodes(self, nodes):
		convert = lambda text: int(text) if text.isdigit() else text
		alphanum_key = lambda key: [convert(c) for c in re.split(r'([0-9]+)', key.name)]
		nodes.sort(key=alphanum_key)