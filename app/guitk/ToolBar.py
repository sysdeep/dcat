#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter

from .utils import qicon

class ToolBar(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(ToolBar, self).__init__(parent, *args, **kwargs)

		self.cb_open_db = None

		self.icon_open = qicon("document_open.png")

		self.btn_open = tkinter.Button(self, text="open", command=self.__open_db, image=self.icon_open, relief="flat")
		# self.btn_open = ttk.Button(controls_frame, text="open", command=self.__open_db, image=self.icon_open)
		self.btn_open.pack(side="left")

	def __open_db(self):
		self.cb_open_db()


