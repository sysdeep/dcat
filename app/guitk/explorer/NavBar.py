#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter


class NavBar(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(NavBar, self).__init__(parent, *args, **kwargs)


		self.cb_go = None
		self.cb_back = None
		self.cb_root = None

		
		controls_frame = tkinter.Frame(self)
		controls_frame.pack(fill="both", side="left", padx=10, pady=10)

		label = tkinter.Label(controls_frame, text="stack")
		label.pack(side="left")

		btn_back = tkinter.Button(controls_frame, text="back", command=self.__go_back)
		btn_back.pack(side="left")


		self.stack_frame = tkinter.Frame(self)
		self.stack_frame.pack(fill="both", side="left", padx=10, pady=10)



	def update_history(self, items):
		
		self.__clear_stack()

		btn = tkinter.Button(self.stack_frame, text="root", command=self.__go_root )
		btn.pack(side="left")

		inames = [item.name for item in items]
		for i, iname in enumerate(inames):
			btn = tkinter.Button(self.stack_frame, text=iname, command=lambda x=i: self.__go(x), compound="left" )
			btn.pack(side="left")
		


	def __clear_stack(self):
		for widget in self.stack_frame.winfo_children():
			widget.destroy()


	def __go(self, x):
		if self.cb_go:
			self.cb_go(x)


	def __go_back(self):
		if self.cb_back:
			self.cb_back()

	def __go_root(self):
		if self.cb_root:
			self.cb_root()


	def set_cb_go(self, cb):
		self.cb_go = cb

	def set_cb_back(self, cb):
		self.cb_back = cb


	def set_cb_root(self, cb):
		self.cb_root = cb

	













class StackFrame(tkinter.Frame):
	def __init__(self, parent, *args, **kwargs):
		super(StackFrame, self).__init__(parent, *args, **kwargs)

		self.cb_root = None

	def set_items(self, items):
		"""
			Args:
				items	[list]	: ["root", "foo", ...]
		"""
		self.__clear()

		btn = tkinter.Button(self, text="root", command=self.__go_root )
		btn.pack()

		for i, iname in enumerate(items):
			btn = tkinter.Button(self, text=iname, command=lambda x=i: self.__act_go(x), compound="left" )
			btn.pack(side="left")

			# btn2 = tkinter.Button(self, text=iname, command=lambda x=i: self.__act_go(x) )
			# btn2.pack()



		# #--- controls
		# tkinter.Frame(self, relief="raised", bd=2, height=2).pack(fill="x", padx=5, pady=5)
		# controls_frame = tkinter.Frame(self)
		# controls_frame.pack(fill="both", side="bottom", padx=10, pady=10)
		# ttk.Button(controls_frame, text="Закрыть", image=get_icon("application-exit"), compound="left", command=self.destroy).pack(side="right")


	def __clear(self):
		for widget in self.winfo_children():
			widget.destroy()


	def __act_go(self, index):
		pass

	def __go_root(self):
		if self.cb_root:
			self.cb_root()