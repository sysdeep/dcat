#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time, signal, sys
from app import log
from app.rc import QUE_WALKER, DIR_SCAN, FILE_JSON
from . import twalker

from app.logic import get_tree, fs
from app.lib.mtree import Render, Tree



def signal_handler(signum, frame):
	"""обработчик сигнала завершения от системы"""
	log.info("перехвачен сигнал SIGINT(Ctrl+C)")
	log.info("запрос на выход из cmd")
	# self.stop()

	sys.exit(0)



def set_signal():
	signal.signal(signal.SIGINT, signal_handler)		# обработка Ctrl+C




def scan_export():
	#--- scan
	tree = Tree()
	tree.start_scan(DIR_SCAN)

	r = Render(tree)
	r.show()

	result = tree.start_export()

	fs.store_file(FILE_JSON, result)



def import_tree():
	data_dict = fs.load_file(FILE_JSON)
	tree = Tree()
	tree.start_import(data_dict)

	r = Render(tree)
	r.show()



def main():
	# DIR_SCAN = "/home/nia/Documents"
	set_signal()
	twalker.start(DIR_SCAN)


	while True:
		# print("main loop")


		data = QUE_WALKER.get()
		print("-->", data)

		if data["event"] == "finish":
			tree = get_tree()
			r = Render(tree)
			r.show()

		# time.sleep(1)




if __name__ == "__main__":
	# main()

	# scan_export()

	import_tree()