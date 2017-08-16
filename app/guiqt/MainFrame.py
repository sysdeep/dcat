#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from .Tree import Tree
from .TreeStat import TreeStat
from .NodeStat import NodeStat

class MainFrame(QWidget):
	def __init__(self, parent=None):
		super(MainFrame, self).__init__(parent)

		self.main_layout = QHBoxLayout(self)

		# label = QLabel("Tree")
		# self.main_layout.addWidget(label)
		
		self.__make_tree_side()
		self.__make_node_side()

		


	def __make_tree_side(self):
		tree_side = QVBoxLayout()
		self.main_layout.addLayout(tree_side)
		
		self.tree_view = Tree()
		self.tree_view.select_cb = self.__on_select_node
		tree_side.addWidget(self.tree_view)

		self.tree_stat = TreeStat()
		tree_side.addWidget(self.tree_stat)


		# self.main_layout.addStretch()


	def __make_node_side(self):
		node_side = QVBoxLayout()
		self.main_layout.addLayout(node_side)

		self.node_stat = NodeStat()
		node_side.addWidget(self.node_stat)

		node_side.addStretch()



	def update_tree(self):
		self.tree_view.update_tree()
		self.tree_stat.update_stat()




	def __on_select_node(self, node_id):
		print("---->", node_id)

		self.node_stat.update_node(node_id)