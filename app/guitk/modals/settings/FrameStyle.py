#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk, font



class FrameStyle(ttk.Frame):
	def __init__(self, master, *args, **kwargs):
		super(FrameStyle, self).__init__(master, *args, **kwargs)

		self.config(padding=10)

		style = ttk.Style()
		# self.tk.eval("source themes/pkgIndex.tcl")
		# self.tk.call("package", "require", "ttkthemes")
		# print(style.theme_names())
		# print(style.theme_use())
		# style.theme_use("clam")
		# style.configure('TButton', foreground='green')

		styles = style.theme_names()
		current_style = style.theme_use()
		self.style_box = ttk.Combobox(self, values=styles, state='readonly')
		self.style_box.pack(side="left")
		self.style_box.bind('<<ComboboxSelected>>', self.__update_style)
		self.style_box.set(current_style)



		# self.font_box = ttk.Combobox(self, state='readonly')
		# self.font_box.bind('<<ComboboxSelected>>', self.__update_font)
		# self.font_box.pack(side="left")

		self.__load()




	def __load(self):
		pass
		# fonts = font.families()
		# # print(fonts)
		# self.font_box.config(values = fonts)


	# def __update_font(self, e):
	# 	font_name = self.font_box.get()
	#
	# 	print(font_name)
	#
	# 	style = ttk.Style()
	# 	style.configure(".", font=(font_name, 10))
	#
	# 	# tkinter.Tk.option_add("*Font", (font_name, 12))
	# 	# tkinter.Tk.config("*Font", (font_name, 12))




	def __update_style(self, e):
		new_style = self.style_box.get()


		style = ttk.Style()
		style.theme_use(new_style)


	def apply(self):
		pass