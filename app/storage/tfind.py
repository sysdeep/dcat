#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import get_storage



DB_PATH = "/home/nia/Development/_Python/_DCat/reanimator.dcat"




if __name__ == "__main__":


    storage = get_storage()
    storage.open_storage(DB_PATH)



    # storage.find_items("ant")
    v = storage.get_db_version()
    print(v)