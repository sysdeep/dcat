import time


class FNode(object):
	def __init__(self):


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




	def make_data_dict(self):



		result = {
			"uuid"			: self.uuid,
			"name"			: self.name,
			"volume_id"		: self.volume_id,
			"parent_id"		: self.parent_id,
			"ftype"			: self.ftype,
			"rights"		: self.rights,
			"owner"			: self.owner,
			"group"			: self.group,
			"ctime"			: self.ctime,
			"atime"			: self.atime,
			"mtime"			: self.mtime,
			"category"		: self.category,
			"description"	: self.description,
			"size"			: self.size,
		}

		return result


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



def make_fnode(file_data):
	fnode = FNode()
	fnode.uuid = file_data["uuid"]
	fnode.volume_id = file_data["volume_id"]
	fnode.parent_id = file_data["parent_id"]
	fnode.name = file_data["name"]
	fnode.size = file_data["size"]
	fnode.ctime = file_data["ctime"]
	fnode.ftype = file_data["type"]
	fnode.description = file_data["description"]
	return fnode


def make_fnodes(files_array):
	result = []
	for file_data in files_array:
		result.append(make_fnode(file_data))

	return result




def make_vnode(volume_data):
	vnode = VNode()
	vnode.uuid 			= volume_data["uuid"]
	vnode.name 			= volume_data["name"]
	vnode.vtype 		= volume_data["vtype"]
	vnode.path 			= volume_data["path"]
	vnode.created 		= volume_data["created"]
	vnode.updated 		= volume_data["updated"]
	vnode.description 	= volume_data["description"]
	return vnode


def make_vnodes(volumes_array):
	result = []
	for volume_data in volumes_array:
		result.append(make_vnode(volume_data))

	return result