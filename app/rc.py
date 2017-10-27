#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
from queue import Queue

DIR_SELF = os.path.dirname(os.path.abspath(__file__))
DIR_MEDIA = os.path.normpath(os.path.join(DIR_SELF, "..", "media"))

DIR_ICONS = os.path.join(DIR_MEDIA, "icons")

DIR_SCAN = os.path.normpath(os.path.join(DIR_SELF, "..", "..", "sdir"))
# FILE_JSON = os.path.normpath(os.path.join(DIR_SELF, "..", "sdir.json"))
FILE_JSON = os.path.normpath(os.path.join(DIR_SELF, "..", "..", "sdir.json"))
#FILE_DB_TEST = "/home/nia/Development/_Python/_DCat/dcat/tests/s1.db"
FILE_DB_TEST = os.path.normpath(os.path.join(DIR_SELF, "..", "..", "simple.db"))




VERSION = "0.0.1"
ABOUT_NAME = "DCat"
ABOUT_AUTHOR_NAME = "nia"
ABOUT_AUTHOR_EMAIL = "sysdeep@yandex.ru"
ABOUT_SLUG = "Менеджер каталогов съёмных носителей"
ABOUT_DESCRIPTION = """
DCat позволяет управлять базой данных CD, DVD или других съёмных носителей для быстрого просмотра и поиска, без необходимости подключать накопитель.
"""


QUE_WALKER = Queue()





def get_icon_path(*icon_subpath):
	return os.path.join(DIR_ICONS, *icon_subpath)




def set_scan_dir(new_path):
	global DIR_SCAN
	DIR_SCAN = new_path

def get_scan_dir():
	global DIR_SCAN
	return DIR_SCAN