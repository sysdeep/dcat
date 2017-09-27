#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk
from tkinter import filedialog

from app.rc import ABOUT_NAME, ABOUT_AUTHOR_EMAIL, ABOUT_AUTHOR_NAME, ABOUT_DESCRIPTION, ABOUT_SLUG, VERSION
from ..utils import aqicon

class About(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(About, self).__init__(master, *args, **kwargs)
		self.title("О программе")

		self.maxsize(400, 300)
		self.minsize(400, 300)




		self.main_frame = tkinter.Frame(self,)
		self.main_frame.pack(expand=True, fill="both", side="top", padx=10, pady=20)


		tkinter.Label(self.main_frame, text=ABOUT_NAME, anchor="w").pack(side="top", fill="x")
		tkinter.Label(self.main_frame, text=ABOUT_SLUG, anchor="w").pack(side="top", fill="x")
		full_name = "{}({})".format(ABOUT_AUTHOR_NAME, ABOUT_AUTHOR_EMAIL)
		tkinter.Label(self.main_frame, text=full_name, anchor="w").pack(side="top", fill="x")

		tkinter.Label(self.main_frame, text="", anchor="w").pack(side="top", fill="x")

		tkinter.Message(self.main_frame, text=ABOUT_DESCRIPTION, anchor="w", justify="center", aspect=300, width=400).pack(side="top", fill="x")

		tkinter.Label(self.main_frame, text="", anchor="w").pack(side="top", fill="x")

		version_string = "Версия: {}".format(VERSION)
		tkinter.Label(self.main_frame, text=version_string, anchor="w").pack(side="top", fill="x")


		controls_frame = tkinter.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		self.icon_close = aqicon("close")
		# ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")
		tkinter.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())




	# def destroy(self):
	# 	tkinter.Toplevel.destroy(self)


if __name__ == "__main__":


	root = tkinter.Tk()

	modal = About(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()