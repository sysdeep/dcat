#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from converter.Converter import Converter



SRC_DB = "/home/nia/2.dcat"
DST_DIR = "/home/nia/Development/_Python/_DCat/Export10/"


converter = Converter()
converter.start(SRC_DB, DST_DIR)