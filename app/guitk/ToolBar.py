#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter

from .utils import qicon

class ToolBar(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(ToolBar, self).__init__(parent, *args, **kwargs)

		self.cb_open_db = None
		self.cb_create_db = None
		self.cb_create_db_backup = None


		self.icon_open 			= qicon("document_open.png")
		self.icon_create 		= qicon("document_new.png")
		self.icon_back_up		= qicon("document_save_as.png")
		self.icon_find			= qicon("find.png")

		self.btn_open = tkinter.Button(self, text="Открыть", command=self.__open_db, image=self.icon_open, relief="flat", compound="left")
		self.btn_open.pack(side="left")

		self.btn_new = tkinter.Button(self, text="Создать", command=self.__create_db, image=self.icon_create, relief="flat", compound="left")
		self.btn_new.pack(side="left")

		self.btn_backup = tkinter.Button(self, text="BackUP", command=self.__create_db_backup, image=self.icon_back_up, relief="flat", compound="left")
		self.btn_backup.pack(side="left")

		btn_find = tkinter.Button(self, text="Поиск", command=self.__show_find_modal, image=self.icon_find, relief="flat", compound="left")
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