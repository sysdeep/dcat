#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	dbus - системная шина сообщений
"""
from .EventEmitter import EventEmitter

DATA = {
	"emitter"	: EventEmitter()
}


#--- actions
SHOW_ABOUT_VOLUME 		= "show_about_volume"			# args: vnode
# SHOW_ABOUT_FILE 		= "show_about_file"				# args: fnode			2018.03.06 - removed(modal in flist)
SHOW_ABOUT_BASE 		= "show_about_base"				# args: None
# SHOW_EDIT_VOLUME 		= "show_edit_volume"			# args: vnode
SHOW_ADD_VOLUME			= "show_add_volume"				# args: None
SHOW_FIND				= "show_find"					# args: None
SHOW_SETTINGS			= "show_settings"				# args: None
SHOW_DATABASES			= "show_databases"				# args: None


#--- export
SHOW_EXPORT_VOLUME		= "show_export_volume"			# args: volume_id, volume_name
SHOW_EXPORT_VOLUME_A	= "show_export_volume_a"		# args: volume_id, volume_name
SHOW_EXPORT_VOLUME_B	= "show_export_volume_b"		# args: volume_id, volume_name
SHOW_EXPORT_VOLUME_10	= "show_export_volume_10"		# args: volume_id, volume_name
SHOW_EXPORT_VOLUME_OK	= "show_export_volume_ok"		# args: None
SHOW_EXPORT_VOLUME_ERR	= "show_export_volume_err"		# args: None

SHOW_EXPORT_FTREE 		= "show_export_ftree"			# args: fnode 	-
# SHOW_REMOVE_FTREE		= "show_remove_ftree"			# args: fnode 	-
# SHOW_REMOVE_FTREE_OK	= "show_remove_ftree_ok"		# args: None


#--- import
SHOW_IMPORT_VOLUME		= "show_import_volume"			# args: None



REQUEST_OPEN_DB			= "request_open_db"				# args: db_path - событие для MainWindow - открыть заданную базу



#---
SCAN_COMPLETE			= "scan_complete"				# args: None

















def eon(event_name, f):
	DATA["emitter"].eon(event_name, f)

def eoff(event_name, f):
	DATA["emitter"].eoff(event_name, f)

def emit(event_name, *args, **kwargs):
	DATA["emitter"].emit(event_name, *args, **kwargs)



