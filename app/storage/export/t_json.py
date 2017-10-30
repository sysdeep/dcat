#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	тестирование экспорта и импорта
"""

from ..main import get_storage


DB = "/home/nia/Development/_Python/_DCat/2.dcat"
EXFILE = "/home/nia/Development/_Python/_DCat/2.json"

storage = get_storage()
storage.open_storage(DB)



storage.export_db(EXFILE)




