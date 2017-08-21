#!/usr/bin/env python3
# -*- coding: utf-8 -*-



class LNode(object):
	def __init__(self, uuid, ftype):
		self.uuid = uuid
		self.ftype = ftype
		self.name = ""

		self.data = None