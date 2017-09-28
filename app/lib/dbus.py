#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	dbus - системная шина сообщений
"""
from .EventEmitter import EventEmitter

DATA = {
	"emitter"	: EventEmitter()
}


#--- events consts
SHOW_ABOUT_VOLUME 		= "show_about_volume"			# args: vnode
SHOW_ABOUT_FILE 		= "show_about_file"				# args: fnode
SHOW_ABOUT_BASE 		= "show_about_base"				# args: None
SHOW_EDIT_VOLUME 		= "show_edit_volume"			# args: vnode
SHOW_ADD_VOLUME			= "show_add_volume"				# args: None

STORAGE_VOLUME_UPDATED 	= "storage_volume_updated"		# args: volume_uuid

SCAN_COMPLETE			= "scan_complete"				# args: None

def eon(event_name, f):
	DATA["emitter"].eon(event_name, f)

def eoff(event_name, f):
	DATA["emitter"].eoff(event_name, f)

def emit(event_name, *args, **kwargs):
	DATA["emitter"].emit(event_name, *args, **kwargs)



