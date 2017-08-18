#!/usr/bin/env python3
# -*- coding: utf-8 -*-




def make_frow():
	item = {
		"volume_id": "",
		"parent_id": "",
		"uuid": "",
		"name": "",
		"type": 0,

		"rights": 0,

		"owner": "",
		"group": "",
			
		"ctime": 0,
		"atime": 0,
		"mtime": 0,

		"category": 0,
		"description": "",

		"size"	: 0
	}
	return item



class Node(object):
	def __init__(self):
		self.is_volume = False
		self.is_dir = False
		self.is_file = False


class Volume(Node):
	def __init__(self):
		super(Volume, self).__init__()
		self.is_volume = True

		self.uuid = None
		self.name = ""




class CommonFile(Node):
	def __init__(self):
		super(CommonFile, self).__init__()


		self.volume_id	= ""
		self.parent_id	= ""
		self.uuid	= ""
		self.name	= ""
		self.type	= 0

		self.rights	= 0

		self.owner	= ""
		self.group	= ""
			
		self.ctime	= 0
		self.atime	= 0
		self.mtime	= 0

		self.category	= 0
		self.description	= ""

		self.size	= 0







class VDir(CommonFile):
	def __init__(self):
		super(VDir, self).__init__()
		self.is_dir = True



class VFile(CommonFile):
	def __init__(self):
		super(VFile, self).__init__()
		self.is_file = True





