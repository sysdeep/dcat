#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class VNode(object):
	def __init__(self):
		self.uuid = None
		self.name = ""
		self.vtype = "other"
		self.path = ""
		self.created = "---"
		self.updated = "---"