#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.lib import dbus
from .utils import ticons

class ToolBar(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(ToolBar, self).__init__(parent, *args, **kwargs)

		self.cb_open_db = None
		self.cb_create_db = None
		self.cb_create_db_backup = None




		self.btn_open = tkinter.Button(self, text="Открыть", command=self.__open_db, image=ticons.ticon(ticons.I_OPEN_FILE), relief="flat", compound="left")
		self.btn_open.pack(side="left")

		self.btn_new = tkinter.Button(self, text="Создать", command=self.__create_db, image=ticons.ticon(ticons.I_CREATE_FILE), relief="flat", compound="left")
		self.btn_new.pack(side="left")

		btn_add_volume = tkinter.Button(self, text="Добавить том", command=self.__show_add_volume, image=ticons.ticon(ticons.I_ADD_ITEM), relief="flat", compound="left")
		btn_add_volume.pack(side="left")

		self.btn_backup = tkinter.Button(self, text="BackUP", command=self.__create_db_backup, image=ticons.ticon(ticons.I_SAVE_AS), relief="flat", compound="left")
		self.btn_backup.pack(side="left")

		btn_find = tkinter.Button(self, text="Поиск", command=self.__show_find_modal, image=ticons.ticon(ticons.I_FIND), relief="flat", compound="left")
		btn_find.pack(side="left")

	def __open_db(self):
		self.cb_open_db()


	def __create_db(self):
		self.cb_create_db()

	def __create_db_backup(self):
		if self.cb_create_db_backup:
			self.cb_create_db_backup()


	def __show_find_modal(self):
		self.cb_show_find_modal()


	def __show_add_volume(self):
		dbus.emit(dbus.SHOW_ADD_VOLUME)