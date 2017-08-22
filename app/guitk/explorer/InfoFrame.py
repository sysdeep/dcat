#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk
from ..utils import events, conv

from .VInfo import VInfo
from .FInfo import FInfo

# from . import qicon
from app.storage import get_storage, FRow, FType, VRow

class InfoFrame(ttk.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(InfoFrame, self).__init__(parent, *args, **kwargs)


		self.vinfo = VInfo(self, width=600)
		self.vinfo.pack(side="top", fill="x", ipadx=5, ipady=5)

		self.finfo = FInfo(self)
		self.finfo.pack(side="top", fill="x", pady=20)


		self.storage = get_storage()

		self.current_item = None


	
		# events.on(events.Event.TREE_SELECT, self.__on_tree_selected)



	def update_volume(self, vnode):
		self.vinfo.update_info(vnode)


	def update_file(self, fnode):
		self.finfo.update_info(fnode)


	def on_select_file(self, lnode):
		self.finfo.update_info(lnode.data)
		# self.__on_tree_selected(lnode)


	# def __on_tree_selected(self, item):
	# 	if self.current_item is None:
	# 		self.current_item = item
	# 		self.__update_info()
	# 		return True

	# 	if self.current_item.uuid != item.uuid:
	# 		self.current_item = item
	# 		self.__update_info()
	# 		return True

	# 	return False


	# def __update_info(self):
		
	# 	if self.current_item.ftype == "volume":
	# 		return False		

	# 	for i, l in enumerate(self.litems):
	# 		value = self.current_item.data[l]
	# 		print(value)
	# 		label = self.labels[i]
			

	# 		if l == "ctime":
	# 			r = conv.convert_ctime(value)
	# 			print(r)
	# 			label.configure(text=r)
	# 		else:
	# 			label.configure(text=value)




	# 	if self.parent_id == item_id:
	# 		return False

	# 	self.parent_id = item_id
	# 	self.__clear()
			
		
	# 	if item_type == FType.FILE:
	# 		return False


	# 	if item_type == FType.DIR:
	# 		items = self.storage.find_childrens(self.parent_id)
	# 	elif item_type == FType.VOLUME:
	# 		items = self.storage.find_volume_items(self.parent_id, "0")
	# 	else:
	# 		return False


	# 	for f in items:



	# 		if f[FRow.TYPE] == FType.DIR:
	# 			icon = self.icon_folder
	# 		else:
	# 			icon = self.icon_file


	# 		ivalues = (
	# 			str(f[FRow.SIZE]),
	# 			f[FRow.RIGHTS],
	# 			f[FRow.OWNER],
	# 			f[FRow.GROUP],
	# 			f[FRow.CTIME],
	# 			f[FRow.ATIME],
	# 			f[FRow.MTIME],
	# 		)

	# 		# self.__tree.insert("", 'end', f[FRow.UUID], text=f[FRow.NAME], tags=("simple", ), image=icon, values=("111", "222"))
	# 		self.__tree.insert("", 'end', f[FRow.UUID], text=f[FRow.NAME], tags=("simple", ), image=icon, values=ivalues)





				
	# def __clear(self):
	# 	for row in self.__tree.get_children():
	# 		self.__tree.delete(row)
