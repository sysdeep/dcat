#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

# from app.rc import ABOUT_NAME, ABOUT_AUTHOR_EMAIL, ABOUT_AUTHOR_NAME, ABOUT_DESCRIPTION, ABOUT_SLUG, VERSION
from ..utils import aqicon
from app.data import VOLUME_TYPE
from app.storage import get_storage
#
# class IRow(object):
# 	def __init__(self, parent, name, sname):
# 		self.parent = parent
# 		self.name = name
# 		self.sname = sname
#
# 		lkey_text = self.sname + ": "
# 		self.lkey = ttk.Label(self.parent, text=lkey_text)
# 		self.vkey = ttk.Label(self.parent, text="")
#
# 	def update(self, value):
# 		self.vkey.config(text=value)






class EditVolume(tkinter.Toplevel):
	def __init__(self, vnode, master=None, *args, **kwargs):
		super(EditVolume, self).__init__(master, *args, **kwargs)
		self.title("Редактирование тома")

		self.maxsize(400, 300)
		self.minsize(400, 300)

		self.vnode = vnode
		self.vtype = None
		self.storage = get_storage()


		self.main_frame = tkinter.Frame(self,)
		self.main_frame.pack(expand=True, fill="both", side="top", padx=10, pady=20)


		edit_frame = ttk.Frame(self.main_frame)
		edit_frame.pack(fill="x", side="top", padx=10, pady=10)

		row = 0
		ttk.Label(edit_frame, text="Название тома: ").grid(row=row, column=0, sticky="e")
		self.volume_name_entry = tkinter.Entry(edit_frame, width=30, justify="left")
		self.volume_name_entry.grid(row=row, column=1, sticky="w")

		row += 1
		ttk.Label(edit_frame, text="Иконка: ").grid(row=row, column=0, sticky="e")
		self.volume_type_box = ttk.Combobox(edit_frame, values=VOLUME_TYPE, state='readonly')
		self.volume_type_box.grid(row=row, column=1, sticky="w")
		self.volume_type_box.bind('<<ComboboxSelected>>', self.__update_volume_vtype)



		self.description = tkinter.Text(self.main_frame, height=10, width=40)
		self.description.pack(side="top", fill="both", expand=True)


		#--- controls
		controls_frame = tkinter.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		self.icon_close = aqicon("close")
		self.icon_save = aqicon("save")

		tkinter.Button(controls_frame, text="Сохранить", command=self.__do_save, image=self.icon_save, compound="left").pack(side="left")
		tkinter.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())




		self.__init_data()


	def __init_data(self):
		self.volume_name_entry.insert(0, self.vnode.name)
		self.vtype = self.vnode.vtype
		self.volume_type_box.set(self.vtype)
		if self.vnode.description:
			self.description.insert(tkinter.END, self.vnode.description)


	def __update_volume_vtype(self, e):
		self.vtype = self.volume_type_box.get()


	def __do_save(self):
		name = self.volume_name_entry.get()
		name.strip()

		if len(name) == 0:
			return False

		self.vnode.name = name
		self.vnode.vtype = self.vtype
		self.vnode.description = self.description.get(1.0, tkinter.END)


		row = {
			"uuid"			: self.vnode.uuid,
			"name"			: name,
			"vtype"			: self.vtype,
			"description"	: self.vnode.description
		}

		self.storage.update_volume_row(row, commit=True)
		self.destroy()






if __name__ == "__main__":


	root = tkinter.Tk()

	modal = EditVolume(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()