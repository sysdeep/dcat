#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Store import Store

# lin
# SCAN_PATH = "/home/nia/Music"
SCAN_PATH = "/home/nia/Android"
XFILE = "/home/nia/Development/_Python/_DCat/binvoldict.binvoldict"


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




store = Store()
# store.make_db(SCAN_PATH, XFILE)
store.read_db(XFILE)