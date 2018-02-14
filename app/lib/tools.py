#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


def dtimeit(func):
	"""декоратор для замера времени выполнения"""
	def timed(*args, **kwargs):
		ts = time.time()
		result = func(*args, **kwargs)
		te = time.time()

		print("timeit: ", te - ts)
		return result

	return timed
