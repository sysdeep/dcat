#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
from Store import Store
# from Writer import Writer
# from Reader import Reader
# from tools import ETimer
# lin
SCAN_PATH = "/home/nia/Music"											# 130 		- gz 2.6 k
SCAN_PATH = "/home/nia/Android"											# 31105 	- gz 504.8 k
SCAN_PATH = "/home/nia/Development/_Comcon"								# 863285 	- gz 15.5 m (14.9 m - strip keys)
# XFILE = "/home/nia/Development/_Python/_DCat/features_files/binvoldict.binvoldict"
XDB = "/home/nia/Development/_Python/_DCat/features_files"

# win
# flat - 9.59 kb

""" 

    74075
        size        - 2.66 Mb
        time        - 5 min
        mem         - 40 mb
"""
# SCAN_PATH = "E:\\Screens"
# SCAN_PATH = "E:\\_Comcon"
# XFILE = "E:\\Tmp\\binvoldict.binvoldict"





# #--- new objects
# etimer = ETimer()
# # Writer(SCAN_PATH, XFILE).start()
# # etimer.elapsed("write")
# Reader(XFILE).print_root_files()
# etimer.elapsed("read")
# # Reader(XFILE).print_tree()






# storew = Store()
# storew.make_db(SCAN_PATH, XFILE)


DB = "6_xml"

store = Store()
# store.create(XDB, DB)
store.open_db(os.path.join(XDB, DB))
# store.add_volume("vol1", SCAN_PATH)

store.read_volume("vol1", SCAN_PATH) 
