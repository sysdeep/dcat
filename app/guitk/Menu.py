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


		self.cb_create = None
		self.cb_open = None
		self.cb_open_modal_add_volume = None


		#--- key bindings
		self.parent.bind_all("<Control-q>", lambda e: self.__c_exit())


		self.makeMenu()



		
	def makeMenu(self):
		self.menu = Menu(self.parent, relief="flat")
		self.parent.config(menu=self.menu)

		self.last_menu = Menu(self.menu, tearoff=0)

		file_menu = Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="File", menu=file_menu)
		file_menu.add_command(label="Open", command=self.c_open_db)
		file_menu.add_command(label="Create", command=self.c_create_db)
		file_menu.add_separator()
		file_menu.add_command(label="Add volume", command=self.c_add_volume)
		file_menu.add_separator()
		file_menu.add_cascade(label="Last", menu=self.last_menu)
		file_menu.add_separator()
		file_menu.add_command(label="Exit", command=self.__c_exit, compound="left", accelerator="Ctrl+q")


		help_menu = Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="Помощь", menu=help_menu)

		help_menu.add_command(label="О программе", command=self.c_show_about)




	def add_last_files(self, last_array):
		for item in last_array:
			self.last_menu.add_command(label=item, command=lambda x=item: self.c_open_last(x))




	def c_open_last(self, item):
		if self.cb_open:
			self.cb_open(item)



	def __c_exit(self):
		print("exit")
		self.parent.quit()
		# main_ee.emit("exit")

	def c_about(self):
		win = Toplevel()
		lab = Label(win, text="Это просто программа-тест \n меню в Tkinter")
		lab.pack()


	def c_create_db(self):
		title = 'Choose the output directory'
		op = asksaveasfilename(defaultextension=".dcat", title=title)
		if op and self.cb_create:
			self.cb_create(op)




	def c_open_db(self):
		if self.cb_open:
			self.cb_open()


	def c_add_volume(self):
		if self.cb_open_modal_add_volume:
			self.cb_open_modal_add_volume()




	def c_show_about(self):
		modal = About(self.parent)


	def set_cb_create(self, cb):
		self.cb_create = cb

	def set_cb_show_open_db(self, cb):
		self.cb_open = cb

	def set_cb_open_modal_add_volume(self, cb):
		self.cb_open_modal_add_volume = cb
	
