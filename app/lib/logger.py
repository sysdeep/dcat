#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from os import mkdir
import logging
import logging.handlers
import sys
import platform




log 		= logging.getLogger("app")
log.setLevel(logging.DEBUG)				# всё от DEBUG и выше

def setup_console():
	format_console = logging.Formatter("%(asctime)s - [%(module)s] - %(message)s", datefmt='%H:%M:%S')
	handler = logging.StreamHandler(sys.stderr)
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