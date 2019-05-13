#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.lib.EventEmitter import EventEmitter




# SHOW_OPEN_DB = "show_open_db"			# args: path - событие для MainWindow - открыть заданную базу












__emitter = EventEmitter()


def eon(event_name, f):
	__emitter.eon(event_name, f)

def eoff(event_name, f):
	__emitter.eoff(event_name, f)

def emit(event_name, *args, **kwargs):
	__emitter.emit(event_name, *args, **kwargs)