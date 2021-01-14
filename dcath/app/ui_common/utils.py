#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


def convert_ctime(ctime:int) -> str:
	"""перевод даты ctime в текстовое представление"""
	t = time.gmtime(ctime)
	result = time.strftime("%Y-%m-%d %H:%M:%S", t)
	return result