#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QGridLayout
from PyQt5.QtGui import QFontDatabase

from app.storage.volume.VolumeHeader import VolumeHeader


class VolumeInfo(QGroupBox):
	def __init__(self, parent=None):
		super(VolumeInfo, self).__init__(parent)
		self.setTitle("Volume info")
		
		layout = QGridLayout()
		self.setLayout(layout)
		
		
		self.__name = QLabel()
		self.__path = QLabel()
		self.__icon = QLabel()
		self.__records_len = QLabel()
		self.__sdata_len = QLabel()
		self.__tdata_len = QLabel()
		
		
		row = 0
		
		layout.addWidget(QLabel("название"), row, 0)
		layout.addWidget(self.__name, row, 1)
		
		row += 1
		layout.addWidget(QLabel("путь"), row, 0)
		layout.addWidget(self.__path, row, 1)
		
		row += 1
		layout.addWidget(QLabel("иконка"), row, 0)
		layout.addWidget(self.__icon, row, 1)
		
		row += 1
		layout.addWidget(QLabel("всего записей"), row, 0)
		layout.addWidget(self.__records_len, row, 1)
		
		row += 1
		layout.addWidget(QLabel("длина таблицы"), row, 0)
		layout.addWidget(self.__sdata_len, row, 1)
		
		row += 1
		layout.addWidget(QLabel("длина текста"), row, 0)
		layout.addWidget(self.__tdata_len, row, 1)
		
		
		
		
		
		
		# self.magic = 0
		# self.version = 0
		# self.icon_id = 0
		# self.created= 0
		# self.records_len = 0
		# self.name = ""
		# self.path = ""
		# self.description = ""
		#
		# self.section_table_len = 0
		# self.section_text_len = 0
		
		
	def set_info(self, header_data: VolumeHeader):
		print(header_data.name)


		self.__name.setText(header_data.name)
		self.__path.setText(header_data.scan_path)
		self.__icon.setText(str(header_data.icon))
		self.__records_len.setText(str(header_data.records))
		self.__sdata_len.setText(str(header_data.table_len))
		self.__tdata_len.setText(str(header_data.heap_len))
		



if __name__ == "__main__":
	import sys
	import signal
	from PyQt5.QtWidgets import QApplication



	app = QApplication(sys.argv)

	lamp = VolumeInfo()
	lamp.show()

	sys.exit(app.exec_())