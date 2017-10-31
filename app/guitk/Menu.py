#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path

from tkinter import *

from tkinter.filedialog import *
from .modals.About import About

from .utils import ticons
from app.lib import dbus


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



		self.makeMenu()



		
	def makeMenu(self):
		self.menu = Menu(self.parent, relief="flat")
		self.parent.config(menu=self.menu)

		self.last_menu = Menu(self.menu, tearoff=0)

		file_menu = Menu(self.menu, tearoff=0)
		# self.menu.add_cascade(label="Файл", menu=file_menu, accelerator="Ctrl+f")
		self.menu.add_cascade(label="Файл", menu=file_menu)
		file_menu.add_command(label="Открыть", command=self.__show_open_db, image=ticons.ticon(ticons.I_OPEN_FILE), compound="left")
		file_menu.add_command(label="Создать", command=self.__show_create_db, image=ticons.ticon(ticons.I_CREATE_FILE), compound="left")
		file_menu.add_command(label="BackUp", command=self.__create_db_backup, image=ticons.ticon(ticons.I_SAVE_AS), compound="left")
		file_menu.add_separator()
		file_menu.add_command(label="Добавить том", command=self.__show_add_volume, image=ticons.ticon(ticons.I_ADD_ITEM), compound="left")
		file_menu.add_separator()
		file_menu.add_cascade(label="Last", menu=self.last_menu, image=ticons.ticon(ticons.I_BOOKMARK), compound="left")
		file_menu.add_separator()
		file_menu.add_command(label="Выход", command=self.__c_exit, compound="left", accelerator="Ctrl+q", image=ticons.ticon(ticons.CLOSE))


		# settings_menu = Menu(self.menu, tearoff=0)
		# self.menu.add_cascade(label="Настройки", menu=settings_menu)
		# settings_menu.add_command(label="Стиль", command=self.__show_style)
		self.menu.add_command(label="Настройки", command=self.__show_settings)


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



	def __show_settings(self):
		dbus.emit(dbus.SHOW_SETTINGS)