#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time, signal, sys
from app import log
from app.rc import QUE_WALKER, DIR_SCAN
from . import twalker



def signal_handler(signum, frame):
	"""обработчик сигнала завершения от системы"""
	log.info("перехвачен сигнал SIGINT(Ctrl+C)")
	log.info("запрос на выход из cmd")
	# self.stop()

	sys.exit(0)



def set_signal():
	signal.signal(signal.SIGINT, signal_handler)		# обработка Ctrl+C





def main():

	set_signal()
	twalker.start(DIR_SCAN)


	while True:
		print("main loop")


		data = QUE_WALKER.get()
		print("-->", data)

		# time.sleep(1)




if __name__ == "__main__":
	main()