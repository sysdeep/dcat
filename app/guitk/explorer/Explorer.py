#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk, PhotoImage

from app.logic import get_tree, load_tree_demo
from app.storage import get_storage, VRow, FRow, FType
from ..utils.events import select_tree_item
from ..utils import qicon, conv

from .NavBar import NavBar
from .VList import VList
from .FList import FList
from .InfoFrame import InfoFrame


class LNode(object):
	def __init__(self, uuid, ftype):
		self.uuid = uuid
		self.ftype = ftype
		self.name = ""

		self.data = None



class Explorer(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(Explorer, self).__init__(parent, *args, **kwargs)



		self.v_list = VList(self)
		self.v_list.pack(side="left", expand=True, fill="both")
		self.v_list.set_select_cb(self.__on_select_volume)
		self.v_list.set_remove_cb(self.__on_remove_volume)

		self.f_list = FList(self)
		self.f_list.pack(side="left", expand=True, fill="both")
		self.f_list.set_select_cb(self.__on_select_frow)
		# self.f_list.set_open_cb(self.__on_open_frow)

		self.info_frame = InfoFrame(self)
		self.info_frame.pack(side="right", expand=True, fill="both")
		

		self.storage = get_storage()


		self.icon_folder = qicon("folder.png")
		self.icon_file = qicon("empty.png")
		self.icon_volume = qicon("document_save.png")


		
		# self.history_stack = []
		# self.current_volume = None
		self.current_vnode = None


		self.v_list.reload_volumes()
		




	def refresh(self):
		self.f_list.clear()
		self.v_list.reload_volumes()



	#--- volume actions -------------------------------------------------------
	def __on_select_volume(self, vnode):
		self.current_vnode = vnode
		self.f_list.update_volume(self.current_vnode.uuid)
		self.info_frame.update_volume(self.current_vnode)



	def __on_remove_volume(self, volume_uuid):
		
		self.storage.remove_volume(volume_uuid)
		self.refresh()
	#--- volume actions -------------------------------------------------------









	def __on_select_frow(self, fnode):
		self.info_frame.update_file(fnode)





















	# def __on_open_frow(self, lnode):
	# 	self.__history_push(lnode)










	# def __go_back(self):

		
	# 	self.__history_pop()


	# 	if len(self.history_stack) == 0:
	# 		self.f_list.update_volume(self.current_volume)
	# 		self.nav_bar.update_history(self.history_stack)
	# 		return False

	# 	current_lnode = self.__history_last()
	# 	self.nav_bar.update_history(self.history_stack)
	# 	self.f_list.update_folder(current_lnode.uuid)




	# def __go_history(self, index):

	# 	current_lnode = self.__history_splice(index)
	# 	self.f_list.update_folder(current_lnode.uuid)














	# def __history_push(self, item):
	# 	self.history_stack.append(item)
	# 	self.nav_bar.update_history(self.history_stack)

	# def __history_pop(self):
	# 	item = self.history_stack.pop()
	# 	self.nav_bar.update_history(self.history_stack)
	# 	return item

	# def __history_last(self):
	# 	return self.history_stack[-1]

	# def __history_clear(self):
	# 	self.history_stack = []
	# 	self.nav_bar.update_history(self.history_stack)

	# def __history_splice(self, index):
	# 	item = self.history_stack[index]
	# 	self.history_stack = self.history_stack[:index+1]
	# 	self.nav_bar.update_history(self.history_stack)
	# 	return item








	# def __sort(self, col):
	# 	"""соктировка"""
	# 	# grab values to sort as a list of tuples (column value, column id)
	# 	# e.g. [('Argentina', 'I001'), ('Australia', 'I002'), ('Brazil', 'I003')]
	# 	data = [(self.__tree.set(child, col), child) for child in self.__tree.get_children('')]

	# 	# reorder data
	# 	# tkinter looks after moving other items in
	# 	# the same row
	# 	# data.sort(reverse=descending)
	# 	data.sort(reverse=self.__sort_dir)
	# 	for indx, item in enumerate(data):
	# 		self.__tree.move(item[1], '', indx)   # item[1] = item Identifier

	# 	self.__sort_dir = not self.__sort_dir