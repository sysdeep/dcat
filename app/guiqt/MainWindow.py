#!/usr/bin/env python3
# -*- coding: utf-8 -*-




from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QStyleFactory
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QTimer, pyqtSignal


from app import shared
from app.storage import get_storage

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
		self.main_menu	= None			# меню
		self.main_toolbar = None
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


		self.main_menu = MainMenu(self)
		self.main_toolbar = MainToolBar(self)

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
		self.show()


	def __check_open_last(self):
		#--- если в настройках флаг открывать последний
		is_open_last = self.usettings.data["open_last"]
		if is_open_last == 0:
			return False

		last = self.usettings.get_last_base()

		if last:
			self.__on_open_db(last)




	def __on_open_db(self, db_path):
		"""запрос на открытие базы по заданному пути"""

		# #--- проверка существования базы
		# if not os.path.exists(db_path):
		# 	self.usettings.remove_last(db_path)
		# 	return False

		self.storage.close_storage()
		self.storage.open_storage(db_path)

		self.explorer.reload()
		# self.__update_db_info()
		#
		# self.usettings.update_last_base(db_path)
		# self.__update_title(db_path)







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