#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QGridLayout
from PyQt5.QtGui import QFontDatabase, QIcon, QPixmap

from app.lib.models.VolumeHeader import VolumeHeader

from ...rc import get_icon_path
from ...ui_common.icons_map import VOLUME_ICONS_MAP

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
		
		self.__db_file_path = QLabel()
		
		
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
		
		row += 1
		layout.addWidget(QLabel("путь до файла базы"), row, 0)
		layout.addWidget(self.__db_file_path, row, 1)
		
		
		
		
		
		
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
		
		
	def set_info(self, header_data: VolumeHeader, db_file_path: str):

		

		self.__name.setText(header_data.name)
		self.__path.setText(header_data.scan_path)
		self.__records_len.setText(str(header_data.records))
		self.__sdata_len.setText(str(header_data.table_len))
		self.__tdata_len.setText(str(header_data.heap_len))
		
		#--- icon
		icon_file = VOLUME_ICONS_MAP.get(header_data.icon, 14)		# other fallback
		icon = QPixmap(get_icon_path("volumes", icon_file))
		self.__icon.setText(str(header_data.icon))
		self.__icon.setPixmap(icon)
		

		self.__db_file_path.setText(db_file_path)


if __name__ == "__main__":
	import sys
	import signal
	from PyQt5.QtWidgets import QApplication



	app = QApplication(sys.argv)

	lamp = VolumeInfo()
	lamp.show()

	sys.exit(app.exec_())