#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk
# from ...utils import events, conv

from .DInfo import DInfo
from .VInfo import VInfo
from .FInfo import FInfo

# from . import qicon
from app.storage import get_storage, FRow, FType, VRow
from app.storage.models.VNode import VNode
from app.storage.models.FNode import FNode





class InfoFrame(ttk.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(InfoFrame, self).__init__(parent, *args, **kwargs)


		self.__db_info_frame = DInfo(parent=self)
		self.__db_info_frame.pack(side="top", fill="x")

		self.__volume_info_frame = VInfo(self, width=600)
		self.__volume_info_frame.pack(side="top", fill="x", ipadx=5, ipady=5)

		self.__file_info_frame = FInfo(self)
		self.__file_info_frame.pack(side="top", fill="x", pady=20)


		self.storage = get_storage()

		self.current_item = None


	
		# events.on(events.Event.TREE_SELECT, self.__on_tree_selected)


	#--- public ---------------------------------------------------------------
	def update_volume(self, vnode: VNode):
		"""инфо о томе"""
		self.__volume_info_frame.update_info(vnode)


	def update_file(self, fnode: FNode):
		"""инфо о файле"""
		self.__file_info_frame.update_info(fnode)


	def drop_volume(self):
		"""сброс инфо о томе и соответственно о файле"""
		self.__volume_info_frame.drop_info()						# drop volume
		self.__file_info_frame.drop_info()							# drop file

	def drop_file(self):
		"""сброс инфо о файле"""
		self.__file_info_frame.drop_info()

	# def on_select_file(self, lnode):
	# 	self.__file_info_frame.update_info(lnode.data)
	# 	# self.__on_tree_selected(lnode)
	#--- public ---------------------------------------------------------------


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
