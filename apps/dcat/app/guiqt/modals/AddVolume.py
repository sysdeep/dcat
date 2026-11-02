#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import threading
import time
from queue import Queue
import uuid
from datetime import datetime

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, \
	QLabel, QLineEdit, QComboBox, QTextEdit, QProgressBar, QFileDialog
from PyQt5.QtCore import Qt

from app.storage.models.VNode import VNode
from app.data import VOLUME_TYPE
from app import log
from app.storage import get_storage

from .. import icons



def now_date():
	return time.strftime("%Y-%m-%d %H:%M:%S")


class AddVolume(QDialog):
	def __init__(self, parent=None):
		super(AddVolume, self).__init__(parent)
		
		
		self.storage = get_storage()
		
		self.main_layout = QVBoxLayout(self)

		#--- main form
		form = QGridLayout()

		self.edit_path = QLineEdit()
		self.btn_select_path = QPushButton(icons.get_icon(icons.I_OPEN_FOLDER), "")
		self.btn_select_path.clicked.connect(self.__show_select_dir)
		
		self.edit_vname = QLineEdit()
		
		
		self.edit_icon = QComboBox()
		for vtype in VOLUME_TYPE:
			self.edit_icon.addItem(icons.get_volume_icon(vtype), vtype)
		
		self.edit_description = QTextEdit()
		self.edit_description.setMaximumHeight(100)
		self.edit_progress = QProgressBar()

		row = 0
		form.addWidget(QLabel("Каталог: "), row, 0, Qt.AlignRight)
		form.addWidget(self.edit_path, row, 1)
		form.addWidget(self.btn_select_path, row, 2)
		
		row += 1
		form.addWidget(QLabel("Название тома: "), row, 0, Qt.AlignRight)
		form.addWidget(self.edit_vname, row, 1, 1, 2)
		
		
		row += 1
		form.addWidget(QLabel("Иконка: "), row, 0, Qt.AlignRight)
		form.addWidget(self.edit_icon, row, 1, 1, 2)
		
		row += 1
		form.addWidget(QLabel("Описание: "), row, 0, Qt.AlignRight | Qt.AlignTop)
		form.addWidget(self.edit_description, row, 1, 1, 2)
		


		#--- controls
		controls = QHBoxLayout()
		
		self.btn_quit = QPushButton(icons.get_icon(icons.I_EXIT), "Закрыть")
		self.btn_quit.clicked.connect(self.close)
		
		self.btn_start = QPushButton(icons.get_icon(icons.I_START), "Запуск")
		self.btn_start.clicked.connect(self.start_action)
		
		self.label_error = QLabel()
		
		controls.addWidget(self.btn_start)
		controls.addStretch()
		controls.addWidget(self.btn_quit)
		
		
		
		#--- make layout
		self.main_layout.addLayout(form)
		self.main_layout.addSpacing(20)
		self.main_layout.addWidget(self.edit_progress)
		self.main_layout.addSpacing(20)
		self.main_layout.addWidget(self.label_error)
		self.main_layout.addStretch()
		self.main_layout.addLayout(controls)


		
		



	def start_action(self):
		"""запуск сканирования"""
		log.info("запуск сканирования")
		vpath = self.edit_path.text()
		vname = self.edit_vname.text()
		
		vicon_index = self.edit_icon.currentIndex()
		vicon = VOLUME_TYPE[vicon_index]
		
		vdescription = self.edit_description.toPlainText()
		
		
		print(vpath, vname, vicon, vdescription)


		log.info("каталог для сканирования: " + vpath)
		log.info("название: " + vname)

		#--- проверка входных данных
		self.__update_err("")
		result, err = self.__prepare_scan(vpath, vname)

		if result is False:
			log.warning(err)
			self.__update_err(err)
			return False


		#--- обновляем статус
		self.__update_state(is_started=True)


		stime_start = datetime.now()
		log.info("начало сканирования: " + now_date())



		#--- create volume record
		self.__create_volume_record()

		#
		#
		#
		# self.files_counter = 0
		#
		#
		# #--- запуск канала чтения потока
		# self.__start_chan_reader()
		#
		#
		# # t = threading.Thread(target=scan_dir, args=(self.volume_path, self.chan))
		# t = threading.Thread(target=scaner.start_scan, args=(self.volume_path, self.chan))
		# t.start()


	def __update_err(self, err_text):
		self.label_error.setText(err_text)
	
	def __prepare_scan(self, vpath, vname):

		if not os.path.exists(vpath):
			return False, "выбранный каталог не существует"

		if len(vname) == 0:
			return False, "название не должно быть пустым"

		return True, None


	def __show_select_dir(self):
		
		home_path = os.path.expanduser("~")
		spath = QFileDialog.getExistingDirectory(self, "Выбор каталога для сканирования", home_path)
		
		
		
		if spath:
			# spath = os.path.normpath(spath)
			# self.volume_path = spath
			# self.select_label.config(text=self.volume_path)
			
			self.edit_path.setText(spath)

			volume_name = os.path.basename(spath)
			self.edit_vname.setText(volume_name)
			# self.volume_name_entry.delete(0, "end")
			# self.volume_name_entry.insert(0, volume_name)

			# self.scan_path_entry.delete(0, "end")
			# self.scan_path_entry.insert(0, self.volume_path)

			# self.__start_scan(spath)




	def __update_state(self, is_started: bool):
		self.btn_start.setDisabled(is_started)
		self.btn_quit.setDisabled(is_started)

	
	def __create_volume_record(self):
		log.info("создание записи о томе")
		self.volume_id = str(uuid.uuid4())
		vdata = {
			"name" 			: self.volume_name,
			"uuid" 			: self.volume_id,
			"path" 			: self.volume_path,
			"vtype" 		: self.volume_vtype,
			"description"	: self.volume_description,
			"created" 		: now_date()
		}
		
		self.storage.create_volume_row(vdata)






if __name__ == "__main__":

	import sys
	from PyQt5.QtWidgets import QApplication

	app = QApplication(sys.argv)



	dialog = AddVolume()
	dialog.show()


	# view.show()



	sys.exit(app.exec_())