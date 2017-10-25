#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path

from tkinter import *

from tkinter.filedialog import *
from .modals.About import About
from .utils.icons import qicon, aqicon
from app.lib import dbus
# from lib.ee import main_ee
# from .widgets.IOTestDialog import IOTestDialog
# from .widgets.IOTableDialog import IOTableDialog

# from .modals.units_feeder import UnitsFeederModal
# from .modals.units_belt_v import UnitsBeltVModal
# from .modals.units_belt_h import UnitsBeltHModal
# from .modals.units_system import UnitsSystemModal
# from .modals.units_upost import UnitsUpostModal
# from .modals.units_bunkers import UnitsBunkersModal

# from .modals.system_cmd import SystemCMDModal

class BarMenu():
	"""
	BarMain widget
	"""
	def __init__(self, parent):
		self.parent = parent
		self.menu = None


		#--- callbacks
		self.cb_show_create = None
		self.cb_show_open = None
		self.cb_open_last = None
		self.cb_show_add_volume = None
		self.cb_create_db_backup = None



		#--- key bindings
		self.parent.bind_all("<Control-q>", lambda e: self.__c_exit())



		self.icon_open 			= qicon("document_open.png")
		self.icon_create 		= qicon("document_new.png")
		self.icon_add_volume 	= qicon("edit_add.png")
		self.icon_exit			= aqicon("close")
		self.icon_back_up		= qicon("document_save_as.png")
		self.icon_last			= qicon("bookmark.png")

		self.makeMenu()



		
	def makeMenu(self):
		self.menu = Menu(self.parent, relief="flat")
		self.parent.config(menu=self.menu)

		self.last_menu = Menu(self.menu, tearoff=0)

		file_menu = Menu(self.menu, tearoff=0)
		# self.menu.add_cascade(label="Файл", menu=file_menu, accelerator="Ctrl+f")
		self.menu.add_cascade(label="Файл", menu=file_menu)
		file_menu.add_command(label="Открыть", command=self.__show_open_db, image=self.icon_open, compound="left")
		file_menu.add_command(label="Создать", command=self.__show_create_db, image=self.icon_create, compound="left")
		file_menu.add_command(label="BackUp", command=self.__create_db_backup, image=self.icon_back_up, compound="left")
		file_menu.add_separator()
		file_menu.add_command(label="Добавить том", command=self.__show_add_volume, image=self.icon_add_volume, compound="left")
		file_menu.add_separator()
		file_menu.add_cascade(label="Last", menu=self.last_menu, image=self.icon_last, compound="left")
		file_menu.add_separator()
		file_menu.add_command(label="Выход", command=self.__c_exit, compound="left", accelerator="Ctrl+q", image=self.icon_exit)


		settings_menu = Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Настройки", menu=settings_menu)
		settings_menu.add_command(label="Стиль", command=self.__show_style)


		help_menu = Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Помощь", menu=help_menu)

		help_menu.add_command(label="О программе", command=self.__show_about)




	def add_last_files(self, last_array):
		for item in last_array:
			self.last_menu.add_command(label=item, command=lambda x=item: self.__open_last(x))




	def __open_last(self, item):
		if self.cb_open_last:
			self.cb_open_last(item)



	def __show_create_db(self):
		if self.cb_show_create:
			self.cb_show_create()


	def __show_open_db(self):
		if self.cb_show_open:
			self.cb_show_open()


	def __create_db_backup(self):
		if self.cb_create_db_backup:
			self.cb_create_db_backup()
		


	def __show_add_volume(self):
		if self.cb_show_add_volume:
			self.cb_show_add_volume()




	def __show_about(self):
		About(self.parent)



	def __c_exit(self):
		print("exit")
		self.parent.quit()
		# main_ee.emit("exit")



	def __show_style(self):
		dbus.emit(dbus.SHOW_STYLES)