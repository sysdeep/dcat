#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def make_frow(uid, name, parent_id, ftype, st):
	"""используется при обходе файловой системы"""
	item = {
		"volume_id": "",
		"parent_id": parent_id,
		"uuid": uid,
		"name": name,
		"type": ftype,

		"rights": st.st_mode,

		"owner": st.st_uid,
		"group": st.st_gid,

		"ctime": st.st_ctime,
		"atime": st.st_atime,
		"mtime": st.st_mtime,

		"category": 0,
		"description": "",

		"size": st.st_size
	}
	return item
