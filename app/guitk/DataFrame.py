#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk
from .utils import events
from . import qicon
from app.storage import get_storage, FRow, FType, VRow

class DataFrame(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(DataFrame, self).__init__(parent, *args, **kwargs)


		self.storage = get_storage()
		self.parent_id = None


		self.icon_folder = qicon("folder.png")
		self.icon_file = qicon("empty.png")
		self.icon_volume = qicon("document_save.png")

		label = tkinter.Label(self, text="data")
		label.pack()


		columns=('size', 'rights', "owner", "group", "ctime", "atime", "mtime")
		# self.__tree = ttk.Treeview(self, show="tree", selectmode='browse', columns=columns)
		# self.__tree = ttk.Treeview(self, selectmode='browse', show="headings", columns=columns, displaycolumns=columns)
		self.__tree = ttk.Treeview(self, selectmode='browse', show="tree headings", columns=columns, displaycolumns=columns)
		self.__tree.heading("size", text="Размер")
		self.__tree.heading("rights", text="Права")
		self.__tree.heading("owner", text="Владелец")
		self.__tree.heading("group", text="Группа")
		self.__tree.heading("ctime", text="Создание")
		self.__tree.heading("atime", text="Доступ")
		self.__tree.heading("mtime", text="Модификация")
		self.__tree.heading('#0', text='Name')
		self.__tree.pack(side="left", expand=True, fill="both")

		#--- vertical scroll
		ysb = ttk.Scrollbar(self, orient="vertical", command= self.__tree.yview)
		self.__tree['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")



		events.on(events.Event.TREE_SELECT, self.__on_tree_selected)



	def __on_tree_selected(self, item_id, item_type):
		if self.parent_id == item_id:
			return False

		self.parent_id = item_id
		self.__clear()
			
		
		if item_type == FType.FILE:
			return False


		if item_type == FType.DIR:
			items = self.storage.find_childrens(self.parent_id)
		elif item_type == FType.VOLUME:
			items = self.storage.find_volume_items(self.parent_id, "0")
		else:
			return False


		for f in items:



			if f[FRow.TYPE] == FType.DIR:
				icon = self.icon_folder
			else:
				icon = self.icon_file


			ivalues = (
				str(f[FRow.SIZE]),
				f[FRow.RIGHTS],
				f[FRow.OWNER],
				f[FRow.GROUP],
				f[FRow.CTIME],
				f[FRow.ATIME],
				f[FRow.MTIME],
			)

			# self.__tree.insert("", 'end', f[FRow.UUID], text=f[FRow.NAME], tags=("simple", ), image=icon, values=("111", "222"))
			self.__tree.insert("", 'end', f[FRow.UUID], text=f[FRow.NAME], tags=("simple", ), image=icon, values=ivalues)





				
	def __clear(self):
		for row in self.__tree.get_children():
			self.__tree.delete(row)