#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Store import Store
from Writer import Writer
from Reader import Reader
from tools import ETimer
# lin
SCAN_PATH = "/home/nia/Music"
# SCAN_PATH = "/home/nia/Android"
# SCAN_PATH = "/home/nia/Development/_Comcon"							# 896833 - 37.4 Mb
XFILE = "/home/nia/Development/_Python/_DCat/features_files/binvoldict.binvoldict"


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





#--- new objects
etimer = ETimer()
Writer(SCAN_PATH, XFILE).start()
etimer.elapsed("write")
Reader(XFILE).print_root_files()
etimer.elapsed("read")
# Reader(XFILE).print_tree()






# storew = Store()
# storew.make_db(SCAN_PATH, XFILE)

# storer = Store()
# storer.read_db(XFILE)