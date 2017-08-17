#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import shared
from .Storage import Storage


def get_storage():
    storage = shared.get_storage()
    if storage is None:
        print("create storage")
        storage = Storage()
        shared.set_storage(storage)

    return storage





if __name__ == "__main__":

    from app.rc import FILE_DB_TEST
    # FILE_PATH = "/home/nia/Development/_Python/_DCat/dcat/tests/s1.db"
    FILE_PATH = FILE_DB_TEST


    storage = get_storage()
    storage.create_storage(FILE_PATH)
    # storage.open_storage(FILE_PATH)
    # volumes = storage.get_volumes()
    # files = storage.get_files()


    # print("volumes:")
    # print(volumes)

    # for v in volumes:
    #     files = storage.get_files(volume=v[1])
    #     print(len(files))

    # print()

    # print("files:")
    # print(files)
