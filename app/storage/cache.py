#!/usr/bin/env python3
# -*- coding: utf-8 -*-



DATA = {
	"volumes"	: []
}




def get_volumes():
	return DATA["volumes"]

def set_volumes(volumes):
	DATA["volumes"] = volumes

def clear_volumes():
	DATA["volumes"] = []