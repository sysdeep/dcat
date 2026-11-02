#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QTreeWidget
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal

# from app.storage.models.FNode import FNode

class FilesListNav(QWidget):
	go_root_signal = pyqtSignal()
	# go_node_signal = pyqtSignal(FNode)

	def __init__(self, parent=None):
		super(FilesListNav, self).__init__(parent)

		self.main_layout = QHBoxLayout(self)



		self.history_stack = []
		self.__stack_items_count = 0

		# self.__buttons = []

		# self.history_layout = QHBoxLayout()

		self.btn_root = QPushButton("/")
		self.btn_root.clicked.connect(self.__go_root)

		self.btn_back = QPushButton("back")
		self.btn_back.clicked.connect(self.__on_back)
		
		
		
		self.main_layout.addWidget(self.btn_root)
		self.main_layout.addWidget(self.btn_back)
		# self.main_layout.addLayout(self.history_layout)
		self.main_layout.addStretch()




		#--- start
		self.__update_back_btn()
		self.__update_root_btn()




	def reinit(self):
		self.history_stack = []
		self.__update_back_btn()
		self.__update_root_btn()
		# self.update_history()


	def history_push(self, fnode):
		self.history_stack.append(fnode)
		self.__update_back_btn()
		self.__update_root_btn()
		# self.update_history()


	# def update_history(self):

	# 	self.__clear_stack()

	# 	inames = [item.name for item in self.history_stack]
	# 	self.__stack_items_count = len(inames)
	# 	self.__update_btn_back()

		

	# 	__last_btn = None
	# 	for i, iname in enumerate(inames):
	# 		iname += " >"
	# 		btn = QPushButton(iname)
	# 		btn.clicked.connect(lambda x=i: self.__go(x))
	# 		self.history_layout.addWidget(btn)
	# 		__last_btn = btn

	# 	if __last_btn:
	# 		__last_btn.setDisabled(True)

		


	# def __clear_stack(self):
	# 	print("clear_stack")
	# 	w = self.history_layout.takeAt(0)
	# 	print(w)
	# 	# for widget in self.main_layout.ch
	# 	# for widget in self.stack_frame.winfo_children():
	# 	# 	widget.destroy()



	def __go_root(self):
		self.go_root_signal.emit()


	def __on_back(self):
		if self.history_stack:

			if len(self.history_stack) > 1:
				self.history_stack.pop()
				node = self.history_stack[-1]
				self.go_node_signal.emit(node)	
			else:
				self.go_root_signal.emit()
			

	# def __go(self, x):
	# 	print("__go", x)
	# 	# fnode = self.history_splice(x)
	# 	#
	# 	# if self.cb_go:
	# 	# 	# self.cb_go(fnode.uuid)
	# 	# 	self.cb_go(fnode)



	def __update_back_btn(self):
		self.btn_back.setEnabled(len(self.history_stack))

	def __update_root_btn(self):
		self.btn_root.setEnabled(len(self.history_stack))















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
