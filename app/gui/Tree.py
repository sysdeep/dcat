#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from app.logic import get_tree
from app.rc import get_icon_path
from . import events, qicon


class Tree(QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)


		self.select_cb = None

		self.model = QStandardItemModel()
		self.model.setHorizontalHeaderLabels(['name'])
		self.setModel(self.model)
		self.setUniformRowHeights(True)
		# self.setHeaderHidden(True)
		self.setFixedWidth(300)

		self.__rows_dict = {}
		self.tree = get_tree()

		events.on("update_tree", self.__update_tree)

		self.clicked.connect(self.__select)
		self.expanded.connect(self.__expanded_item)


	def __update_tree(self):
		self.model.clear()
		self.__make_tree()


	def update_tree(self):
		self.__make_tree()


	def __make_tree(self):

		#--- запуск обхода дерева
		# root_items = self.tree.get_nodes_level(1)		# все элементы корня
		root = self.tree.get_root()
		root_items = root.childrens

		for item in root_items:
			self.__wnode(item, self.model, 0)



	def __wnode(self, node, parent, deep):
			"""
				рекурсивный обход элементов и добавление их на форму
			"""
			# if deep == 2:
			# 	return

			if node.ntype == "f":
				# icon = QIcon(get_icon_path("document-properties.png"))
				icon = qicon("empty.png")
			elif node.ntype == "d":
				icon = qicon("folder.png")
				# icon = QIcon(get_icon_path("document-open.png"))
				# icon = QIcon(get_icon_path("document-open.png"))
			else:
				icon = QIcon(get_icon_path("list-remove.png"))

			row = QStandardItem(node.name)				# элемент строки
			# row.com_sys_id = node["sys_id"]					# определяем свой атрибут(нужен при выборе)
			row.setIcon(icon)				# icon
			row.setEditable(False)							# editable - false

			row.setData(node.id, Qt.UserRole+1)

			self.__rows_dict[node.id] = row

			parent.appendRow(row)							# добавляем


			#--- ищем всех деток на уровень ниже(не дальше)
			# child_items = [node for node in simple_obj_list
			# 			   if (node["tree_lk"] > node_lk) and (node["tree_rk"] < node_rk) and(node["tree_level"] == node_level+1)]

			# child_items = self.tree.get_childrens(node)
			child_items = node.childrens


			#--- для каждого из деток вызываем рекурсию
			for node in child_items:
				self.__wnode(node, row, deep+1)


	def __select(self, index):
		
		selected_id = index.data(Qt.UserRole+1)
		# print(d)

		if self.select_cb:
			self.select_cb(selected_id)







	def __expanded_item(self, model_index):
		selected_id = model_index.data(Qt.UserRole+1)
		print(selected_id)

		# node = self.tree.get_node_id(selected_id)
		# # print(node)

		
		

		# for x in node.childrens:
		# 	tree_branch = self.__rows_dict[x.id]
		# 	self.__wnode(x, tree_branch, 0)