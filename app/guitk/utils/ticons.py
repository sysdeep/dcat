#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tkinter import PhotoImage
from app.rc import get_icon_path


#--- standart icons -----------------------------------------------------------
CLOSE 	= "close"
ERROR 	= "error"
INFO 	= "info"
EDIT	= "edit"
SAVE	= "save"
TRASH	= "trash"
GO_NEXT	= "next"
GO_PREV = "go_prev"
OPEN_FOLDER = "open_folder"

I_OPEN_FILE = "i_open_file"
I_CREATE_FILE = "i_create_file"
I_ADD_ITEM = "i_add_item"
I_SAVE_AS = "i_save_as"
I_FIND = "i_find"
I_BOOKMARK = "i_bookmark"
I_EXPORT = "i_export"
I_IMPORT = "i_import"


ALIACES = {
	CLOSE     		: "exit.png",
	ERROR     		: "error.png",
	INFO			: "info.png",
	EDIT			: "edit.png",
	SAVE			: "save.png",
	TRASH			: "edittrash.png",
	GO_NEXT			: "go_next.png",
	GO_PREV			: "go_prev.png",
	OPEN_FOLDER		: "open_folder.png",
	I_OPEN_FILE		: "open_file.png",
	I_CREATE_FILE	: "create_file.png",
	I_ADD_ITEM		: "add_item.png",
	I_SAVE_AS		: "save_as.png",
	I_FIND			: "find.png",
	I_BOOKMARK		: "bookmark.png",
	I_EXPORT		: "export.png",
	I_IMPORT		: "import.png"
}


#--- file_list icons ----------------------------------------------------------
F_FOLDER = "f_folder"
F_EMPTY = "f_empty"

F_ALIACES = {
	F_FOLDER	: "folder.png",
	F_EMPTY		: "empty.png",
}




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
	"crypted"	: "decrypted.png",
	"other"     : "contents.png"
}


CACHE = {}
VCACHE = {}


DATA = {
	"pack"	: "oxygen"					# набор иконок
}


def real_icon(*args):
	"""получить объект иконки по произвольному пути"""
	file_path = get_icon_path(*args)
	return PhotoImage(file=file_path)


def ticon(name):
	if name in CACHE:
		# print("in cache")
		return CACHE[name]

	if name not in ALIACES:
		name = ERROR

	pack = DATA["pack"]
	i = real_icon(pack, ALIACES[name])
	CACHE[name] = i
	return i


def ficon(name):
	if name in CACHE:
		return CACHE[name]


	if name not in F_ALIACES:
		return ticon(ERROR)

	pack = DATA["pack"]

	i = real_icon(pack, "ftypes", F_ALIACES[name])
	CACHE[name] = i
	return i





def vicon(name):
	if name in VCACHE:
		return VCACHE[name]


	if name not in VOLUME_ICONS:
		return ticon(ERROR)

	pack = DATA["pack"]

	i = real_icon(pack, "volumes", VOLUME_ICONS[name])
	VCACHE[name] = i
	return i











if __name__ == "__main__":

	from tkinter import *

	root = Tk()


	main_layout = Frame(root)
	main_layout.pack()

	row = 0
	for item in ALIACES.keys():
		Label(main_layout, image=ticon(item)).grid(row=row, column=0)
		Label(main_layout, text=item).grid(row=row, column=1)
		row += 1


	# for item in ALIACES.keys():
	# 	Label(main_layout, image=ticon(item)).grid(row=row, column=0)
	# 	Label(main_layout, text=item).grid(row=row, column=1)
	# 	row += 1


	# #-- default
	# icon = ticon(CLOSE)
	# Button(root, text="test", image=icon, command=quit, compound="left").pack()
	#
	# icon = ticon(CLOSE)
	# Button(root, text="test", image=icon, command=quit, compound="left").pack()
	#
	#
	# #-- bad name
	# icon = ticon("qqq")
	# Button(root, text="test", image=icon, command=quit, compound="left").pack()


	Button(root, text="test", command=quit).pack()





	root.mainloop()