#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QAction, QFileDialog
# from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem

# from app.rc import get_icon_path

from . import events, qicon
from .ModalScan import ModalScan

# from .icons import qicon
# from app.logic import get_project

# from .modals import show_modal_once, Settings, ControlCenter, ObjectsEmu, About, ProjectPackages
# from .modals.FaenzaIcons import FaenzaIcons
# from .modals.Users import Users
# from .modals.CalibrationFlags import CalibrationFlags


# from .modals.console import PyConsoleModal


class BarMenu(object):
	def __init__(self, parent):
		self.parent 	= parent
		# self.project 	= get_project()


		menu = self.parent.menuBar()
		toolbar = self.parent.addToolBar("Main")

		#--- file -------------------------------------------------------------
		file_menu = menu.addMenu("Файл")


		file_open_action = QAction("Open", self.parent)
		file_open_action.setIcon(qicon("document_open.png"))
		file_open_action.triggered.connect(lambda: self.__file_open())

		file_menu.addAction(file_open_action)
		toolbar.addAction(file_open_action)



		file_create_action = QAction("New catalog", self.parent)
		file_create_action.setIcon(qicon("document_new.png"))
		file_create_action.triggered.connect(lambda: self.__file_create())

		file_menu.addAction(file_create_action)
		toolbar.addAction(file_create_action)

		# file_open_dir_action = QAction("Open dir", self.parent)
		# file_open_dir_action.triggered.connect(lambda: self.__file_open_dir())
		# file_menu.addAction(file_open_dir_action)
		#
		# file_scan_action = QAction("Scan", self.parent)
		# file_scan_action.triggered.connect(self.__file_scan)
		# file_menu.addAction(file_scan_action)

		file_save_action = QAction("Save", self.parent)
		file_save_action.setIcon(qicon("document_save.png"))
		file_save_action.triggered.connect(lambda: self.__file_save())
		file_menu.addAction(file_save_action)



	# def __file_open_dir(self):
	# 	# print("file_open")
	# 	dlg = QFileDialog()
	# 	# dlg.setAcceptMode(QFileDialog.AcceptOpen)
	# 	dlg.setFileMode(QFileDialog.Directory)
	# 	dlg.setOption(QFileDialog.ShowDirsOnly, True)
	#
	#
	# 	if dlg.exec_():
	# 		files = dlg.selectedFiles()
	# 		print(files)
	# 		if len(files) > 0:
	# 			# set_scan_dir(files[0])
	# 			events.set_scan_path(files[0])
	#
	#
	# def __file_scan(self):
	# 	print("scan")
	# 	events.start_scan()



	def __file_save(self):
		# print("file_open")
		dlg = QFileDialog()
		dlg.setAcceptMode(QFileDialog.AcceptSave)
		# dlg.setFileMode(QFileDialog.Directory)
		# dlg.setOption(QFileDialog.ShowDirsOnly, True)


		if dlg.exec_():
			files = dlg.selectedFiles()
			print(files)
			if len(files) > 0:
			# 	# set_scan_dir(files[0])
				events.set_save_file(files[0])




	def __file_open(self):
		dlg = QFileDialog()
		dlg.setAcceptMode(QFileDialog.AcceptOpen)
		# dlg.setFileMode(QFileDialog.Directory)
		# dlg.setOption(QFileDialog.ShowDirsOnly, True)


		if dlg.exec_():
			files = dlg.selectedFiles()
			print(files)
			if len(files) > 0:
			# 	# set_scan_dir(files[0])
				events.set_open_file(files[0])

	def __file_create(self):
		modal = ModalScan(self.parent)
		modal.show()

		# name = QFileDialog.getOpenFileName(self.parent, 'open dir')
		# with open(name[0], "w", encoding='utf-8') as fd:
		# 	fd.write(json_data)
		# 	fd.close()

		#
		# #--- control center
		# control_center_action = QAction("Центр настроек", self.parent)
		# control_center_action.triggered.connect(lambda: ControlCenter(self.parent).show())
		# control_center_action.setIcon(qicon("lock"))
		# control_center_action.setShortcut("Ctrl+1")
		# file_menu.addAction(control_center_action)

	# 	#--- settings
	# 	settings_action = QAction("Настройка конфигурации", self.parent)
	# 	settings_action.triggered.connect(lambda: Settings(self.parent).show())
	# 	settings_action.setIcon(qicon("window-new"))
	# 	file_menu.addAction(settings_action)
	#
	#
	# 	#--- users
	# 	users_action = QAction("Пользователи", self.parent)
	# 	users_action.triggered.connect(lambda: Users(self.parent).show())
	# 	users_action.setIcon(qicon("podcast-new"))
	# 	file_menu.addAction(users_action)
	#
	#
	# 	file_menu.addSeparator()
	#
	# 	#--- logout
	# 	logout_action = QAction("Выход", self.parent)
	# 	logout_action.triggered.connect(self.parent.logout)
	# 	logout_action.setIcon(qicon("object-rotate-left"))
	# 	logout_action.setToolTip("Сменить пользователя")
	# 	file_menu.addAction(logout_action)
	#
	#
	# 	#--- exit
	# 	exit_action = QAction("&Закрыть", self.parent)
	# 	exit_action.setShortcut("Ctrl+Q")
	# 	exit_action.setStatusTip("Закрыть приложение")
	# 	exit_action.setIcon(qicon("system-shutdown-restart-panel"))
	# 	exit_action.triggered.connect(self.parent.exit)
	# 	file_menu.addAction(exit_action)
	#
	#
	#
	# 	#--- system -----------------------------------------------------------
	# 	system_menu = menu.addMenu("Система")
	#
	# 	#--- log
	# 	system_menu_ulog = QAction("Журнал", self.parent)
	# 	# system_menu_ulog.triggered.connect(lambda: ULog(self.parent).show())
	# 	system_menu_ulog.triggered.connect(lambda: show_modal_once("ulog", self.parent))
	# 	system_menu_ulog.setIcon(qicon("image-bmp"))
	# 	system_menu.addAction(system_menu_ulog)
	#
	# 	#--- calibration line 1
	# 	system_menu_test_flags_line1 = QAction("Тестирование координат флажков - линия 1", self.parent)
	# 	system_menu_test_flags_line1.triggered.connect(self.__start_modal_test_flags_line1)
	# 	system_menu_test_flags_line1.setIcon(qicon("image-bmp"))
	# 	system_menu.addAction(system_menu_test_flags_line1)
	#
	# 	#--- calibration line 2
	# 	system_menu_test_flags_line2 = QAction("Тестирование координат флажков - линия 2", self.parent)
	# 	system_menu_test_flags_line2.triggered.connect(self.__start_modal_test_flags_line2)
	# 	system_menu_test_flags_line2.setIcon(qicon("image-bmp"))
	# 	system_menu.addAction(system_menu_test_flags_line2)
	#
	#
	#
	# 	#--- debug ------------------------------------------------------------
	# 	debug_menu = menu.addMenu("Debug")
	#
	# 	#--- objects info
	# 	debug_objects_info = QAction("ObjectsInfo", self.parent)
	# 	debug_objects_info.triggered.connect(lambda: show_modal_once("objects_info", self.parent))
	# 	debug_menu.addAction(debug_objects_info)
	#
	# 	#--- project packages
	# 	debug_project_packages = QAction("Project packages", self.parent)
	# 	debug_project_packages.triggered.connect(lambda: ProjectPackages(self.parent).show())
	# 	debug_menu.addAction(debug_project_packages)
	#
	# 	#--- objects emu
	# 	debug_objects_emu = QAction("ObjectsEmu", self.parent)
	# 	debug_objects_emu.triggered.connect(lambda: ObjectsEmu(self.parent).show())
	# 	debug_menu.addAction(debug_objects_emu)
	#
	# 	debug_menu.addSeparator()
	#
	# 	#--- faenza icons
	# 	debug_faenza = QAction("Иконки Faenza", self.parent)
	# 	debug_faenza.triggered.connect(lambda: FaenzaIcons(self.parent).show())
	# 	debug_menu.addAction(debug_faenza)
	#
	#
	#
	# 	debug_ii = QAction("Console", self.parent)
	# 	debug_ii.setShortcut("Ctrl+`")
	# 	debug_ii.setIcon(qicon("system-lock-screen"))
	# 	debug_ii.setStatusTip("Открыть окно консоли")
	# 	debug_ii.triggered.connect(lambda: PyConsoleModal(self.parent).show())
	# 	debug_menu.addAction(debug_ii)
	#
	#
	# 	#--- Help -------------------------------------------------------------
	# 	help_menu = menu.addMenu("Справка")
	#
	# 	#--- about
	# 	help_menu_about = QAction("О программе", self.parent)
	# 	help_menu_about.setIcon(qicon("help-about"))
	# 	help_menu_about.triggered.connect(lambda: About(self.parent).show())
	# 	help_menu.addAction(help_menu_about)
	#
	#
	#
	#
	# def __start_modal_test_flags_line1(self):
	# 	line_model = self.project.get_node("line1")
	# 	modal = CalibrationFlags(line_model=line_model, parent=self.parent)
	# 	modal.show()
	#
	# def __start_modal_test_flags_line2(self):
	# 	line_model = self.project.get_node("line2")
	# 	modal = CalibrationFlags(line_model=line_model, parent=self.parent)
	# 	modal.show()