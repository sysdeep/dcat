#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.rc import get_icon_path
from .defs import VOLUME_ICONS, IPACK


def get_volume_icon(volume_icon_type):
	def vicon(name):

		i = real_icon(pack, "volumes", VOLUME_ICONS[name])
		VCACHE[name] = i
		return i

