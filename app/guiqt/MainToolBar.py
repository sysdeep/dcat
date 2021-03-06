#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Главное меню

"""

from PyQt5.QtWidgets import QAction, QShortcut, QMenu, QToolBar
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSignal

from . import icons

class MainToolBar(QToolBar):

	s_opendb = pyqtSignal()
	s_createdb = pyqtSignal()
	s_addvolume = pyqtSignal()


	def __init__(self, parent=None):
		super(MainToolBar, self).__init__(parent)

		self.addAction(icons.get_icon(icons.I_OPEN_FILE), "Открыть", lambda: self.s_opendb.emit())
		self.addAction(icons.get_icon(icons.I_CREATE_FILE), "Создать", lambda: self.s_createdb.emit())
		self.addAction(icons.get_icon(icons.I_ADD_ITEM), "Добавить том", lambda: self.s_addvolume.emit())


		# action_create = QAction("Создать", self.main_window)
		# file_toolbar.addAction(action_create)

		# action_backup = QAction("BackUp", self.main_window)
		# file_toolbar.addAction(action_backup)

		# file_toolbar.addSeparator()

		# action_add_volume = QAction("Добавить том", self.main_window)
		# file_toolbar.addAction(action_add_volume)

		# file_toolbar.addSeparator()

		# action_exit = QAction("Выход", self.main_window)
		# file_toolbar.addAction(action_exit)

		#
		# #--- control center
		# # control_center_action = QAction("Центр настроек", self.parent)
		# # control_center_action.triggered.connect(lambda: lbus.emit(lbus.SHOW_CONTROL_CENTER))
		# # control_center_action.setIcon(qficon("lock.png"))
		# # control_center_action.setShortcut("Ctrl+1")
		# # control_center_action.setWhatsThis("Цент настроек позволяет настроить параметры оборудования")
		# # file_menu.addAction(control_center_action)
		#
		# # --- Settings
		# settings_menu = self.menu.addMenu("Настройки")
		#
		# action_settings = QAction("Настройки", self.main_window)
		# settings_menu.addAction(action_settings)
		#
		# # --- help
		# help_menu = self.menu.addMenu("Помощь")
		#
		# action_about = QAction("О программе", self.main_window)
		# help_menu.addAction(action_about)

