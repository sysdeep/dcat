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


class ETimer:
	def __init__(self):
		self.start = time.time()
		self.last = self.start



	def elapsed(self, label):
		timestamp = time.time()

		result_total = timestamp - self.start
		result_last = timestamp - self.last

		self.last = timestamp
		print("{:<16} : {} [+{:.5f}]".format(label, result_total, result_last))