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



class LNode(object):
	def __init__(self, uuid, ftype):
		self.uuid = uuid
		self.ftype = ftype
		self.name = ""

		self.data = None



class Explorer(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(Explorer, self).__init__(parent, *args, **kwargs)


		self.nav_bar = NavBar(self)
		self.nav_bar.pack(side="top", fill="x")
		self.nav_bar.set_cb_back(self.__go_back)
		self.nav_bar.set_cb_root(self.__remake_tree)
		self.nav_bar.set_cb_go(self.__go_history)



		self.v_list = VList(self)
		self.v_list.pack(side="left", expand=True, fill="both")


		self.__sort_dir = False

		columns=('size', 'rights', "owner", "group", "ctime", "atime", "mtime")
		self.__tree = ttk.Treeview(self, show="tree headings", selectmode='browse', columns=columns)
		# self.__tree.heading("size", text="Размер", command=lambda c="size": self.__sort(c))
		self.__tree.heading("size", text="Размер")
		self.__tree.heading("rights", text="Права")
		self.__tree.heading("owner", text="Владелец")
		self.__tree.heading("group", text="Группа")
		self.__tree.heading("ctime", text="Создание")
		self.__tree.heading("atime", text="Доступ")
		self.__tree.heading("mtime", text="Модификация")
		self.__tree.heading('#0', text='Название')

		self.__tree.column("#0", minwidth=200, width=200)
		self.__tree.column("size", minwidth=50, width=60)
		self.__tree.column("rights", minwidth=40, width=50)
		self.__tree.column("owner", minwidth=80, width=80)
		self.__tree.column("group", minwidth=80, width=80)
		self.__tree.column("ctime", minwidth=90, width=90)
		self.__tree.column("atime", minwidth=90, width=90)
		self.__tree.column("mtime", minwidth=100, width=100)


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



		self.storage = get_storage()


		self.icon_folder = qicon("folder.png")
		self.icon_file = qicon("empty.png")
		self.icon_volume = qicon("document_save.png")


		# root_stack_item = StackItem("0|r", "root")
		# self.history_stack = [root_stack_item]
		self.history_stack = []
		# self.stack_frame.update_items(self.history_stack)
		# self.nav_bar.update_history(self.history_stack)




		self.current_items = {}
		self.litems = {}


		self.v_list.reload_volumes()
		self.__remake_tree()
		


	def __remake_tree(self):
		self.__clear()
		self.__history_clear()
		self.__insert_volumes()






	def __insert_volume(self, volume_row):
		volume_id = volume_row["uuid"]
		volume_name = volume_row["name"]
		# item_volume_id = volume_id + "|" + "v"
		# self.__tree.insert('', 'end', item_volume_id, text=volume_name, tags=("simple", ), image=self.icon_volume)
		self.__tree.insert('', 'end', volume_id, text=volume_name, tags=("simple", ), image=self.icon_volume)
		
		# self.current_items[item_volume_id] = volume_name

		lnode = LNode(volume_id, "volume")
		lnode.data = volume_row
		lnode.name = volume_name
		self.litems[volume_id] = lnode





	def __insert_volumes(self):
		volumes = self.storage.fetch_volumes()
		for item in volumes:
			self.__insert_volume(item)


	def __insert_file(self, file_row):

		file_id = file_row[FRow.UUID]
		file_name = file_row[FRow.NAME]

		if file_row[FRow.TYPE] == FType.DIR:
			ftype = "dir"
			icon = self.icon_folder
			item_id = file_row[FRow.UUID] + "|" + "d"
		else:
			ftype = "file"
			icon = self.icon_file
			item_id = file_row[FRow.UUID] + "|" + "f"


		ivalues = (
				str(file_row[FRow.SIZE]),
				file_row[FRow.RIGHTS],
				file_row[FRow.OWNER],
				file_row[FRow.GROUP],
				conv.convert_ctime(file_row[FRow.CTIME]),
				conv.convert_ctime(file_row[FRow.ATIME]),
				conv.convert_ctime(file_row[FRow.MTIME]),
			)

		# ivalues = (
		# 		str(file_row[FRow.SIZE]),
		# 		file_row[FRow.RIGHTS],
		# 		file_row[FRow.OWNER],
		# 		file_row[FRow.GROUP],
		# 		file_row[FRow.CTIME],
		# 		file_row[FRow.ATIME],
		# 		file_row[FRow.MTIME],
		# 	)

		# self.__tree.insert("", 'end', item_id, text=file_row[FRow.NAME], tags=("simple", ), image=icon, values=ivalues)
		self.__tree.insert("", 'end', file_id, text=file_row[FRow.NAME], tags=("simple", ), image=icon, values=ivalues)
		# self.current_items[item_id] = file_row[FRow.NAME]
		# print(self.current_items)


		lnode = LNode(file_row[FRow.UUID], ftype)
		lnode.data = file_row
		lnode.name = file_name
		self.litems[file_row[FRow.UUID]] = lnode


	def __insert_back(self):
		self.__tree.insert("", 'end', "back_id", text="..", tags=("simple", ))



	def __insert_root_files(self, volume_id):
		items = self.storage.fetch_volume_files(volume_id)

		self.__insert_back()
		for item in items:
			self.__insert_file(item)



	def __insert_parent_files(self, parent_id):
		items = self.storage.fetch_parent_files(parent_id)

		self.__insert_back()
		for item in items:
			self.__insert_file(item)


	
		
			





	def __init_data(self):
		pass
		# message = """Центр состояния объектов"""
		# tkinter.Label(self.__data_frame, text=message, font=("Helvetica", 12, "bold")).pack()




	def __go_history(self, index):

		current_item = self.__history_splice(index)
		# item = self.history_stack[index]

		# self.history_stack = self.history_stack[:index]
		# # self.history_stack = self.history_stack[:index+1]
		# # self.stack_frame.update_items(self.history_stack)

		# print("go history: ", item.uuid)
		self.__update_list(current_item)



	
	def __update_list(self, item):

		if item.ftype == "volume":
			self.__clear()
			self.__insert_root_files(item.uuid)
			return False


		if item.ftype == "dir":
			self.__clear()
			self.__insert_parent_files(item.uuid)
			return False






	def __select_row(self, e):
		selection = self.__tree.selection()
		if len(selection) == 0:
			return False
		
		

		selected_item = self.__tree.selection()[0]

		if selected_item == "back_id":
			return False

		item = self.litems[selected_item]

		select_tree_item(item)

	def __open_row(self, e):
		selection = self.__tree.selection()
		if len(selection) == 0:
			return False

		selected_item = self.__tree.selection()[0]

		if selected_item == "back_id":
			self.__go_back()
			return False


		item = self.litems[selected_item]


		if item.ftype == "file":
			return False

		
		self.__history_push(item)

		self.__update_list(item)




		
	def __go_back(self):

		# self.history_stack.pop()
		self.__history_pop()
		if len(self.history_stack) == 0:
			self.__clear()
			self.__insert_volumes()
			return False

		
		

		curr_item = self.__history_last()
		self.__update_list(curr_item)
		









	def __clear(self):
		for row in self.__tree.get_children():
			self.__tree.delete(row)


		self.litems = {}





	def __history_push(self, item):
		self.history_stack.append(item)
		self.nav_bar.update_history(self.history_stack)

	def __history_pop(self):
		item = self.history_stack.pop()
		self.nav_bar.update_history(self.history_stack)
		return item

	def __history_last(self):
		return self.history_stack[-1]

	def __history_clear(self):
		self.history_stack = []
		self.nav_bar.update_history(self.history_stack)

	def __history_splice(self, index):
		item = self.history_stack[index]
		self.history_stack = self.history_stack[:index+1]
		self.nav_bar.update_history(self.history_stack)
		return item








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