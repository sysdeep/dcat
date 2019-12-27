#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from Store import Store
from Writer import Writer
from Reader import Reader
from tools import ETimer
# lin
SCAN_PATH = "/home/nia/Music"
SCAN_PATH = "/home/nia/Android"
SCAN_PATH = "/home/nia/Development/_Comcon"							
# SCAN_PATH = "/home/nia/Development/_Python/_DCat/features_files/dataset"
XFILE = "/home/nia/Development/_Python/_DCat/features_files/binvolmem.bin"


# SCAN_PATH = "E:\\Screens"
# SCAN_PATH = "E:\\_Comcon"
# XFILE = "E:\\Tmp\\binvoldict.binvoldict"





#--- new objects
etimer = ETimer()
# Writer(SCAN_PATH, XFILE).start()
# etimer.elapsed("write")
Reader(XFILE).print_root_files()
etimer.elapsed("read")
# Reader(XFILE).print_tree()



