#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path

from tkinter import *
from tkinter.filedialog import *
from .modals.About import About
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


		#--- key bindings
		self.parent.bind_all("<Control-q>", lambda e: self.__c_exit())


		self.makeMenu()



		
	def makeMenu(self):
		self.menu = Menu(self.parent, relief="flat")
		self.parent.config(menu=self.menu)

		self.last_menu = Menu(self.menu, tearoff=0)

		file_menu = Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="File", menu=file_menu)
		file_menu.add_command(label="Open", command=self.__show_open_db)
		file_menu.add_command(label="Create", command=self.__show_create_db)
		file_menu.add_separator()
		file_menu.add_command(label="Add volume", command=self.__show_add_volume)
		file_menu.add_separator()
		file_menu.add_cascade(label="Last", menu=self.last_menu)
		file_menu.add_separator()
		file_menu.add_command(label="Exit", command=self.__c_exit, compound="left", accelerator="Ctrl+q")


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


	def __show_add_volume(self):
		if self.cb_show_add_volume:
			self.cb_show_add_volume()




	def __show_about(self):
		About(self.parent)



	def __c_exit(self):
		print("exit")
		self.parent.quit()
		# main_ee.emit("exit")
