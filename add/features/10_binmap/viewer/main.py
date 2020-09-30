#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from app.App import App



DB_PATH = "/home/nia/Development/_Python/_DCat/Export10/Video.bm.gz"
# DB_PATH = "/home/nia/Development/_Python/_DCat/Export10/Apps.bm.gz"





if __name__ == "__main__":

	if len(sys.argv) > 1:
		path = sys.argv[1]
	else:
		path = DB_PATH
	app = App(db_path=path)
	app.start()
	
	