#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from .Tree import Tree

class MainFrame(QWidget):
	def __init__(self, parent=None):
		super(MainFrame, self).__init__(parent)

		self.main_layout = QHBoxLayout()
		self.setLayout(self.main_layout)

		# label = QLabel("Tree")
		# self.main_layout.addWidget(label)
		self.tree_view = Tree()
		self.main_layout.addWidget(self.tree_view)

		self.main_layout.addStretch()



	def update_tree(self):
		self.tree_view.update_tree()

