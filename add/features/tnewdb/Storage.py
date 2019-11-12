#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import struct


from Header import Header
from utils import to_bstring, from_bstring



class FPage(object):
    PAGE_SIZE = 1024*4
    def __init__(self, name):
        self.name = name




class Storage(object):
    def __init__(self):
        self.__fd = None

    # def opendb(self, path):
    #     self.__fd = gzip.open("data.gz", "r+b")

    def write_header(self, header):
        header_system = header.pack_system()

        name = to_bstring("Привет")
        desc = to_bstring("Description")
        path = to_bstring("Path")


        with gzip.open("data.gz", "wb") as fd:

            fd.seek(0)
            fd.write(header_system)

            fd.seek(1024)
            fd.write(name)

            fd.seek(1024 * 2)
            fd.write(desc)

            fd.seek(1024 * 3)
            fd.write(path)



    def read_header(self):

        with gzip.open("data.gz", "rb") as fd:
            fd.seek(0)
            bsystem = fd.read(1024)

            fd.seek(1024)
            bname = fd.read(1024)

            name = from_bstring(bname)
            print(name)


            fd.seek(1024 * 2)
            bdesc = fd.read(1024)

            desc = from_bstring(bdesc)
            print(desc)

    def append_blocks(self, num):
        BLOCK_SIZE = 1024*4
        START_BLOCK = 1
        
        with gzip.open("data.gz", "wb") as fd:
            for i in range(num):
                bname = to_bstring("name " + str(i))

                fd.seek(START_BLOCK * BLOCK_SIZE)
                fd.write(bname)

                START_BLOCK += 1




if __name__ == "__main__":



    st = Storage()

    # header = Header()

    # st.write_header(header)

    # st.read_header()



    st.append_blocks(10000)