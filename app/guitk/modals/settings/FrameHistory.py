#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import tkinter
from tkinter import ttk



class FrameHistory(ttk.Frame):
	def __init__(self, master, usettings, *args, **kwargs):
		super(FrameHistory, self).__init__(master, *args, **kwargs)

		self.config(padding=10)

		self.usettings = usettings





		self.var_autoloading = tkinter.IntVar()
		# self.var_autoloading.set(1)


		settings_frame = ttk.Frame(self)
		settings_frame.pack(side="top", fill="x")

		# row = 0
		# ttk.Label(settings_frame, text="Автозагрузка базы:").grid(row=row, column=0, sticky="e", pady=5, padx=5)
		# ttk.Checkbutton(settings_frame).grid(row=row, column=1)
		# ttk.Checkbutton(settings_frame, text="File", variable=self.var_autoloading).grid(row=0, column=0)

		ttk.Checkbutton(settings_frame, text="Автозагрузка базы:", variable=self.var_autoloading).pack(side="left")




		controls_frame = ttk.Frame(self)
		controls_frame.pack(side="bottom", fill="x")


		ttk.Button(controls_frame, text="Очистить историю").pack(side="right")



		self.__load()


	def __load(self):
		autoload_flag = self.usettings.is_open_last
		self.var_autoloading.set(autoload_flag)