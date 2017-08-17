#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter


class StackFrame(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(StackFrame, self).__init__(parent, *args, **kwargs)


		self.cb = None

		label = tkinter.Label(self, text="stack")
		label.pack()


	def update_items(self, items):


		for widget in self.winfo_children():
			widget.destroy()


		for i, item in enumerate(items):
			iname = item.name
			btn = tkinter.Button(self, text=iname, command=lambda x=i: self.__act_go(x) )
			btn.pack()



	def __act_go(self, x):
		print(x)

		if self.cb:
			self.cb(x)


	def on_change(self, callback):
		self.cb = callback
