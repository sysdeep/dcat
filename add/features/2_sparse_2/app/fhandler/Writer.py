#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip

from app.models.constants import META_SIZE, HEADER_SIZE, BLOCK_SIZE
from app.models.SMeta import SMeta
from app.models.SHeader import SHeader
from app.models.SBlock import SBlock

class Writer(object):
    def __init__(self, file_path):
        
        self.file_path = file_path
        self.__fd = fd = gzip.open(self.file_path, "wb")

        self.__meta = None
        self.__header = None


    def set_meta(self, meta: SMeta):
        self.__meta = meta

        #--- write meta
        self.__fd.seek(0)
        meta_bdata = SMeta.pack(self.__meta)
        self.__fd.write(meta_bdata)


    def set_header(self, header):
        self.__header = header


        #--- write heder
        self.__fd.seek(META_SIZE)
        header_bdata = SHeader.pack(self.__header)
        self.__fd.write(header_bdata)



    def append_body_block(self, num, block):
        """добавить блок данных в заданную позицию"""
        
        start = META_SIZE + HEADER_SIZE + (num * BLOCK_SIZE)

        block_bdata = SBlock.pack(block)
        self.__fd.seek(start)
        self.__fd.write(block_bdata)



    def save(self):
        

        


        self.__fd.close()



    # def read_file(self, path):
    #     pass
    
    #     #--- read meta
    #     fd.seek(0)
    #     bdata = df.read(META_SIZE)

    #     meta = SMeta.unpack(bdata)

    #     #--- read header
    #     # fd.seek(META_SIZE)
    #     # header_bdata = fd.read(meta.header_size)




