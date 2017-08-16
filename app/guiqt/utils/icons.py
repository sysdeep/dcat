#!/usr/bin/env python
# -*- coding: utf-8 -*-


from PyQt5.QtGui import QIcon
from app.rc import get_icon_path

def qicon(file_name):
    return QIcon(get_icon_path(file_name))