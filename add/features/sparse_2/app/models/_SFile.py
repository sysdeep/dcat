#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Структура файла

    -------------------------
    | meta                  |
    -------------------------
    | header                |
    -------------------------
    | body                  |
    -------------------------
"""

import struct
from .constants import META_SIZE


class SFile(object):
    # SIZE = 1042*10                      # полный размер блока
    # SYSTEM_SIZE = 1024
    # NAME_SIZE = 1024
    # PATH_SIZE = 1024
    # DESCRIPTION_SIZE = 1024
    def __init__(self):


        #--- file sections
        self.meta = None
        self.header = None
        self.body = None







        #--- data
        self.version = 1            # версия(4b)
        self.created = 2            # дата и время создания
        self.updated = 0            # дата и время модификации
        self.vtype = 0              # тип хранилища(папка, диск, CD...)

        # self.name_len = 0
        # self.path_name = 0
        # self.description_len = 0
        self.name = ""              # имя
        self.path = ""              # путь при создании
        self.description = ""       # описание



    def __make_meta(self):
        pass


    # @staticmethod



    def pack_system(self):

        data = b""

        dataset = (
            self.version,
            self.created,
            self.updated,
            self.vtype,
        )

        data += struct.pack("<IIII", *dataset)

        # for _ in range(self.SYSTEM_SIZE - len(data)):
        #     data += b"0"

        return data

    def unpack_system(self, bdata):
        
        dataset = struct.unpack("<IIII", bdata[0:16])
        self.version = dataset[0]
        self.created = dataset[1]



    def get_page(self):
        pass



    def set_page(self, bdata):
        pass







if __name__ == "__main__":



    header = Header()
    data = header.pack_system()


    print(data)

    header.unpack_system(data)
    print(header.version)
    print(header.created)