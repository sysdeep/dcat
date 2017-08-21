#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os.path

from tkinter import *
from tkinter.filedialog import *
# from lib.ee import main_ee
# from .widgets.IOTestDialog import IOTestDialog
# from .widgets.IOTableDialog import IOTableDialog

# from .modals.units_feeder import UnitsFeederModal
# from .modals.units_belt_v import UnitsBeltVModal
# from .modals.units_belt_h import UnitsBeltHModal
# from .modals.units_system import UnitsSystemModal
# from .modals.units_upost import UnitsUpostModal
# from .modals.units_bunkers import UnitsBunkersModal

# from .modals.system_cmd import SystemCMDModal

class BarMenu():
	"""
	BarMain widget
	"""
	def __init__(self, parent):
		self.parent = parent
		self.menu = None


		self.cb_create = None
		self.cb_open = None


		#--- key bindings
		self.parent.bind_all("<Control-q>", lambda e: self.__c_exit())


		self.makeMenu()



		# main_ee.on("input", self.handle_input)



	# def handle_input(self, key, value):
	# 	print(key, value)



		
	def makeMenu(self):
		self.menu = Menu(self.parent, relief="flat")
		self.parent.config(menu=self.menu)

		file_menu = Menu(self.menu, tearoff=0)
		self.menu.add_cascade(label="File", menu=file_menu)
		file_menu.add_command(label="Open", command=self.c_open_db)
		file_menu.add_command(label="Create", command=self.c_create_db)
		file_menu.add_separator()
		file_menu.add_command(label="Exit", command=self.__c_exit, compound="left", accelerator="Ctrl+q")


		# units_menu = Menu(self.menu)
		# self.menu.add_cascade(label="Оборудование", menu=units_menu)
		# units_menu.add_command(label="Система", command=self.c_units_system)
		# units_menu.add_command(label="Воронка", command=self.c_units_feeder)
		# units_menu.add_command(label="Наклонный транспортёр", command=self.c_units_belt_v)
		# units_menu.add_command(label="Распределительный транспортёр", command=self.c_units_belt_h)
		# units_menu.add_command(label="Пост погрузчика", command=self.c_units_upost)
		# units_menu.add_command(label="Бункеры инертных", command=self.c_units_bunkers)




		# about_menu = Menu(self.menu)
		# self.menu.add_cascade(label="About", menu=about_menu)
		# about_menu.add_command(label="Open", command=self.c_about)
		# about_menu.add_command(label="Exit", command=self.c_exit)

		# system_menu = Menu(self.menu)
		# self.menu.add_cascade(label="System", menu=system_menu)
		# system_menu.add_command(label="IO Table Dialog", command=self.c_iotabledialog)

		# debug_menu = Menu(self.menu)
		# self.menu.add_cascade(label="Debug", menu=debug_menu)
		# debug_menu.add_command(label="IO Dialog", command=self.c_iodialog)
		# debug_menu.add_command(label="CMD Dialog", command=self.c_cmddialog)
		# debug_menu.add_command(label="Exit", command=self.c_exit)





	def __c_exit(self):
		print("exit")
		self.parent.quit()
		# main_ee.emit("exit")

	def c_about(self):
		win = Toplevel()
		lab = Label(win, text="Это просто программа-тест \n меню в Tkinter")
		lab.pack()


	def c_create_db(self):
		title = 'Choose the output directory'
		op = asksaveasfilename(defaultextension=".dcat", title=title)
		if op and self.cb_create:
			self.cb_create(op)




	def c_open_db(self):
		inpath = askopenfilename(
				title=u"Select ADEPT-encrypted PDF file to decrypt",
				defaultextension=u".dcat", filetypes=[('DCat files', '.dcat')])

		if inpath and self.cb_open:
			inpath = os.path.normpath(inpath)
			self.cb_open(inpath)


	def set_cb_create(self, cb):
		self.cb_create = cb

	def set_cb_open(self, cb):
		self.cb_open = cb

# 	def c_iodialog(self):
# 		IOTestDialog(self.parent)

# 	def c_cmddialog(self):
# 		SystemCMDModal(self.parent)


# 	def c_iotabledialog(self):
# 		IOTableDialog(self.parent)






# 	def c_units_feeder(self):
# 		UnitsFeederModal(self.parent)

# 	def c_units_upost(self):
# 		UnitsUpostModal(self.parent)

# 	def c_units_belt_v(self):
# 		UnitsBeltVModal(self.parent)

# 	def c_units_belt_h(self):
# 		UnitsBeltHModal(self.parent)

# 	def c_units_system(self):
# 		UnitsSystemModal(self.parent)

# 	def c_units_bunkers(self):
# 		UnitsBunkersModal(self.parent)

# if __name__ == "__main__":





# 	root = Tk()


# 	def exit():
# 		root.quit()

# 	main_ee.on("exit", exit)

# 	root.geometry("350x250+300+300")
# 	bar = BarMenu(root)
# 	# bar.grid()

# 	Button(root, text="Quit", command=quit).grid()
# 	root.mainloop()