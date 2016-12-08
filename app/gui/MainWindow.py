#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QTimer, pyqtSignal


from app import log
from .MainFrame import MainFrame
from app.logic import get_tree, load_tree, load_tree_demo


# from ..logic import get_server, get_project
# from .modals import LoginWindow
# from ..storage import ulog
# from app.rc import get_font_path
# from .BarMenu import BarMenu
# from .SystemTray import SystemTray
# from . import events


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		log.debug("инициализация главного окна программы")
		self.TERMINATED = False
		# self.mnemo 		= None
		# self.DEBUG 		= False
		# self.DEBUG_SHOW_LOGIN = False


		self.max_x = 800
		self.max_y = 600

		self.setWindowTitle("DCat")
		self.setMinimumWidth(self.max_x)							# min width
		self.setMinimumHeight(self.max_y)


		# self.server 	= get_server()
		# self.project 	= get_project()
		# self.client 	= None


		#--- add fonts
		# QFontDatabase.addApplicationFont(get_font_path("Play-Bold.ttf"))
		# QFontDatabase.addApplicationFont(get_font_path("roboto", "RobotoRegular.ttf"))
		# QFontDatabase.addApplicationFont(get_font_path("roboto", "RobotoMono-Regular.ttf"))


		self.__init_gui()




		#--- system tray
		# tray = SystemTray(self)
		# tray.show()


		






	def __init_gui(self):

		# self.setGeometry(300, 300, 300, 300)

		#--- main menu
		# BarMenu(self)

		#--- mnemo bar
		self.__make_main()

		#--- status bar
		self.__make_status_bar()



		self.show()



	


	def __make_main(self):

		"""
			---------------------------------------
			| central_widget
			|	-------------------------
			|	| central_box			|
			|	|	---------			|
			|	|	| mnemo	|			|
			|	|	---------			|
			|	|						|
			|	|	-----------------	|
			|	|	| bottom_field	|	|
			|	|	-----------------	|
			|	|						|
			|	-------------------------
			|
			----------------------------------------

		"""



		#--- central_widget
		central_widget = QWidget(self)
		# central_widget.setContentsMargins(0, 0, 0, 0)
		self.setCentralWidget(central_widget)
		# self.setContentsMargins(0, 0, 0, 0)				# mainwindow margins

		

		#--- central_box
		# central_box = QVBoxLayout()
		# central_widget.setLayout(central_box)
		central_box = QVBoxLayout(central_widget)
		# central_box.setContentsMargins(0, 0, 0, 0)




		main_frame = MainFrame()
		central_box.addWidget(main_frame)


		# #--- bottom_field
		# bottom_field = QHBoxLayout()

		# quit_btn = QPushButton("Выход")
		# quit_btn.clicked.connect(self.exit)

		# bottom_field.addStretch(1)
		# bottom_field.addWidget(quit_btn)





		# #--- mnemo
		# #-- временно корректируем на момент отладки штоб не появлялись ползунки
		# max_x = self.max_x - 30
		# max_y = self.max_y - 80
		# self.mnemo = BarMnemo(max_xx=max_x, max_yy=max_y, parent=self)
		# self.mnemo.setContentsMargins(0, 0, 0, 0)



		# central_box.addWidget(self.mnemo)
		# central_box.addLayout(bottom_field)


		# tree = get_tree()
		load_tree_demo()

		main_frame.update_tree()



	def __make_status_bar(self):
		self.statusBar().showMessage('Ready')






	def exit(self):
		log.info("запрос на закрытие приложения")
		self.close()



	def closeEvent(self, QCloseEvent):
		"""перехват зактытия окна - предварительные завершения для объектов"""

		log.info("закрытие приложения - останавливаем процессы")

		log.info("закрытие приложения - выходим")
		QCloseEvent.accept()









if __name__ == "__main__":

	# from PyQt5.QtWidgets import QStyleFactory
	# from PyQt5.QtCore import QStyleFactory

	app = QApplication(sys.argv)

	# app.setStyle(QStyleFactory.create("fusion"))

	main_win = MainWindow()
	# main_win.DEBUG = True
	# main_win.start_net()

	app.exec_()

