#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

from app.logic import get_tree
from app.rc import get_icon_path
from . import events


class Tree(QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)

		self.model = QStandardItemModel()
		self.model.setHorizontalHeaderLabels(['name'])
		self.setModel(self.model)
		self.setUniformRowHeights(True)
		# self.setHeaderHidden(True)
		self.setFixedWidth(300)

		self.tree = get_tree()

		events.on("update_tree", self.__update_tree)


	def __update_tree(self):
		self.model.clear()
		self.__make_tree()


	def update_tree(self):
		self.__make_tree()


	def __make_tree(self):

		#--- запуск обхода дерева
		root_items = self.tree.get_nodes_level(1)		# все элементы корня
		for item in root_items:
			self.__wnode(item, self.model)



	def __wnode(self, node, parent):
			"""
				рекурсивный обход элементов и добавление их на форму
			"""
			if node.ntype == "f":
				icon = QIcon(get_icon_path("document-properties.png"))
			elif node.ntype == "d":
				icon = QIcon(get_icon_path("document-open.png"))
			else:
				icon = QIcon(get_icon_path("list-remove.png"))

			row = QStandardItem(node.name)				# элемент строки
			# row.com_sys_id = node["sys_id"]					# определяем свой атрибут(нужен при выборе)
			row.setIcon(icon)				# icon
			row.setEditable(False)							# editable - false
			parent.appendRow(row)							# добавляем


			#--- ищем всех деток на уровень ниже(не дальше)
			# child_items = [node for node in simple_obj_list
			# 			   if (node["tree_lk"] > node_lk) and (node["tree_rk"] < node_rk) and(node["tree_level"] == node_level+1)]

			child_items = self.tree.get_childrens(node)


			#--- для каждого из деток вызываем рекурсию
			for node in child_items:
				self.__wnode(node, row)