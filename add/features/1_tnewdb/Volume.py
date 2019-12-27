#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gzip
import struct


from Header import Header
from utils import to_bstring, from_bstring




class Volume(object):
    MODE_NONE = 0
    MODE_READ = 1
    MODE_WRITE = 2

    BLOCK_SIZE = 1024*4
    def __init__(self, db_path):
        self.db_path = db_path
        self.name = ""
        self.__mode = 0
        self.__fd = None

    # def opendb(self, path):
    #     self.__fd = gzip.open("data.gz", "r+b")

    def set_mode(self, mode_enum):
        """переключить режим использования"""
        pass

    def read_block(self, num: int):
        """прочитать заданный блок"""
        self.remount(self.MODE_READ)

        start = self.BLOCK_SIZE * num
        self.__fd.seek(start)
        bdata = self.__fd.read(self.BLOCK_SIZE)
        return bdata

    def write_block(self, num: int, bdata):
        """записать заданный блок"""
        st = self.remount(self.MODE_WRITE)

        # TODO: check bdata size
        start = self.BLOCK_SIZE * num
        self.__fd.seek(start)
        self.__fd.write(bdata)
        
    def remount(self, mode_enum):
        """переключить в заданный режим"""
        if self.__mode == mode_enum:
            return True

        self.__mode = mode_enum
        

        if self.__mode is self.MODE_NONE:
            return False



        if self.__fd is not None:
            self.__fd.close()
            self.__fd = None

        
        md = None

        if self.__mode == self.MODE_READ:
            md = "rb"

        if self.__mode == self.MODE_WRITE:
            md = "wb"

        

        self.__fd = gzip.open(self.db_path, md)

        return True
    
    def umount(self):
        if self.__fd is None:
            return True

        self.__fd.close()
        self.__mode = self.MODE_NONE

        return True







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



    st = Volume("volume.gz")

    bdata = b"hello"

    for i in range(10):
        # st.write_block(i, bdata)
        bdata = st.read_block(i)
        print(bdata)

    # header = Header()

    # st.write_header(header)

    # st.read_header()



    # st.append_blocks(10000)
