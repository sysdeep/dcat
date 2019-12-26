#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Store import Store

SCAN_PATH = "/home/nia/Music"
XFILE = "/home/nia/Development/_Python/_DCat/binvoldict.binvoldict"




store = Store()
store.make_db(SCAN_PATH, XFILE)
store.read_db(XFILE)