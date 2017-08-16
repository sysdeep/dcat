#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from app.logic import get_tree
from app.rc import get_icon_path
from . import events, qicon


class TreeStat(QWidget):
	def __init__(self, parent=None):
		super(TreeStat, self).__init__(parent)

		self.tree = get_tree()

		self.main_layout = QGridLayout(self)

		self.__make_gui()
		self.update_stat()
		# self.model = QStandardItemModel()
		# self.model.setHorizontalHeaderLabels(['name'])
		# self.setModel(self.model)
		# self.setUniformRowHeights(True)
		# # self.setHeaderHidden(True)
		# self.setFixedWidth(300)

		# self.tree = get_tree()

		# events.on("update_tree", self.__update_tree)


	def __make_gui(self):

		self.main_layout.addWidget(QLabel("items:"), 0, 0)
		self.label_items = QLabel()
		self.main_layout.addWidget(self.label_items, 0, 1)

		self.main_layout.addWidget(QLabel("dirs:"), 1, 0)
		self.label_dirs = QLabel()
		self.main_layout.addWidget(self.label_dirs, 1, 1)

		self.main_layout.addWidget(QLabel("files:"), 2, 0)
		self.label_files = QLabel()
		self.main_layout.addWidget(self.label_files, 2, 1)

	def update_stat(self):
		nodes = self.tree.get_nodes()
		
		self.label_items.setText(str(len(nodes)))


		dirs = [item for item in nodes.values() if item.ntype == "d"]
		files = [item for item in nodes.values() if item.ntype == "f"]

		self.label_dirs.setText(str(len(dirs)))
		self.label_files.setText(str(len(files)))
		


	