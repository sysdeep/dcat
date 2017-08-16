#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from app.logic import get_tree
from app.rc import get_icon_path
from . import events, qicon


class NodeStat(QWidget):
	def __init__(self, parent=None):
		super(NodeStat, self).__init__(parent)

		self.tree = get_tree()

		self.main_layout = QGridLayout(self)


		self.items = (
			"name", "ntype", "st_size", "st_atime", "st_mtime", "st_ctime",
			"id", "id_parent", "level"
		)
		self.labels = {}


		self.__make_gui()
		# self.update_node()
		# self.model = QStandardItemModel()
		# self.model.setHorizontalHeaderLabels(['name'])
		# self.setModel(self.model)
		# self.setUniformRowHeights(True)
		# # self.setHeaderHidden(True)
		# self.setFixedWidth(300)

		# self.tree = get_tree()

		# events.on("update_tree", self.__update_tree)


	def __make_gui(self):

		


		for index, name in enumerate(self.items):
			self.main_layout.addWidget(QLabel(name), index, 0)
			label = QLabel()
			self.main_layout.addWidget(label, index, 1)

			self.labels[name] = label







	def update_node(self, node_id):
		node = self.tree.get_node_id(node_id)
		
		for i in self.items:

			value = getattr(node, i)

			label = self.labels[i]
			label.setText(str(value))




	