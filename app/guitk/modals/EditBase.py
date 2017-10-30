#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

from ..utils import aqicon
from app.data import VOLUME_TYPE
from app.storage import get_storage
from ..utils.icons import volume_icon






class EditBase(tkinter.Toplevel):
	def __init__(self, master=None, *args, **kwargs):
		super(EditBase, self).__init__(master, *args, **kwargs)
		self.title("Редактирование базы")

		self.maxsize(450, 300)
		self.minsize(450, 300)

		self.storage = get_storage()


		self.main_frame = ttk.Frame(self, padding=10)
		self.main_frame.pack(expand=True, fill="both", side="top")



		self.description = tkinter.Text(self.main_frame, height=6, width=20)
		self.description.pack(side="top", fill="both", expand=True)


		#--- controls
		controls_frame = ttk.Frame(self.main_frame)
		controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

		self.icon_close = aqicon("close")
		self.icon_save = aqicon("save")

		ttk.Button(controls_frame, text="Сохранить", command=self.__do_save, image=self.icon_save, compound="left").pack(side="left")
		ttk.Button(controls_frame, text="Закрыть(Ctrl+w)", command=self.destroy, image=self.icon_close, compound="left").pack(side="right")

		self.bind_all("<Control-w>", lambda e: self.destroy())




		self.__init_data()


	def __init_data(self):
		description = "not found in db"
		sys_info = self.storage.fetch_system()
		for row in sys_info:
			if row["key"] == "description":
				description = row["value"]



		self.description.insert(tkinter.END, description)


	def __do_save(self):

		description = self.description.get(1.0, tkinter.END)


		self.storage.update_system("description", description)
		self.storage.commit()





if __name__ == "__main__":


	root = tkinter.Tk()

	modal = EditBase(root)
	ttk.Button(root, text="quit", command=quit).pack()

	root.mainloop()