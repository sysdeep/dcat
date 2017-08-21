#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.storage import get_storage
from ..utils import qicon

class VList(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(VList, self).__init__(parent, *args, **kwargs)


		self.storage = get_storage()
		self.icon_volume = qicon("document_save.png")
		self.select_cb = None

		self.__list = ttk.Treeview(self, show="tree", selectmode='browse')
		self.__list.pack(side="left", expand=True, fill="both")


		#--- vertical scroll
		ysb = ttk.Scrollbar(self, orient="vertical", command= self.__list.yview)
		self.__list['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")

		self.__list.column("#0", width=200)
		self.__list.tag_bind("simple", "<<TreeviewSelect>>", self.__select_row)
		# self.__list.bind("<Double-1>", self.__open_row)




	def reload_volumes(self):
		self.__clear()
		self.__insert_volumes()

	def set_select_cb(self, cb):
		self.select_cb = cb



	def __insert_volume(self, volume_row):
		volume_id = volume_row["uuid"]
		volume_name = volume_row["name"]
		self.__list.insert('', 'end', volume_id, text=volume_name, tags=("simple", ), image=self.icon_volume)
		
		# # self.current_items[item_volume_id] = volume_name

		# lnode = LNode(volume_id, "volume")
		# lnode.data = volume_row
		# lnode.name = volume_name
		# self.litems[volume_id] = lnode





	def __insert_volumes(self):
		volumes = self.storage.fetch_volumes()
		for item in volumes:
			self.__insert_volume(item)



	def __clear(self):
		for row in self.__list.get_children():
			self.__list.delete(row)



	def __select_row(self, e):
		selection = self.__list.selection()
		if len(selection) == 0:
			return False
		
		

		selected_item = self.__list.selection()[0]


		if self.select_cb:
			self.select_cb(selected_item)