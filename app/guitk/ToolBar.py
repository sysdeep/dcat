#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app import log
from app.lib import dbus
from .utils import ticons

class ToolBar(ttk.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(ToolBar, self).__init__(parent, *args, **kwargs)

		self.cb_open_db = None
		self.cb_create_db = None
		self.cb_create_db_backup = None
		self.cb_show_find_modal = None


		self.buttons = (
			ToolBarButton(self, text="Открыть", image=ticons.ticon(ticons.I_OPEN_FILE), compound="left", command=self.__open_db),
			ToolBarButton(self, text="Создать", command=self.__create_db, image=ticons.ticon(ticons.I_CREATE_FILE), compound="left"),
			ToolBarButton(self, text="Добавить том", command=self.__show_add_volume, image=ticons.ticon(ticons.I_ADD_ITEM), compound="left"),
			ToolBarButton(self, text="Импортировать том", command=self.__show_import_volume, image=ticons.ticon(ticons.I_IMPORT), compound="left"),
			ToolBarButton(self, text="BackUP", command=self.__create_db_backup, image=ticons.ticon(ticons.I_SAVE_AS), compound="left"),
			ToolBarButton(self, text="Поиск", command=self.__show_find_modal, image=ticons.ticon(ticons.I_FIND), compound="left"),
		)




		for btn in self.buttons:
			btn.pack(side="left", ipadx=10, ipady=10)



		# # self.btn_open = tkinter.Button(self, text="Открыть", command=self.__open_db, image=ticons.ticon(ticons.I_OPEN_FILE), relief="flat", compound="left")
		# # self.btn_open = ttk.Button(self, text="Открыть", command=self.__open_db, image=ticons.ticon(ticons.I_OPEN_FILE), compound="left")
		# self.btn_open = ttk.Button(self, command=self.__open_db, image=ticons.ticon(ticons.I_OPEN_FILE), compound="left")
		# self.btn_open.pack(side="left")

		# self.btn_new = tkinter.Button(self, text="Создать", command=self.__create_db, image=ticons.ticon(ticons.I_CREATE_FILE), relief="flat", compound="left")
		# self.btn_new = ttk.Button(self, text="Создать", command=self.__create_db, image=ticons.ticon(ticons.I_CREATE_FILE), compound="left")
		# self.btn_new.pack(side="left")

		# btn_add_volume = tkinter.Button(self, text="Добавить том", command=self.__show_add_volume, image=ticons.ticon(ticons.I_ADD_ITEM), relief="flat", compound="left")
		# btn_add_volume = ttk.Button(self, text="Добавить том", command=self.__show_add_volume, image=ticons.ticon(ticons.I_ADD_ITEM), compound="left")
		# btn_add_volume.pack(side="left")

		# btn_import_volume = tkinter.Button(self, text="Импортировать том", command=self.__show_import_volume, image=ticons.ticon(ticons.I_IMPORT), relief="flat", compound="left")
		# btn_import_volume = ttk.Button(self, text="Импортировать том", command=self.__show_import_volume, image=ticons.ticon(ticons.I_IMPORT), compound="left")
		# btn_import_volume.pack(side="left")
		#
		# # self.btn_backup = tkinter.Button(self, text="BackUP", command=self.__create_db_backup, image=ticons.ticon(ticons.I_SAVE_AS), relief="flat", compound="left")
		# self.btn_backup = ttk.Button(self, text="BackUP", command=self.__create_db_backup, image=ticons.ticon(ticons.I_SAVE_AS), compound="left")
		# self.btn_backup.pack(side="left")
		#
		# # btn_find = tkinter.Button(self, text="Поиск", command=self.__show_find_modal, image=ticons.ticon(ticons.I_FIND), relief="flat", compound="left")
		# btn_find = ttk.Button(self, text="Поиск", command=self.__show_find_modal, image=ticons.ticon(ticons.I_FIND), compound="left")
		# btn_find.pack(side="left")



		



	def __open_db(self):
		self.cb_open_db()


	def __create_db(self):
		self.cb_create_db()

	def __create_db_backup(self):
		if self.cb_create_db_backup:
			self.cb_create_db_backup()


	def __show_find_modal(self):
		if self.cb_show_find_modal:
			self.cb_show_find_modal()


	def __show_add_volume(self):
		dbus.emit(dbus.SHOW_ADD_VOLUME)


	def __show_import_volume(self):
		dbus.emit(dbus.SHOW_IMPORT_VOLUME)










class ToolBarButton(ttk.Label):
	def __init__(self, master, command=None, **kwargs):
		super(ToolBarButton, self).__init__(master, **kwargs)

		self.command = command

		self.bind("<Button-1>", self.__on_click)

	def __on_click(self, event):
		if self.command:
			try:
				self.command()
			except Exception as e:
				log.exception(e)