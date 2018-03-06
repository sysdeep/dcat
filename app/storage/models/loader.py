#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import FNode, VNode






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