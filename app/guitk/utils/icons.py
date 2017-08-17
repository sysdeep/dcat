#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import PhotoImage
# from PyQt5.QtGui import QIcon
from app.rc import get_icon_path

def qicon(file_name):
    file_path = get_icon_path(file_name)
    return PhotoImage(file=file_path)