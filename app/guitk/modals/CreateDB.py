#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter

class CreateDB(tkinter.TopLevel):
	def __init__(self, master=None, *args, **kwargs):
		super(CreateDB, self).__init__(master, *args, **kwargs)
		self.title("Центр управления")
		self.option_add("*Font", (GUI_FONT_NAME, GUI_FONT_SIZE))
		self.minsize(400, 300)
		self.item = item
		self.status = True
		self.main_frame = SFrame(self, item=self.item)
		self.main_frame.pack(fill="both", expand=True)



		controls_frame = tkinter.Frame(self)
		controls_frame.pack(fill="both", side="bottom", padx=10, pady=10)

		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", image=get_icon("application-exit"), compound="left", command=self.destroy).pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())



	def destroy(self):
		self.status = False
		tkinter.Toplevel.destroy(self)


	def set_item(self, item):
		self.main_frame.set_item(item)