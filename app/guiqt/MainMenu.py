#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	Главное меню

"""

from PyQt5.QtWidgets import QAction, QShortcut, QMenu, QMenuBar
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSignal

from . import icons

class MainMenu(QMenuBar):
	
	s_opendb = pyqtSignal()
	s_createdb = pyqtSignal()

	def __init__(self, parent=None):
		super(MainMenu, self).__init__(parent)
		


		#--- File
		file_menu = self.addMenu("Файл")
		
		file_menu.addAction(icons.get_icon(icons.I_OPEN_FILE), "Открыть", lambda: self.s_opendb.emit())
		file_menu.addAction(icons.get_icon(icons.I_CREATE_FILE), "Создать", lambda: self.s_createdb.emit())

		

		# action_open = QAction("Открыть", self.main_window)
		# action_open.setIcon(icons.get_icon(icons.I_OPEN_FILE))
		# file_menu.addAction(action_open)

		# action_create = QAction("Создать", self.main_window)
		# action_create.setIcon(icons.get_icon(icons.I_CREATE_FILE))
		# file_menu.addAction(action_create)

		# action_backup = QAction("BackUp", self.main_window)
		# action_backup.setIcon(icons.get_icon(icons.I_SAVE_AS))
		# file_menu.addAction(action_backup)

		# file_menu.addSeparator()

		# action_add_volume = QAction("Добавить том", self.main_window)
		# action_add_volume.setIcon(icons.get_icon(icons.I_ADD_ITEM))
		# file_menu.addAction(action_add_volume)

		# file_menu.addSeparator()

		# action_exit = QAction("Выход", self.main_window)
		# action_exit.setIcon(icons.get_icon(icons.I_EXIT))
		# action_exit.triggered.connect(self.main_window.act_exit)
		# action_exit.setShortcut("Ctrl+q")
		# file_menu.addAction(action_exit)


		# #--- control center
		# # control_center_action = QAction("Центр настроек", self.parent)
		# # control_center_action.triggered.connect(lambda: lbus.emit(lbus.SHOW_CONTROL_CENTER))
		# # control_center_action.setIcon(qficon("lock.png"))
		# # control_center_action.setShortcut("Ctrl+1")
		# # control_center_action.setWhatsThis("Цент настроек позволяет настроить параметры оборудования")
		# # file_menu.addAction(control_center_action)

		# # --- Settings
		# settings_menu = self.menu.addMenu("Настройки")

		# action_settings = QAction("Настройки", self.main_window)
		# settings_menu.addAction(action_settings)

		# # --- help
		# help_menu = self.menu.addMenu("Помощь")

		# action_about = QAction("О программе", self.main_window)
		# help_menu.addAction(action_about)