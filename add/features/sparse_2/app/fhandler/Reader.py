#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip

from app.models.constants import META_SIZE, HEADER_SIZE, BLOCK_SIZE
from app.models.SMeta import SMeta
from app.models.SHeader import SHeader
from app.models.SBlock import SBlock

class Reader(object):
    def __init__(self, file_path):
        
        self.file_path = file_path
        self.fd = gzip.open(self.file_path, "rb")

        self.meta = None
        self.header = None

        self.fd.seek(0, 2)

        db_size = self.fd.tell()
        body_size = db_size - META_SIZE - HEADER_SIZE
        print("body: ", body_size)

        self.__read()


    def __read(self):

        #--- read meta
        self.fd.seek(0)
        meta_bdata = self.fd.read(META_SIZE)
        self.meta = SMeta.unpack(meta_bdata)

        #--- read header
        self.fd.seek(META_SIZE)
        header_bdata = self.fd.read(HEADER_SIZE)
        self.header = SHeader.unpack(header_bdata)


    def close_file(self):
        self.fd.close()


    def read_block(self, num):
        start = META_SIZE + HEADER_SIZE + (num * BLOCK_SIZE)

        self.fd.seek(start)
        bdata = self.fd.read(BLOCK_SIZE)

        block = SBlock.unpack(bdata)

        return block


    # def set_meta(self, meta: SMeta):
    #     self.__meta = meta


    # def set_header(self, header):
    #     self.__header = header


    # def save(self):
    #     fd = gzip.open(self.file_path, "wb")

    #     #--- write meta
    #     fd.seek(0)
    #     meta_bdata = SMeta.pack(self.__meta)
    #     fd.write(meta_bdata)

    #     #--- write heder
    #     # fd.seek(META_SIZE)

    #     fd.close()



    # def read_file(self, path):
    #     pass
    
    #     #--- read meta
    #     fd.seek(0)
    #     bdata = df.read(META_SIZE)

    #     meta = SMeta.unpack(bdata)

    #     #--- read header
    #     # fd.seek(META_SIZE)
    #     # header_bdata = fd.read(meta.header_size)




