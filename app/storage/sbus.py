#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
	sbus - шина сообщений
"""
from app.lib.EventEmitter import EventEmitter

DATA = {
	"emitter"	: EventEmitter()
}


STORAGE_OPENED			= "storage_opened"				# args: None
STORAGE_CLOSED			= "storage_closed"				# args: None
STORAGE_CREATED			= "storage_created"				# args: None
STORAGE_VOLUME_UPDATED 	= "storage_volume_updated"		# args: volume_uuid

DB_COMMITTED			= "db_committed"				# args: None - база сохранена
DB_MIGRATED				= "db_migrated"					# args: None - база произвела миграцию

def eon(event_name, f):
	DATA["emitter"].eon(event_name, f)

def eoff(event_name, f):
	DATA["emitter"].eoff(event_name, f)

def emit(event_name, *args, **kwargs):
	DATA["emitter"].emit(event_name, *args, **kwargs)



