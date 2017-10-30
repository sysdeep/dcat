#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json


def make_volume(vnode):
	result = {
		"uuid"	: vnode.uuid,

	}


def make(file_export_path, volumes, files=None):


	result = {
		"volumes"	: []
	}


	for volume in volumes:
		result["volumes"].append(volume.make_data_dict())

