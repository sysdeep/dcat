#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time


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










# class Node(object):
# 	def __init__(self):
# 		self.is_volume = False
# 		self.is_dir = False
# 		self.is_file = False




class VNode(object):
	def __init__(self):
		self.uuid = None
		self.name = ""
		self.vtype = "other"
		self.path = ""
		self.created = "---"




class FNode(object):
	def __init__(self):
		self.uuid = None
		self.name = ""


		self.volume_id	= ""
		self.parent_id	= ""
		self.uuid	= ""
		self.name	= ""
		self.ftype	= 0

		self.rights	= 0

		self.owner	= ""
		self.group	= ""
			
		self.ctime	= 0
		self.atime	= 0
		self.mtime	= 0

		self.category	= 0
		self.description	= ""

		self.size	= 0


		self.parents = []					# спсиок родителей для рекурсивного поиска



	def is_file(self):
		return self.ftype == 1

	def is_dir(self):
		return self.ftype == 0


	def fctime(self):
		return self.__format_date(self.ctime)

	def fmtime(self):
		return self.__format_date(self.mtime)
	
	def fatime(self):
		return self.__format_date(self.atime)

	def __format_date(self, ctime):
		t = time.gmtime(ctime)
		result = time.strftime("%Y-%m-%d %H:%M:%S", t)
		return result



	def make_parents_path(self, is_self=False):
		parents = [parent.name for parent in self.parents]

		if is_self:
			parents.append(self.name)

		# parents.insert(0, "")
		parents_str = "/".join(parents)

		return "/" + parents_str











# class CommonFile(Node):
# 	def __init__(self):
# 		super(CommonFile, self).__init__()


# 		self.volume_id	= ""
# 		self.parent_id	= ""
# 		self.uuid	= ""
# 		self.name	= ""
# 		self.type	= 0

# 		self.rights	= 0

# 		self.owner	= ""
# 		self.group	= ""
			
# 		self.ctime	= 0
# 		self.atime	= 0
# 		self.mtime	= 0

# 		self.category	= 0
# 		self.description	= ""

# 		self.size	= 0







# class VDir(CommonFile):
# 	def __init__(self):
# 		super(VDir, self).__init__()
# 		self.is_dir = True



# class VFile(CommonFile):
# 	def __init__(self):
# 		super(VFile, self).__init__()
# 		self.is_file = True





