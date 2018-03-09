#!/usr/bin/env python3
# -*- coding: utf-8 -*-




from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStyleFactory
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QTimer, pyqtSignal


from .MainMenu import MainMenu


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()



		#--- заголовок окна
		self.title 		= "MS3"

		#--- размеры
		# self.max_x = 1600
		# self.max_y = 950

		#--- стиль окна
		# self.wstyle = ""

		#--- размер окна при старте
		# self.startup_size = def_ui.STUPTUP_SIZE_NORMAL



		#--- объекты
		self.main_menu	= None			# меню
		# self.mnemo 		= None			# мнемосхема
		# self.bar_menu	= None
		# self.server 	= None			# ссылка на сервер
		# self.project 	= None			# ссылка на проект с данными
		# self.client 	= None			# ссылка на клиента TCP(для внутренних нужд)




		#--- add fonts
		# QFontDatabase.addApplicationFont(get_font_path("Play-Bold.ttf"))
		# QFontDatabase.addApplicationFont(get_font_path("roboto", "RobotoRegular.ttf"))
		# QFontDatabase.addApplicationFont(get_font_path("roboto", "RobotoMono-Regular.ttf"))


		#--- FEATURES... ------------------------------------------------------
		#--- system tray
		#--- !!! KDE-error - при закрытии MainWindow трей остаётся висеть... и приложение не останавливается....
		#--- сейчас нагрузки на него нет - пока отключаем
		# tray = SystemTray(self)
		# tray.show()
		#--- FEATURES... ------------------------------------------------------

		# dbus.eon(dbus.SHOW_ERROR_VIEW, self.__on_error_view)
		# dbus.eon(dbus.SHOW_MODAL_REQRES, self.__on_show_modal_reqres)
		# dbus.eon(dbus.SHOW_MODAL_INFO_DATA, self.__on_show_modal_info_data)

		self.init_gui()



	def init_gui(self):
		"""построение интерфейса"""

		#--- window meta
		self.setWindowTitle(self.title)
		# self.setMinimumWidth(self.max_x)							# min width
		# self.setMinimumHeight(self.max_y)


		#--- window style
		# styles = QStyleFactory.keys()
		# if self.wstyle in styles:
		# 	QApplication.setStyle(QStyleFactory.create(self.wstyle))


		# self.setGeometry(300, 300, 300, 300)


		self.main_menu = MainMenu(self)

		# self.init_central_gui()


		#--- status bar
		self.statusBar().showMessage('ready')



		#--- отображение в зависимости от настроек отображения окна
		# if self.startup_size == def_ui.STUPTUP_SIZE_FULL:				# полный экран
		# 	self.showFullScreen()
		# elif self.startup_size == def_ui.STUPTUP_SIZE_MAX:				# максимально возможный
		# 	self.showMaximized()
		# else:															# по умолчанию не меньше настроек
		#
		self.show()


	def init_central_gui(self):
		#--- mnemo bar
		self.setCentralWidget(self.mnemo)




	def act_exit(self):
		# log.info("запрос на закрытие приложения")
		self.close()



	def closeEvent(self, QCloseEvent):
		"""перехват зактытия окна - предварительные завершения для объектов"""

		# log.info("закрытие приложения - останавливаем процессы")

		# #--- clientTCP
		# if self.client:
		# 	self.client.stop()
		# 	# self.client.wait()

		#--- packages logger
		# self.packages_logger.terminate()
		# self.packages_logger.wait()

		# self.reader.terminate()
		# self.reader.quit()

		# self.unbind()

		# log.info("закрытие приложения - выходим")
		QCloseEvent.accept()













if __name__ == "__main__":

	import sys
	from PyQt5.QtWidgets import QApplication

	app = QApplication(sys.argv)



	dialog = MainWindow()
	# dialog.show()


	# view.show()



	sys.exit(app.exec_())