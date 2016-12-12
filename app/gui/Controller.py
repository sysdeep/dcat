#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
from . import events
from app import log
from app.logic import load_tree, store_tree
# from .utils.WalkerDispatcher import WalkerDispatcher



class Controller(object):
	def __init__(self):



		# events.on("set_scan_path", self.set_scan_path)
		events.on("set_save_file", self.set_save_file)
		events.on("set_open_file", self.set_open_file)
		# events.on("start_scan", self.start_scan)


	


	def set_save_file(self, path):

		store_tree(path)
	


	def set_open_file(self, path):
		log.info("open db file: " + path)
		load_tree(path)
		events.update_tree()


