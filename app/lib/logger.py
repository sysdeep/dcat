#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from os import mkdir
import logging
import logging.handlers
import sys
import platform





#--- если платформа Windows - не раскрашиваем(пока)
if platform.system() == 'Windows':
	TTY = False
else:
	TTY = True

"""
цвета посмотреть тут
http://misc.flogisoft.com/bash/tip_colors_and_formatting
"""
TTY_COLORS = {
	0: '\x1b[0m',			# not set - normal
	10: '\x1b[34m',			# debug - blue
	20: '\x1b[32m',			# info - green
	30: '\x1b[33m',			# warning - yellow
	40: '\x1b[95m',			# error - pink
	50: '\x1b[91m'			# critical - red
}

class ColorConsoleHandler(logging.StreamHandler):
	# def __init__(self, stream=None):
	# 	super(consoleLogger, self).__init__(stream)


	def __make_color(self, level, msg):
		if TTY is False:
			return msg

		color = TTY_COLORS[level]

		return color + msg + TTY_COLORS[0]


	def emit(self, record):

		try:
			msg = self.__make_color(record.levelno, self.format(record) )
			stream = self.stream
			stream.write(msg)
			stream.write(self.terminator)
			self.flush()
		except Exception:
			self.handleError(record)














log 		= logging.getLogger("app")
log.setLevel(logging.DEBUG)				# всё от DEBUG и выше

def setup_console():
	format_console = logging.Formatter("%(asctime)s - [%(module)s] - %(message)s", datefmt='%H:%M:%S')
	# handler = logging.StreamHandler(sys.stderr)
	handler = ColorConsoleHandler(sys.stderr)
	handler.setFormatter(format_console)
	log.addHandler(handler)


setup_console()







if __name__ == "__main__":
	log.debug('debug message')
	log.info('info message')
	log.warn('warn message')
	log.error('error message')
	log.critical('critical message')
	try:
		a=1/0
	except:
		log.exception("exception message")
	log.critical("critical message")