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
		self.description = ""


	def make_data_dict(self):

		result = {
			"uuid"			: self.uuid,
			"name"			: self.name,
			"vtype"			: self.vtype,
			"path"			: self.path,
			"created"		: self.created,
			"updated"		: self.updated,
			"description"	: self.description
		}

		return result