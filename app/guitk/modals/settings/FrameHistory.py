#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
{
    "version": "0.1",
    "lastbases": [
        "/home/nia/Development/_Python/_DCat/reanimator.dcat",
        "/home/nia/Development/_Python/_DCat/3.dcat",
        "/home/nia/Development/_Python/_DCat/2.dcat",
        "/home/nia/Development/_Python/_DCat/1.dcat"
    ],
    "open_last": 1
}
"""

import tkinter
from tkinter import ttk



class FrameHistory(ttk.Frame):
	def __init__(self, master, usettings, *args, **kwargs):
		super(FrameHistory, self).__init__(master, *args, **kwargs)

		self.config(padding=10)

		self.usettings = usettings


		self.autoload_flag = 0


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


		ttk.Button(controls_frame, text="Очистить историю", command=self.__clear_history).pack(side="right")



		self.__load()


	def __load(self):
		self.autoload_flag = self.usettings.is_open_last
		self.var_autoloading.set(self.autoload_flag)



	def __clear_history(self):
		self.usettings.clear_lastbases()



	def apply(self):
		autoload_flag = self.var_autoloading.get()


		if autoload_flag != self.autoload_flag:
			self.usettings.is_open_last = autoload_flag