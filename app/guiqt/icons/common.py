#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtGui import QIcon

from app.rc import get_icon_path
from .defs import VOLUME_ICONS, FTYPE_ICONS, IPACK



def real_icon(*args):
	"""получить объект иконки по произвольному пути"""
	file_path = get_icon_path(*args)
	return file_path


def get_volume_icon(volume_icon_type):
	icon = VOLUME_ICONS.get(volume_icon_type, "no_icon.png")
	return QIcon(get_icon_path(IPACK, "volumes", icon))

def get_ftype_icon(file_type_icon):
	icon = FTYPE_ICONS.get(file_type_icon, "no_icon.png")
	return QIcon(get_icon_path(IPACK, "ftypes", icon))


def get_icon(icon_name):
	return QIcon(get_icon_path(IPACK, icon_name))