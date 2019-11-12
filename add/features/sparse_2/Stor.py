#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .st.constants import META_SIZE
from .st.SMeta import SMeta

class Stor(object):
    def __init__(self):
        pass




    def read_file(self, path):
        pass
    
        #--- read meta
        fd.seek(0)
        bdata = df.read(META_SIZE)

        meta = SMeta.unpack(bdata)

        #--- read header
        # fd.seek(META_SIZE)
        # header_bdata = fd.read(meta.header_size)




