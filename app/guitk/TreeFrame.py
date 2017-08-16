#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.logic import get_tree, load_tree_demo

class TreeFrame(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(TreeFrame, self).__init__(parent, *args, **kwargs)


		label = tkinter.Label(self, text="tree")
		label.pack()

		self.__tree = ttk.Treeview(self, show="tree", selectmode='browse')
		self.__tree.pack(side="left", expand=True, fill="both")


		#--- vertical scroll
		ysb = ttk.Scrollbar(self, orient="vertical", command= self.__tree.yview)
		self.__tree['yscroll'] = ysb.set
		ysb.pack(side="right", expand=False, fill="y")

		self.__tree.column("#0", width=300)
		self.__tree.tag_bind("simple", "<<TreeviewSelect>>", self.__select_row)


		load_tree_demo()
		tree_date = get_tree()


		root = tree_date.get_root()
		root_items = root.childrens

		# self.__tree.insert('', 'end', 'widgets', text='Widget Tour')

		for item in root_items:
			self.__tree.insert('', 'end', item.id, text=item.name, tags=("simple", ))
			self.__wnode(item)

		# #--- обход дерева и добавление элементов
		# def wnode(node, slist):
		# 	values = slist.get(node)
		# 	if values is None: return

		# 	for nodec in sorted(values.keys()):
		# 		slist = values[nodec]
		# 		obj_model = self.project.get_object(nodec)
		# 		self.__tree.insert(node, "end", nodec, text=obj_model.sname, tags=("simple",), open=True)
		# 		wnode(nodec, values)

	
		# #--- запуск обхода дерева
		# for node in sorted(objects_tree.keys()):
		# 	obj_model = self.project.get_object(node)
		# 	self.__tree.insert("", "end", node, text=obj_model.sname, tags=("simple",), open=True)
		# 	wnode(node, objects_tree)



	# def __wnode(self, node, parent, deep):
	def __wnode(self, node):
			"""
				рекурсивный обход элементов и добавление их на форму
			"""

			items = node.childrens

			for item in items:

				name = str(item.id) + " _ " + item.name
				self.__tree.insert(node.id, "end", item.id, text=name, tags=("simple",), open=False)

				self.__wnode(item)

			## if deep == 2:
			## 	return

			# if node.ntype == "f":
			# 	# icon = QIcon(get_icon_path("document-properties.png"))
			# 	icon = qicon("empty.png")
			# elif node.ntype == "d":
			# 	icon = qicon("folder.png")
			# 	# icon = QIcon(get_icon_path("document-open.png"))
			# 	# icon = QIcon(get_icon_path("document-open.png"))
			# else:
			# 	icon = QIcon(get_icon_path("list-remove.png"))

			# row = QStandardItem(node.name)				# элемент строки
			# # row.com_sys_id = node["sys_id"]					# определяем свой атрибут(нужен при выборе)
			# row.setIcon(icon)				# icon
			# row.setEditable(False)							# editable - false

			# row.setData(node.id, Qt.UserRole+1)

			# self.__rows_dict[node.id] = row

			# parent.appendRow(row)							# добавляем


			# #--- ищем всех деток на уровень ниже(не дальше)
			# # child_items = [node for node in simple_obj_list
			# # 			   if (node["tree_lk"] > node_lk) and (node["tree_rk"] < node_rk) and(node["tree_level"] == node_level+1)]

			# # child_items = self.tree.get_childrens(node)
			# child_items = node.childrens


			# #--- для каждого из деток вызываем рекурсию
			# for node in child_items:
			# 	self.__wnode(node, row, deep+1)





	def __init_data(self):
		pass
		# message = """Центр состояния объектов"""
		# tkinter.Label(self.__data_frame, text=message, font=("Helvetica", 12, "bold")).pack()


	def __select_row(self, e):
		self.__current_tree_item = self.__tree.selection()[0]
		self.__make_data()


	def __make_data(self):
		print(self.__current_tree_item)

		# for widget in self.__data_frame.winfo_children():
		# 	widget.destroy()


		# obj_model = self.project.get_object(self.__current_tree_item)

		# frame = IObject(self.__data_frame, model=obj_model)

		# ctrl_frame = tkinter.Frame(self.__data_frame, padx=10, pady=10)
		# ctrl_frame.pack(fill="x", expand=True)
		# # ttk.Button(ctrl_frame, text="Открыть в отдельном окне", command=lambda : DObject(self.__current_tree_item)).pack(side="right")
		# ttk.Button(ctrl_frame, text="Открыть в отдельном окне", command=lambda : show_amodal(self.__current_tree_item)).pack(side="right")




class Separator(tkinter.Frame):
	def __init__(self, parent=None):
		tkinter.Frame.__init__(self, parent)
		self.config(relief="raised", bd=2, height=2)
		self.pack(fill="x", padx=5, pady=5)
