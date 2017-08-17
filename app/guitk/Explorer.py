#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk, PhotoImage

from app.logic import get_tree, load_tree_demo
from app.storage import get_storage, VRow, FRow, FType
from .utils.events import select_tree_item
from . import qicon

from .StackFrame import StackFrame
from .explorer.NavBar import NavBar


class StackItem(object):
	def __init__(self, uuid, name):
		self.uuid = uuid
		self.name = name



class Explorer(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(Explorer, self).__init__(parent, *args, **kwargs)



		label = tkinter.Label(self, text="explorer")
		label.pack()

		self.stack_frame = StackFrame(self)
		self.stack_frame.pack()
		self.stack_frame.on_change(self.__go_history)

		self.nav_bar = NavBar(self)
		self.nav_bar.pack()

		columns=('size', 'rights', "owner", "group", "ctime", "atime", "mtime")
		self.__tree = ttk.Treeview(self, show="tree headings", selectmode='browse', columns=columns)
		self.__tree.heading("size", text="Размер")
		self.__tree.heading("rights", text="Права")
		self.__tree.heading("owner", text="Владелец")
		self.__tree.heading("group", text="Группа")
		self.__tree.heading("ctime", text="Создание")
		self.__tree.heading("atime", text="Доступ")
		self.__tree.heading("mtime", text="Модификация")
		self.__tree.heading('#0', text='Название')
		self.__tree.pack(side="left", expand=True, fill="both")


		#--- vertical scroll
		ysb = ttk.Scrollbar(self, orient="vertical", command= self.__tree.yview)
		self.__tree['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")

		self.__tree.column("#0", width=300)
		# self.__tree.tag_bind("simple", "<<TreeviewSelect>>", self.__select_row)
		self.__tree.bind("<Double-1>", self.__select_row)
		# self.__tree.tag_bind("simple", "<<TreeviewOpen>>", self.__open_row)



		self.storage = get_storage()


		self.icon_folder = qicon("folder.png")
		self.icon_file = qicon("empty.png")
		self.icon_volume = qicon("document_save.png")


		root_stack_item = StackItem("0|r", "root")
		self.history_stack = [root_stack_item]
		self.stack_frame.update_items(self.history_stack)
		self.nav_bar.update_history(self.history_stack)




		self.current_items = {}

		self.__make_tree()
		

	def __insert_volume(self, volume_row):
		volume_id = volume_row[VRow.UUID]
		volume_name = volume_row[VRow.NAME]
		item_volume_id = volume_id + "|" + "v"
		self.__tree.insert('', 'end', item_volume_id, text=volume_name, tags=("simple", ), image=self.icon_volume)
		self.current_items[item_volume_id] = volume_name

	def __insert_volumes(self):
		volumes = self.storage.fetch_volumes()
		for item in volumes:
			self.__insert_volume(item)


	def __insert_file(self, file_row):
		if file_row[FRow.TYPE] == FType.DIR:
			icon = self.icon_folder
			item_id = file_row[FRow.UUID] + "|" + "d"
		else:
			icon = self.icon_file
			item_id = file_row[FRow.UUID] + "|" + "f"


		ivalues = (
				str(file_row[FRow.SIZE]),
				file_row[FRow.RIGHTS],
				file_row[FRow.OWNER],
				file_row[FRow.GROUP],
				file_row[FRow.CTIME],
				file_row[FRow.ATIME],
				file_row[FRow.MTIME],
			)

		self.__tree.insert("", 'end', item_id, text=file_row[FRow.NAME], tags=("simple", ), image=icon, values=ivalues)
		self.current_items[item_id] = file_row[FRow.NAME]
		print(self.current_items)


	def __insert_back(self):
		self.__tree.insert("", 'end', "back_id|back_id", text="..", tags=("simple", ))



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


	def __make_tree(self):

		self.__insert_volumes()
		
			





	def __init_data(self):
		pass
		# message = """Центр состояния объектов"""
		# tkinter.Label(self.__data_frame, text=message, font=("Helvetica", 12, "bold")).pack()




	def __go_history(self, index):

		item = self.history_stack[index]

		self.history_stack = self.history_stack[:index]
		# self.history_stack = self.history_stack[:index+1]
		# self.stack_frame.update_items(self.history_stack)

		print("go history: ", item.uuid)
		self.__update_list(item.uuid)


	def __update_list(self, vuuid):
		# self.current_items = {}
		selected_item = vuuid

		is_back = False

		if selected_item == "back_id|back_id":
			is_back = True

			#--- drop last
			self.history_stack.pop()
			self.stack_frame.update_items(self.history_stack)

			#--- get last
			stack_item = self.history_stack[-1]

			#--- if this is root
			if stack_item.name == "root":
				selected_item = "0|r"
			else:
				selected_item = stack_item.uuid


		if selected_item == "0|r":
			print("correct ctack")
			# print(self.history_stack)
			# self.history_stack = self.history_stack[:1]
			root_stack_item = StackItem("0|r", "root")
			self.history_stack = [root_stack_item]
			self.stack_frame.update_items(self.history_stack)


		sarray = selected_item.split("|")
		item_id = sarray[0]
		item_type = sarray[1]

		print("-------------")
		print(self.current_items)
		print("-------------")
		if is_back is False:

			if selected_item != "0|r":

				item_name = self.current_items[selected_item]
				stack_item = StackItem(selected_item, item_name)
				# stack_item = StackItem(selected_item, item_id)
				self.history_stack.append(stack_item)
				self.stack_frame.update_items(self.history_stack)



		


		


		if item_type == "v":
			item_type = FType.VOLUME
			self.__clear()
			self.__insert_root_files(item_id)
		elif item_type == "d":
			item_type = FType.DIR
			self.__clear()
			self.__insert_parent_files(item_id)
		elif item_type == "f":
			item_type = FType.FILE
			# self.__insert_back()
		elif item_type == "r":
			self.__clear()
			self.__insert_volumes()
		else:
			item_type = FType.UNKNOWN



	def __select_row(self, e):
		selection = self.__tree.selection()
		if len(selection) == 0:
			return False

		selected_item = self.__tree.selection()[0]

		self.__update_list(selected_item)

		
		


		


	def __clear(self):
		for row in self.__tree.get_children():
			self.__tree.delete(row)




