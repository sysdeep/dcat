#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tkinter

from .Menu import BarMenu
# from .TreeFrame import TreeFrame
# from .DataFrame import DataFrame
from .explorer import Explorer

from app.logic import load_tree_demo

class MainWindow(tkinter.Tk):
	def __init__(self):
		super(MainWindow, self).__init__()


		self.title("DCat")
		# self.iconphoto(self, get_icon("gnome-app-install-star"))

		self.menu_bar = BarMenu(self)

		# self.tree_frame = TreeFrame(self, width=800)
		# self.tree_frame.pack(side="left", fill="both", expand=False)

		self.explorer_frame = Explorer(self, width=800)
		self.explorer_frame.pack(side="left", fill="both", expand=False)


		# self.data_frame = DataFrame(self)
		# self.data_frame.pack(side="right", fill="both", expand=True)

		# self.__main_bar = None						# main bar - top
		# self.__mnemo_bar = None
		# self.footer_bar = None
		# self.__ioaction_bar = None

		# status bar
		self.status_bar_text = tkinter.StringVar()
		self.status_bar_text.set("--")



		# load_tree_demo()




if __name__ == "__main__":


	# from .dummyloop import dummyloop

	# from base.iodum import iodum
	# from base.sender import sender


	app = MainWindow()
	app.mainloop()



# 	# root.geometry("350x250+300+300")
