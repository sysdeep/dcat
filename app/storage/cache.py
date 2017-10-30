#!/usr/bin/env python3
# -*- coding: utf-8 -*-



DATA = {
	"volumes"	: [],
	"system"	: {}
}




def get_volumes():
	return DATA["volumes"]

def set_volumes(volumes):
	DATA["volumes"] = volumes

def clear_volumes():
	DATA["volumes"] = []



def get_system():
	return DATA["system"]

def set_system(system_dict):
	DATA["system"] = system_dict

