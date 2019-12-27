#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    структура метаданных файла
"""
import struct
from .constants import META_SIZE





class SMeta(object):
    # SIZE = 1042*10                      # полный размер блока
    # SYSTEM_SIZE = 1024
    # NAME_SIZE = 1024
    # PATH_SIZE = 1024
    # DESCRIPTION_SIZE = 1024
    def __init__(self):


        #--- data
        self.magic = "sdcat"            # идентификатор типа файла(8 байт)      sdcat
        self.version = 1                # версия файла(4 байта)
        self.size = META_SIZE           # размер блока meta(4)
        self.header_size = 1024         # размер блока заголовка(4)
        self.body_block_size = 1024     # размер блока в теле(4)


        # self.version = 1            # версия(4b)
        # self.created = 2            # дата и время создания
        # self.updated = 0            # дата и время модификации
        # self.vtype = 0              # тип хранилища(папка, диск, CD...)

        # self.name_len = 0
        # self.path_name = 0
        # self.description_len = 0
        # self.name = ""              # имя
        # self.path = ""              # путь при создании
        # self.description = ""       # описание


    @staticmethod
    def pack(model):
        bdata = b""
        for _ in range(8):
            bdata += b" "

        dataset = (
            model.version,
            model.size,
            model.header_size,
            model.body_block_size
        )

        bdata  += struct.pack("<IIII", *dataset);

        return bdata


    @staticmethod
    def unpack(bdata):

        model = SMeta()

        bmagic = bdata[0:8]
        dataset = struct.unpack("<IIII", bdata[8:24])

        model.version = dataset[0]
        model.size = dataset[1]
        model.header_size = dataset[2]
        model.body_block_size = dataset[3]

        return model






if __name__ == "__main__":


    meta = SMeta()

    bdata = SMeta.pack(meta)

    print(bdata)


    unpack_meta = SMeta.unpack(bdata)

    print(unpack_meta.version)
    print(unpack_meta.size)
    print(unpack_meta.header_size)
    print(unpack_meta.body_block_size)


    # header = SMeta()
    # data = header.pack_system()


    # print(data)

    # header.unpack_system(data)
    # print(header.version)
    # print(header.created)