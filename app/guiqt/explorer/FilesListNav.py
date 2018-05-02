#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QTreeWidget
from PyQt5.QtGui import QFontDatabase


class FilesListNav(QWidget):
	def __init__(self, parent=None):
		super(FilesListNav, self).__init__(parent)

		self.main_layout = QHBoxLayout(self)



		self.history_stack = []
		self.__stack_items_count = 0






	def reinit(self):
		self.history_stack = []
		self.update_history()


	def history_push(self, fnode):
		self.history_stack.append(fnode)
		self.update_history()


	def update_history(self):

		self.__clear_stack()

		inames = [item.name for item in self.history_stack]
		self.__stack_items_count = len(inames)
		self.__update_btn_back()

		btn_root = QPushButton("/")
		btn_root.clicked.connect(self.__go_root)
		self.main_layout.addWidget(btn_root)

		__last_btn = None
		for i, iname in enumerate(inames):
			iname += " >"
			btn = QPushButton(iname)
			btn.clicked.connect(lambda x=i: self.__go(x))
			self.main_layout.addWidget(btn)
			__last_btn = btn

		if __last_btn:
			__last_btn.setDisabled(True)

		self.main_layout.addStretch()


	def __clear_stack(self):
		print("clear_stack")
		# for widget in self.main_layout.ch
		# for widget in self.stack_frame.winfo_children():
		# 	widget.destroy()

	def __update_btn_back(self):
		print("__update_btn_back")
		# if self.__stack_items_count == 0:
		# 	self.btn_back.configure(state="disabled")
		# else:
		# 	self.btn_back.configure(state="normal")


	def __go_root(self):
		print("__go_root")
		# self.history_clear()
		# if self.cb_root:
		# 	self.cb_root()

	def __go(self, x):
		print("__go", x)
		# fnode = self.history_splice(x)
		#
		# if self.cb_go:
		# 	# self.cb_go(fnode.uuid)
		# 	self.cb_go(fnode)

#
# class StackFrame(QWidget):
# 	def __init__(self, parent):
# 		super(StackFrame, self).__init__(parent)
#
# 		self.cb_root = None
#
# 	def set_items(self, items):
# 		"""
# 			Args:
# 				items	[list]	: ["root", "foo", ...]
# 		"""
# 		self.__clear()
#
# 		btn = tkinter.Button(self, text="root", command=self.__go_root )
# 		btn.pack()
#
# 		for i, iname in enumerate(items):
# 			btn = tkinter.Button(self, text=iname, command=lambda x=i: self.__act_go(x), compound="left" )
# 			btn.pack(side="left")
#
# 			# btn2 = tkinter.Button(self, text=iname, command=lambda x=i: self.__act_go(x) )
# 			# btn2.pack()
#
#
#
# 		# #--- controls
# 		# tkinter.Frame(self, relief="raised", bd=2, height=2).pack(fill="x", padx=5, pady=5)
# 		# controls_frame = tkinter.Frame(self)
# 		# controls_frame.pack(fill="both", side="bottom", padx=10, pady=10)
# 		# ttk.Button(controls_frame, text="Закрыть", image=get_icon("application-exit"), compound="left", command=self.destroy).pack(side="right")
#
#
# 	def __clear(self):
# 		for widget in self.winfo_children():
# 			widget.destroy()
#
#
# 	def __act_go(self, index):
# 		pass
#
# 	def __go_root(self):
# 		if self.cb_root:
# 			self.cb_root()
#
