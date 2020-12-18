#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
!!! не работает с методами класса...
"""
import time


def mtimeit(msg=""):
	"""декоратор для замера времени выполнения"""
	def worker(func):
		def timed(*args, **kwargs):
			ts = time.time()
			result = func(*args, **kwargs)
			te = time.time()
	
			print("{}: {} [{}]".format(msg, te - ts, func.__name__))
			return result
		
		return timed

	return worker


def dtimeit(func):
	"""декоратор для замера времени выполнения"""
	# def timed(*args, **kwargs):
	def timed(*args):
		ts = time.time()
		# result = func(*args, **kwargs)
		result = func(*args)
		te = time.time()

		print("timeit: {} [{}]".format(te - ts, func.__name__))
		return result

	return timed








if __name__ == "__main__":
	
	@mtimeit("qqq func")
	@dtimeit
	def qqq():
		print("start")
		time.sleep(1)
		print("end")
		
		
		
	qqq()