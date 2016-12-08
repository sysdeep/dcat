#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeView, QLabel


class TreeBar(QWidget):
    def __init__(self, parent=None):
        super(TreeBar, self).__init__(parent)

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        label = QLabel("Tree")
        self.main_layout.addWidget(label)


        self.tree_view = QTreeView()
        self.main_layout.addWidget(self.tree_view)
