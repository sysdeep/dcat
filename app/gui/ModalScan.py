#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout, QFileDialog, QTextEdit
from PyQt5.QtGui import QFont

from . import events
from app.rc import set_scan_dir, get_scan_dir
from app import log
from .utils.WalkerDispatcher import WalkerDispatcher
from app.logic import twalker

class ModalScan(QDialog):
	def __init__(self, parent=None):
		super(ModalScan, self).__init__(parent)

		self.main_layout = QVBoxLayout()
		self.setLayout(self.main_layout)



		self.scan_dir = get_scan_dir()
		self.scan_dir_label = QLabel(self.scan_dir)


		self.walker_dispatcher = WalkerDispatcher(self)
		self.walker_dispatcher.msg.connect(self.__handle_new_message)

		self.__make_gui()


	def __make_gui(self):






		self.main_layout.addWidget(self.scan_dir_label)


		self.text_edit = QTextEdit()
		self.text_edit.setReadOnly(True)
		self.text_edit.setFont(QFont("Roboto mono"))
		self.main_layout.addWidget(self.text_edit)


		# self.main_layout.addStretch()

		controls_layout = QHBoxLayout()
		self.main_layout.addLayout(controls_layout)

		btn_open_dir = QPushButton("Open")
		btn_open_dir.clicked.connect(self.__open_dir)



		btn_start_scan = QPushButton("Scan")
		btn_start_scan.clicked.connect(self.__start_scan)



		btn_close = QPushButton("close")
		btn_close.clicked.connect(self.close)

		controls_layout.addWidget(btn_open_dir)
		controls_layout.addWidget(btn_start_scan)
		controls_layout.addStretch()
		controls_layout.addWidget(btn_close)


	def __open_dir(self):
		dlg = QFileDialog()
		# dlg.setAcceptMode(QFileDialog.AcceptOpen)
		dlg.setFileMode(QFileDialog.Directory)
		dlg.setOption(QFileDialog.ShowDirsOnly, True)


		if dlg.exec_():
			files = dlg.selectedFiles()
			print(files)
			if len(files) > 0:
				# set_scan_dir(files[0])
				path = files[0]
				self.__set_scan_dir(path)







	def __start_scan(self):
		log.info("start scaning")
		self.text_edit.clear()


		self.walker_dispatcher.start()

		log.debug("scan_dir: " + self.scan_dir)
		# self.tree.set_empty()


		# walker.start(scan_dir, self.tree)
		twalker.start(self.scan_dir)

		log.debug("done")

		# self.tree.print_nodes()
		# events.update_tree()



	def __set_scan_dir(self, path):

		set_scan_dir(path)
		self.scan_dir = path
		self.scan_dir_label.setText(self.scan_dir)


	def __handle_new_message(self, data):
		log.warning(data)


		if data["event"] == "start":
			self.text_edit.append("start")

		elif data["event"] == "start_scan":
			self.text_edit.append("start_scan")

		elif data["event"] == "finish_scan":
			self.text_edit.append("finish_scan")
			self.text_edit.append("time: {}".format(data["sec"]))
			self.text_edit.append("items: {}".format(data["items_count"]))


		elif data["event"] == "start_tree":
			self.text_edit.append("start_tree")

		elif data["event"] == "finish_tree":
			self.text_edit.append("finish_tree")
			self.text_edit.append("time: {}".format(data["sec"]))

		elif data["event"] == "progress":
			self.text_edit.append("progress: {}".format(data["prc"]))

		elif data["event"] == "finish":


			# self.tree.print_nodes()

			events.update_tree()


