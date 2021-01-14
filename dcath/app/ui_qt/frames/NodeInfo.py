#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QGroupBox, QGridLayout

from app.lib.models.FileRecord import FileRecord


class NodeInfo(QGroupBox):
	def __init__(self, parent=None):
		super(NodeInfo, self).__init__(parent)
		self.setTitle("Node info")
		
		self.main_layout = QVBoxLayout(self)
		
		grid = QGridLayout()
		
		
		
		self.__name = QLabel()
		self.__ftype = QLabel()
		self.__size = QLabel()
		self.__ctime = QLabel()
		self.__rights = QLabel()
		self.__fid = QLabel()
		self.__pid = QLabel()
		
		# self.npos = 0
		# self.nsize = 0
		# self.dpos = 0
		# self.dsize = 0
	
		self.__description = QLabel()
		
		
		
		row = 0
		
		grid.addWidget(QLabel("название"), row, 0)
		grid.addWidget(self.__name, row, 1)
		
		row += 1
		grid.addWidget(QLabel("тип"), row, 0)
		grid.addWidget(self.__ftype, row, 1)
		
		row += 1
		grid.addWidget(QLabel("размер"), row, 0)
		grid.addWidget(self.__size, row, 1)
		
		row += 1
		grid.addWidget(QLabel("дата"), row, 0)
		grid.addWidget(self.__ctime, row, 1)
		
		row += 1
		grid.addWidget(QLabel("права"), row, 0)
		grid.addWidget(self.__rights, row, 1)
		
		row += 1
		grid.addWidget(QLabel("id"), row, 0)
		grid.addWidget(self.__fid, row, 1)
		
		row += 1
		grid.addWidget(QLabel("parent id"), row, 0)
		grid.addWidget(self.__pid, row, 1)
		
		row += 1
		grid.addWidget(QLabel("description"), row, 0)
		grid.addWidget(self.__description, row, 1)
		
		
		
		
		self.main_layout.addLayout(grid)
		self.main_layout.addStretch()
		
		
		
		
	def set_info(self, data: FileRecord):

		ftype_text = "каталог" if data.ftype == FileRecord.FTYPE_CATALOG else "файл"

		self.__name.setText(data.name)
		self.__ftype.setText(ftype_text)
		self.__ctime.setText(str(data.ctime))
		self.__rights.setText(str(data.right))
		self.__fid.setText(str(data.fid))
		self.__pid.setText(str(data.pid))
		self.__size.setText(str(data.size))
		
		# self.npos = 0
		# self.nsize = 0
		# self.dpos = 0
		# self.dsize = 0
	
		self.__description.setText(data.description)

		








if __name__ == "__main__":
	import sys
	import signal
	from PyQt5.QtWidgets import QApplication



	app = QApplication(sys.argv)

	lamp = NodeInfo()
	lamp.show()

	sys.exit(app.exec_())