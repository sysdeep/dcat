#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	система обмена событиями в GUI
"""

from app.lib import EventEmitter

emitter = EventEmitter()


def on(event_name, cb):
	"""подписаться на события"""
	emitter.eon(event_name, cb)





def set_scan_path(path):
	emitter.emit("set_scan_path", path)



def start_scan():
	emitter.emit("start_scan")


def set_save_file(path):
	emitter.emit("set_save_file", path)


def set_open_file(path):
	emitter.emit("set_open_file", path)




def update_tree():
	emitter.emit("update_tree")


#
#
# def show_tray_message(text, title="", state="info"):
# 	"""
# 		отобразить сообщение из системного трея
#
# 		on:
# 			SystemTray.py
# 	"""
# 	emitter.emit("show_tray_message", title, text, state)