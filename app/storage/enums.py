#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class FType():
    DIR     = 0
    FILE    = 1
    VOLUME  = 100
    UNKNOWN = 200



class FRow():
    UUID    = 0
    PARENT  = 1
    VOLUME  = 2
    NAME    = 3
    TYPE    = 4

    RIGHTS  = 5
    OWNER   = 6
    GROUP   = 7

    SIZE    = 8
    
    CTIME   = 9
    ATIME   = 10
    MTIME   = 11

    CATEGORY = 12
    DESCRIPTION = 13



class VRow(object):
    UUID = 0
    NAME = 1