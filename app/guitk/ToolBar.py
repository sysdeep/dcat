#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.storage import get_storage
from .utils import qicon, volume_icon

class ToolBar(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(ToolBar, self).__init__(parent, *args, **kwargs)


		
		# self.select_cb = None
		# self.remove_cb = None
		# self.cb_open_modal_add_volume = None

		# self.is_locked = True

		# self.__volumes_map = {}

		# controls_frame = ttk.Frame(self)
		# controls_frame.pack(side="top", expand=False, fill="x")

		# self.volume_icons = []

		self.icon_remove = qicon("edittrash.png")
		self.icon_unlock = qicon("decrypted.png")
		self.icon_add = qicon("edit_add.png")

		self.btn_open = ttk.Button(self, text="open", command=self.__show_open, image=self.icon_unlock)
		self.btn_open.pack(side="left")

		# self.btn_add_volume = ttk.Button(self, text="add", command=self.__add_volume, image=self.icon_add)
		# self.btn_add_volume.pack(side="left")
		# self.btn_add_volume.config(state="disabled")
		#
		# self.btn_remove_volume = ttk.Button(self, text="remove", command=self.__remove_volume, image=self.icon_remove)
		# self.btn_remove_volume.pack(side="left")
		# self.btn_remove_volume.config(state="disabled")



	def __show_open(self):
		pass


	# def reload_volumes(self):
	# 	"""обновление списка томов"""
	# 	self.__clear()
	# 	self.current_volume_id = None
	# 	self.__volumes_map = {}
	# 	self.__insert_volumes()
	# 	self.is_locked = True
	# 	self.__update_buttons_state()



	


	# def __insert_volumes(self):
	# 	self.volume_icons = []
	# 	volumes = self.storage.fetch_volumes()
	# 	for vnode in volumes:
	# 		ivolume = volume_icon(vnode.vtype)
	# 		self.volume_icons.append(ivolume)
	# 		self.__list.insert('', 'end', vnode.uuid, text=vnode.name, tags=("simple", ), image=ivolume)
	# 		self.__volumes_map[vnode.uuid] = vnode



	# def __clear(self):
	# 	for row in self.__list.get_children():
	# 		self.__list.delete(row)



	# def __select_row(self, e):
	# 	selection = self.__list.selection()
	# 	if len(selection) == 0:
	# 		return False
		
		

	# 	vnode_uuid = self.__list.selection()[0]


	# 	if self.current_volume_id == vnode_uuid:
	# 		return False

	# 	self.current_volume_id = vnode_uuid

	# 	vnode = self.__volumes_map[vnode_uuid]

	# 	if self.select_cb:
	# 		# self.select_cb(selected_item)
	# 		self.select_cb(vnode)





	# #--- toolbar actions ------------------------------------------------------
	# def __remove_volume(self):
	# 	if self.current_volume_id and self.remove_cb:
	# 		print(self.current_volume_id)
	# 		self.remove_cb(self.current_volume_id)



	# def __add_volume(self):
	# 	if self.cb_open_modal_add_volume:
	# 		self.cb_open_modal_add_volume()



	# def __toggle_lock(self):
	# 	self.is_locked = not self.is_locked
	# 	self.__update_buttons_state()

	# #--- toolbar actions ------------------------------------------------------
		


	# def __update_buttons_state(self):
	# 	if self.is_locked:
	# 		self.btn_add_volume.config(state="disabled")
	# 		self.btn_remove_volume.config(state="disabled")
	# 	else:
	# 		self.btn_add_volume.config(state="normal")
	# 		self.btn_remove_volume.config(state="normal")










	# #--- set cbs --------------------------------------------------------------
	# def set_select_cb(self, cb):
	# 	self.select_cb = cb

	# def set_remove_cb(self, cb):
	# 	self.remove_cb = cb

	# def set_cb_open_modal_add_volume(self, cb):
	# 	self.cb_open_modal_add_volume = cb
	# #--- set cbs --------------------------------------------------------------