#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import PhotoImage
# from PyQt5.QtGui import QIcon
from app.rc import get_icon_path

def qicon(file_name):
	file_path = get_icon_path(file_name)
	return PhotoImage(file=file_path)






VOLUME_ICONS = {
	"cd"        : "cdwriter_unmount.png",
	"audio_cd"  : "cdaudio_unmount.png",
	"dvd"       : "dvd_unmount.png",
	"folder"    : "user_home.png",
	"hdd"       : "hdd_unmount.png",
	"hdd_usb"   : "hdd_usb_unmount.png",
	"flash"     : "usbpendrive_unmount.png",
	"sd"        : "sd_mmc_unmount.png",
	"floppy"    : "document_save.png",
	"net"       : "nfs_unmount.png",
	"tape"      : "media_tape.png",
	"other"     : "contents.png"
}

def volume_icon(name):
	file_name = VOLUME_ICONS.get(name)
	if file_name is None:
		file_name = "contents.png"
	return PhotoImage(file=get_icon_path("volumes", file_name))


ALIACES = {
	"close"     : "exit.png",
	"error"     : "error.png",
	"info"		: "info.png",
	"edit"		: "edit.png",
	"save"		: "document_save.png",
	"trash"		: "edittrash.png"
}

def aqicon(name):
	if name in ALIACES:
		return qicon(ALIACES[name])

	return qicon("error")
