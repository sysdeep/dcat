#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.storage import get_storage
from ..utils import qicon, volume_icon

class VList(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(VList, self).__init__(parent, *args, **kwargs)


		self.storage = get_storage()
		self.icon_volume = qicon("document_save.png")
		self.current_volume_id = None

		self.select_cb = None
		self.remove_cb = None
		self.cb_open_modal_add_volume = None
		self.cb_open_db = None

		self.is_locked = True

		self.__volumes_map = {}

		controls_frame = tkinter.Frame(self)
		controls_frame.pack(side="top", expand=False, fill="x")

		self.volume_icons = []

		self.icon_remove = qicon("edittrash.png")
		self.icon_unlock = qicon("decrypted.png")
		self.icon_add = qicon("edit_add.png")
		self.icon_open = qicon("document_open.png")


		self.btn_open = tkinter.Button(controls_frame, text="open", command=self.__open_db, image=self.icon_open, relief="flat")
		# self.btn_open = ttk.Button(controls_frame, text="open", command=self.__open_db, image=self.icon_open)
		self.btn_open.pack(side="left")

		self.btn_lock = tkinter.Button(controls_frame, text="unlock", command=self.__toggle_lock, image=self.icon_unlock, relief="flat")
		self.btn_lock.pack(side="left")

		self.btn_add_volume = tkinter.Button(controls_frame, text="add", command=self.__add_volume, image=self.icon_add, relief="flat")
		self.btn_add_volume.pack(side="left")
		self.btn_add_volume.config(state="disabled")
		
		self.btn_remove_volume = tkinter.Button(controls_frame, text="remove", command=self.__remove_volume, image=self.icon_remove, relief="flat")
		self.btn_remove_volume.pack(side="left")
		self.btn_remove_volume.config(state="disabled")




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
		"""обновление списка томов"""
		self.__clear()
		self.current_volume_id = None
		self.__volumes_map = {}
		self.__insert_volumes()
		self.is_locked = True
		self.__update_buttons_state()



	


	def __insert_volumes(self):
		self.volume_icons = []
		volumes = self.storage.fetch_volumes()
		for vnode in volumes:
			ivolume = volume_icon(vnode.vtype)
			self.volume_icons.append(ivolume)
			self.__list.insert('', 'end', vnode.uuid, text=vnode.name, tags=("simple", ), image=ivolume)
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





	#--- toolbar actions ------------------------------------------------------
	def __remove_volume(self):
		if self.current_volume_id and self.remove_cb:
			print(self.current_volume_id)
			self.remove_cb(self.current_volume_id)



	def __add_volume(self):
		if self.cb_open_modal_add_volume:
			self.cb_open_modal_add_volume()



	def __toggle_lock(self):
		self.is_locked = not self.is_locked
		self.__update_buttons_state()


	def __open_db(self):
		if self.cb_open_db:
			self.cb_open_db()
	#--- toolbar actions ------------------------------------------------------
		


	def __update_buttons_state(self):
		if self.is_locked:
			self.btn_add_volume.config(state="disabled")
			self.btn_remove_volume.config(state="disabled")
		else:
			self.btn_add_volume.config(state="normal")
			self.btn_remove_volume.config(state="normal")










	#--- set cbs --------------------------------------------------------------
	def set_select_cb(self, cb):
		self.select_cb = cb

	def set_remove_cb(self, cb):
		self.remove_cb = cb

	def set_cb_open_modal_add_volume(self, cb):
		self.cb_open_modal_add_volume = cb

	def set_cb_open_db(self, cb):
		self.cb_open_db = cb
	#--- set cbs --------------------------------------------------------------