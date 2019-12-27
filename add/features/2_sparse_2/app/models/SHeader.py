#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

    0 - 16 - meta
    16 - 64 - reserved


"""
import struct
from .constants import HEADER_SIZE
from app.utils import to_bstring, from_bstring, fill_to


class SHeader(object):
    # SIZE = 1042*10                      # полный размер блока
    # SYSTEM_SIZE = 1024
    # NAME_SIZE = 1024
    # PATH_SIZE = 1024
    # DESCRIPTION_SIZE = 1024
    def __init__(self):


        #--- data
        self.version = 1            # версия(4b)(4)
        self.created = 2            # дата и время создания(4)
        self.updated = 0            # дата и время модификации(4)
        self.vtype = 0              # тип хранилища(папка, диск, CD...)(4)
        self.total_blocks = 0       # общее кол-во блоков

        # self.name_len = 0
        # self.path_name = 0
        # self.description_len = 0
        self.name = ""              # имя
        self.path = ""              # путь при создании
        self.description = ""       # описание



    @staticmethod
    def pack(model):
        bdata = b""
       
        #--- 16b
        dataset = (
            model.version,
            model.created,
            model.updated,
            model.vtype,
            model.total_blocks,
        )
        bdata  += struct.pack("<IIIII", *dataset);

        # for _ in range(1024 - size(bdata)):
        #     bdata += b"0"

        bdata = fill_to(bdata, 1024)


        strings = (model.name, model.path, model.description)

        for string_item in strings:

            bitem = fill_to(to_bstring(string_item), 1024)
            bdata += bitem


        # bname = fill_to(to_bstring(model.name), 1024)
        # bpath = fill_to(to_bstring(model.path), 1024)
        # bdescription = fill_to(to_bstring(model.description), 1024)

        # bdata += bname
        # bdata += bpath
        # bdata += bdescription

        return bdata


    


    @staticmethod
    def unpack(bdata):

        model = SHeader()
        
        dataset = struct.unpack("<IIIII", bdata[0:20])

        model.version = dataset[0]
        model.created = dataset[1]
        model.updated = dataset[2]
        model.vtype = dataset[3]
        model.total_blocks = dataset[4]

        #--- name
        # name_len = struct.unpack("<I", bdata[1024:1024+4])[0]
        # name = from_bstring(bdata[1024: 1024+1024])
        # print(name)

        start = 1024
        step = 1024
        strings_result = []
        for _ in range(3):
            bitem = bdata[start:start+step]

            str_item = from_bstring(bitem)
            strings_result.append(str_item)

            start += step

        model.name = strings_result[0]
        model.path = strings_result[1]
        model.description = strings_result[2]


        return model

    # def pack_system(self):

    #     data = b""

    #     dataset = (
    #         self.version,
    #         self.created,
    #         self.updated,
    #         self.vtype,
    #     )

    #     data += struct.pack("<IIII", *dataset)

    #     # for _ in range(self.SYSTEM_SIZE - len(data)):
    #     #     data += b"0"

    #     return data

    # def unpack_system(self, bdata):
        
    #     dataset = struct.unpack("<IIII", bdata[0:16])
    #     self.version = dataset[0]
    #     self.created = dataset[1]



    # def get_page(self):
    #     pass



    # def set_page(self, bdata):
    #     pass







if __name__ == "__main__":



    header = SHeader()
    header.name = "Igor"
    header.path = "/ddkf/rrr/ttt"
    header.description = "description fot"

    bdata = SHeader.pack(header)


    # print(bdata)

    un_header = SHeader.unpack(bdata)

    
    print(un_header.version)
    print(un_header.name)
    print(un_header.path)
    print(un_header.description)