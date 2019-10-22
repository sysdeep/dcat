#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from os.path import expanduser, basename
import os.path


from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStyleFactory, QFileDialog
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QTimer, pyqtSignal


from app import shared
from app.storage import get_storage
from app.rc import VERSION, ABOUT_NAME

from .MainMenu import MainMenu
from .MainToolBar import MainToolBar
from .explorer import Explorer


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()



		#--- заголовок окна
		self.title 		= "MS3"

		#--- размеры
		self.max_x = 800
		self.max_y = 600

		#--- стиль окна
		# self.wstyle = ""

		#--- размер окна при старте
		# self.startup_size = def_ui.STUPTUP_SIZE_NORMAL



		#--- объекты
		self.main_menu	= MainMenu()			# меню
		self.main_menu.s_opendb.connect(self.__on_show_open_db)
		self.main_menu.s_createdb.connect(self.__on_show_create_db)
		self.setMenuBar(self.main_menu)

		self.main_toolbar = MainToolBar()
		self.main_toolbar.s_opendb.connect(self.__on_show_open_db)
		self.main_toolbar.s_createdb.connect(self.__on_show_create_db)
		self.addToolBar(self.main_toolbar)

		self.explorer = None
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


		self.storage = get_storage()

		self.usettings = shared.get_usettings()

		# --- проверяем и обновляем список открывавшихся баз
		self.usettings.check_bases_exists()

		# --- открываем последний
		self.__check_open_last()






	def init_gui(self):
		"""построение интерфейса"""

		#--- window meta
		self.setWindowTitle(self.title)
		self.setMinimumWidth(self.max_x)							# min width
		self.setMinimumHeight(self.max_y)


		#--- window style
		# styles = QStyleFactory.keys()
		# if self.wstyle in styles:
		# 	QApplication.setStyle(QStyleFactory.create(self.wstyle))


		# self.setGeometry(300, 300, 300, 300)


		
		

		self.explorer = Explorer()
		self.setCentralWidget(self.explorer)

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
		self.__update_title()
		self.show()


	def __check_open_last(self):
		#--- если в настройках флаг открывать последний
		is_open_last = self.usettings.data["open_last"]
		if is_open_last == 0:
			return False

		last = self.usettings.get_last_base()

		if last:
			self.__open_db(last)








	def __on_show_open_db(self):
		"""отображение открытия базы"""
		home_path = os.path.expanduser("~")
		fname = QFileDialog.getOpenFileName(self, "Выбор базы", home_path, "dcat files (*.dcat)")

		if fname and len(fname[0]):
			self.__open_db(fname[0])	


	def __on_show_create_db(self):
		"""отображение модала сохранения файла"""
		home_path = os.path.expanduser("~")
		fname = QFileDialog.getSaveFileName(self, "Расположение новой базы", home_path, "dcat files (*.dcat)")
		
		if fname and len(fname[0]):
			file_path = fname[0] if fname[0].endswith(".dcat") else fname[0] + ".dcat"
			self.__create_db(file_path)
			
			










	def __open_db(self, db_path):
		"""запрос на открытие базы по заданному пути"""

	
		self.storage.close_storage()
		self.storage.open_storage(db_path)

		self.explorer.reload()
		# self.__update_db_info()
		#
		self.usettings.update_last_base(db_path)
		self.__update_title(db_path)


	def __create_db(self, db_path):

		if os.path.exists(db_path):
			print("Unable create db - file already exists...")
			return False

		self.storage.close_storage()
		self.storage.create_storage(db_path)

		self.explorer.reload()
		# self.__update_db_info()

		self.usettings.update_last_base(db_path)
		self.__update_title(db_path)





	def __update_title(self, db_path=None):
		"""обновить заголовок"""
		if db_path:
			text = "{} v {} - [{}]".format(ABOUT_NAME, VERSION, os.path.basename(db_path))
		else:
			text = "{} v {}".format(ABOUT_NAME, VERSION)
		self.setWindowTitle(text)

		#--- статусная строка
		status_text = db_path if db_path else "---"
		self.statusBar().showMessage(status_text)




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