#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter


class NavBar(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(NavBar, self).__init__(parent, *args, **kwargs)


		self.cb = None

		label = tkinter.Label(self, text="stack")
		label.pack()

		self.stack_frame = StackFrame(self)
		self.stack_frame.pack()


	def update_history(self, items):

		inames = [item.name for item in items]
		self.stack_frame.set_items(inames)
		


	def __act_go(self, x):
		print(x)

		if self.cb:
			self.cb(x)


	def on_change(self, callback):
		self.cb = callback




class StackFrame(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(StackFrame, self).__init__(parent, *args, **kwargs)


	def set_items(self, items):
		"""
			Args:
				items	[list]	: ["root", "foo", ...]
		"""
		self.__clear()

		for i, iname in enumerate(items):
			btn = tkinter.Button(self, text=iname, command=lambda x=i: self.__act_go(x) )
			btn.pack()

			btn2 = tkinter.Button(self, text=iname, command=lambda x=i: self.__act_go(x) )
			btn2.pack()


	def __clear(self):
		for widget in self.winfo_children():
			widget.destroy()


	def __act_go(self, index):
		pass