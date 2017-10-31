#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from app.rc import ABOUT_NAME, ABOUT_AUTHOR_EMAIL, ABOUT_AUTHOR_NAME, ABOUT_DESCRIPTION, ABOUT_SLUG, VERSION
from ..utils import ticons

class About(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(About, self).__init__(master, *args, **kwargs)
		self.title("О программе")

		self.maxsize(400, 300)
		self.minsize(400, 300)




		self.main_frame = ttk.Frame(self, padding=10)
		self.main_frame.pack(expand=True, fill="both", side="top")


		ttk.Label(self.main_frame, text=ABOUT_NAME, anchor="w").pack(side="top", fill="x")
		ttk.Label(self.main_frame, text=ABOUT_SLUG, anchor="w").pack(side="top", fill="x")
		full_name = "{}({})".format(ABOUT_AUTHOR_NAME, ABOUT_AUTHOR_EMAIL)
		ttk.Label(self.main_frame, text=full_name, anchor="w").pack(side="top", fill="x")

		ttk.Label(self.main_frame, text="", anchor="w").pack(side="top", fill="x")


		self.description = tkinter.Text(self.main_frame, height=6, width=20, padx=10, pady=10)
		self.description.pack(side="top", fill="both", expand=True)
		self.description.insert(tkinter.END, ABOUT_DESCRIPTION)
		self.description.config(state=tkinter.DISABLED)
		# tkinter.Message(self.main_frame, text=ABOUT_DESCRIPTION, anchor="w", justify="center", aspect=300, width=400).pack(side="top", fill="x")

		ttk.Label(self.main_frame, text="", anchor="w").pack(side="top", fill="x")

		version_string = "Версия: {}".format(VERSION)
		ttk.Label(self.main_frame, text=version_string, anchor="w").pack(side="top", fill="x")


		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		# self.icon_close = aqicon("close")
		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=ticons.ticon(ticons.CLOSE), compound="left").pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())





		# mb = ttk.Menubutton(self.main_frame, text="test")
		# mb.pack()
		#
		# var = tkinter.IntVar()
		#
		# mb.menu = tkinter.Menu(mb, tearoff="0")
		# mb["menu"] = mb.menu
		# mb.menu.add_checkbutton(label="qqq", variable=var)












if __name__ == "__main__":


	root = tkinter.Tk()

	modal = About(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()