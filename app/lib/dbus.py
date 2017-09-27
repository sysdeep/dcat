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
SHOW_ABOUT_VOLUME = "show_about_volume"				# args: vnode



def eon(event_name, f):
	DATA["emitter"].eon(event_name, f)

def eoff(event_name, f):
	DATA["emitter"].eoff(event_name, f)

def emit(event_name, *args, **kwargs):
	DATA["emitter"].emit(event_name, *args, **kwargs)



