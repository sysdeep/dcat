#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk
from tkinter import filedialog


from ..utils import aqicon

class Styles(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(Styles, self).__init__(master, *args, **kwargs)
		self.title("Стили")

		self.maxsize(400, 300)
		self.minsize(400, 300)




		self.main_frame = tkinter.Frame(self,)
		self.main_frame.pack(expand=True, fill="both", side="top", padx=10, pady=20)



		style = ttk.Style()
		# self.tk.eval("source themes/pkgIndex.tcl")
		# self.tk.call("package", "require", "ttkthemes")
		# print(style.theme_names())
		# print(style.theme_use())
		# style.theme_use("clam")
		# style.configure('TButton', foreground='green')
		
		styles = style.theme_names()
		current_style = style.theme_use()
		self.style_box = ttk.Combobox(self.main_frame, values=styles, state='readonly')
		self.style_box.pack(side="left")
		self.style_box.bind('<<ComboboxSelected>>', self.__update_style)
		self.style_box.set(current_style)


		

		controls_frame = tkinter.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		self.icon_close = aqicon("close")
		# ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")
		tkinter.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())


	def __update_style(self, e):
		new_style = self.style_box.get()


		style = ttk.Style()
		style.theme_use(new_style)

	# def destroy(self):
	# 	tkinter.Toplevel.destroy(self)


if __name__ == "__main__":


	root = tkinter.Tk()

	modal = About(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()