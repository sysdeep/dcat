#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import struct


def to_bstring(input: str):
    bstr = input.encode(encoding="utf-8")

    str_len = len(bstr)

    bdata = b""
    bdata += struct.pack("<I", str_len)
    bdata += bstr
    return bdata

def from_bstring(bdata):
    str_len = struct.unpack("<I", bdata[0:4])[0]

    bstr = bdata[4:4+str_len]

    return bstr.decode(encoding="utf-8")

    

def fill_to(bdata, size):
    """дополнить данные до определённого размера"""
    for _ in range(size - len(bdata)):
        bdata += b" "

    return bdata


if __name__ == "__main__":


    s = "Привет"

    bdata = to_bstring(s)

    print(bdata)

    bdata += b"ddddddqwdasd"

    ss = from_bstring(bdata)
    print(ss)