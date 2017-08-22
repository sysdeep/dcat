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
		self.current_volume_id = None
		self.select_cb = None
		self.remove_cb = None
		self.cb_open_modal_add_volume = None

		self.__volumes_map = {}

		controls_frame = ttk.Frame(self)
		controls_frame.pack(side="top", expand=False, fill="x")

		ttk.Button(controls_frame, text="add", command=self.__add_volume).pack(side="left")
		ttk.Button(controls_frame, text="remove", command=self.__remove_volume).pack(side="left")




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
		self.current_volume_id = None
		self.__volumes_map = {}
		self.__insert_volumes()



	def set_select_cb(self, cb):
		self.select_cb = cb

	def set_remove_cb(self, cb):
		self.remove_cb = cb

	def set_cb_open_modal_add_volume(self, cb):
		self.cb_open_modal_add_volume = cb


	def __insert_volumes(self):
		volumes = self.storage.fetch_volumes()
		for vnode in volumes:
			self.__list.insert('', 'end', vnode.uuid, text=vnode.name, tags=("simple", ), image=self.icon_volume)
			self.__volumes_map[vnode.uuid] = vnode



	def __clear(self):
		for row in self.__list.get_children():
			self.__list.delete(row)



	def __select_row(self, e):
		selection = self.__list.selection()
		if len(selection) == 0:
			return False
		
		

		vnode_uuid = self.__list.selection()[0]


		if self.current_volume_id == vnode_uuid:
			return False

		self.current_volume_id = vnode_uuid

		vnode = self.__volumes_map[vnode_uuid]

		if self.select_cb:
			# self.select_cb(selected_item)
			self.select_cb(vnode)


	def __remove_volume(self):
		if self.current_volume_id and self.remove_cb:
			print(self.current_volume_id)
			self.remove_cb(self.current_volume_id)



	def __add_volume(self):
		if self.cb_open_modal_add_volume:
			self.cb_open_modal_add_volume()