#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from app.models.SMeta import SMeta
from app.models.SHeader import SHeader
from app.models.SBlock import SBlock
from app.fhandler import Writer
from app.fhandler import Reader


def write_file(file_path):
    meta = SMeta()
    meta.version = 2

    header = SHeader()
    header.name = "test"
    header.path = file_path

    
        

    writer = Writer(file_path)

    #--- meta
    writer.set_meta(meta)
    
    #--- header
    dir_files = os.listdir(".")
    header.total_blocks = len(dir_files)
    writer.set_header(header)

    #--- files
    f_counter = 0
    for f in dir_files:
        block = SBlock()
        block.name = f
        writer.append_body_block(f_counter, block)
        f_counter += 1
    

    #!!! Error - OSError: Negative seek in write mode
    #--- gzip - я так понял, нельзя выполнять поиск и запись в пред. позицию...
    # header.total_blocks = f_counter
    # writer.set_header(header)

    writer.save()




def read_file(file_path):
    reader = Reader(file_path)
    
    print("file version: ", reader.meta.version)
    print("name: ", reader.header.name)
    print("path: ", reader.header.path)
    print("total blocks: ", reader.header.total_blocks)
    print("="*20)
    print("blocks")
    print("="*20)


    for i in range(reader.header.total_blocks):
        print(reader.read_block(i).name)
    
    
    # print(reader.read_block(0).name)
    # print(reader.read_block(1).name)
    # print(reader.read_block(2).name)
    # print(reader.read_block(3).name)
    # print(reader.read_block(4).name)
    


# write_file("t1.gz")
read_file("t1.gz")