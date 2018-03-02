#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter 
from tkinter import ttk

from app.lib import dbus
from .utils import ticons



class DBInfo(ttk.Frame):
	def __init__(self, master, *args, **kwargs):
		super(DBInfo, self).__init__(master, *args, **kwargs)


		# self.cb_show_info = None
		self.configure(padding=5)


		# ttk.Label(self, text="version:").pack(side="left")
		#
		# self.label_version = ttk.Label(self, text="---")
		# self.label_version.pack(side="left")
		#
		# ttk.Label(self, text=" | ").pack(side="left")
		#
		# ttk.Label(self, text="path:").pack(side="left")

		self.label_path = ttk.Label(self, text="---")
		self.label_path.pack(side="left")

		# ttk.Label(self, text=" | ").pack(side="left")
		#
		# ttk.Label(self, text="created:").pack(side="left")
		#
		# self.label_created = ttk.Label(self, text="---")
		# self.label_created.pack(side="left")


		#--- close
		ttk.Button(self, text="Закрыть", image=ticons.ticon(ticons.CLOSE), compound="left", command=self.__on_exit).pack(side="right")

		#--- dbinfo
		ttk.Button(self, text="Info", image=ticons.ticon(ticons.INFO), compound="left", command=self.__show_info).pack(side="right", padx=5)

		#--- show databases
		ttk.Button(self, text="DBs", image=ticons.ticon(ticons.I_FOLDER_HOME), compound="left", command=self.__show_dbs).pack(side="right", padx=5)




	def set_path(self, value):
		self.label_path.config(text=value)


	# def set_version(self, value):
	# 	self.label_version.config(text=value)
	#
	# def set_created(self, value):
	# 	self.label_created.config(text=value)


	# def set_sysinfo(self, sqlite_rows):
	# 	for row in sqlite_rows:
	# 		if row["key"] == "version":
	# 			self.set_version(row["value"])
	# 		elif row["key"] == "created":
	# 			self.set_created(row["value"])
	# 		else:
	# 			pass








	def __on_exit(self):
		self.master.quit()


	def __show_info(self):
		dbus.emit(dbus.SHOW_ABOUT_BASE)

	def __show_dbs(self):
		dbus.emit(dbus.SHOW_DATABASES)