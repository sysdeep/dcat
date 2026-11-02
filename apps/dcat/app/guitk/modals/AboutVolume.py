import tkinter
from tkinter import ttk


from app.data import VOLUME_TYPE
from app.storage import Storage
from app.lib.fsize import naturalsize

from ..utils import ticons


class AboutVolume(tkinter.Toplevel):
    """AboutVolume - модал информации о томе + редактор"""

    def __init__(self, vnode, storage: Storage, master):
        super().__init__(master)
        self._vnode = vnode
        self._storage = storage

        self.title("Свойства тома")
        self.minsize(450, 350)

        self.vtype = None

        self._main_frame = ttk.Frame(self, padding=10)
        self._main_frame.pack(expand=True, fill="both", side="top")

        edit_frame = ttk.Frame(self._main_frame)
        edit_frame.pack(fill="x", side="top", padx=10, pady=10)

        row = 0
        ttk.Label(edit_frame, text="Название тома: ").grid(row=row, column=0, sticky="e", pady=2, padx=5)
        self._volume_name_entry = tkinter.Entry(edit_frame, width=30, justify="left")
        self._volume_name_entry.grid(row=row, column=1, sticky="w", pady=2, padx=5)

        row += 1
        ttk.Label(edit_frame, text="Иконка: ").grid(row=row, column=0, sticky="e", pady=2, padx=5)

        frame_icon = ttk.Frame(edit_frame)
        frame_icon.grid(row=row, column=1, sticky="w", pady=2, padx=5)

        self._volume_type_box = ttk.Combobox(frame_icon, values=VOLUME_TYPE, state="readonly")
        self._volume_type_box.pack(side="left")
        self._volume_type_box.bind("<<ComboboxSelected>>", self.__update_volume_vtype)

        self.__label_vtype_icon = ttk.Label(frame_icon, text="icon")
        self.__label_vtype_icon.pack(side="left", padx=10)
        self.__vtype_icon = None

        row += 1
        ttk.Label(edit_frame, text="Создание").grid(row=row, column=0, sticky="e", pady=2, padx=5)
        self.__label_created = ttk.Label(edit_frame)
        self.__label_created.grid(row=row, column=1, sticky="w", pady=2, padx=5)

        row += 1
        ttk.Label(edit_frame, text="Обновление").grid(row=row, column=0, sticky="e", pady=2, padx=5)
        self.__label_updated = ttk.Label(edit_frame)
        self.__label_updated.grid(row=row, column=1, sticky="w", pady=2, padx=5)

        row += 1
        ttk.Label(edit_frame, text="Путь").grid(row=row, column=0, sticky="e", pady=2, padx=5)
        self.__label_path = ttk.Label(edit_frame)
        self.__label_path.grid(row=row, column=1, sticky="w", pady=2, padx=5)

        row += 1
        ttk.Label(edit_frame, text="Кол-во элементов").grid(row=row, column=0, sticky="e", pady=2, padx=5)
        self.__label_elements_count = ttk.Label(edit_frame)
        self.__label_elements_count.grid(row=row, column=1, sticky="w", pady=2, padx=5)

        row += 1
        ttk.Label(edit_frame, text="Размер всех элементов").grid(row=row, column=0, sticky="e", pady=2, padx=5)
        self._label_elements_size = ttk.Label(edit_frame)
        self._label_elements_size.grid(row=row, column=1, sticky="w", pady=2, padx=5)

        # --- edit description field
        frame_description = ttk.Frame(self._main_frame, padding=5)
        frame_description.pack(side="top", expand=True, fill="both")

        ttk.Label(frame_description, text="описание").pack(fill="x", side="top")
        self._description = tkinter.Text(frame_description, height=6, width=20)
        self._description.pack(side="left", fill="both", expand=True)

        # - vertical scroll
        ysb = ttk.Scrollbar(frame_description, orient="vertical", command=self._description.yview)
        self._description["yscroll"] = ysb.set
        ysb.pack(side="right", expand=False, fill="y")

        # self.description = tkinter.Text(self.main_frame, height=6, width=20)
        # self.description.pack(side="top", fill="both", expand=True)

        # --- controls
        controls_frame = ttk.Frame(self._main_frame)
        controls_frame.pack(fill="both", side="bottom", padx=5, pady=5)

        ttk.Button(
            controls_frame, text="Сохранить", command=self.__do_save, image=ticons.ticon(ticons.SAVE), compound="left"
        ).pack(side="left")
        ttk.Button(
            controls_frame,
            text="Закрыть(Ctrl+w)",
            command=self.destroy,
            image=ticons.ticon(ticons.CLOSE),
            compound="left",
        ).pack(side="right")

        self.bind_all("<Control-w>", lambda e: self.destroy())

        self.__init_data()

    def __init_data(self):
        self._volume_name_entry.insert(0, self._vnode.name)
        self.vtype = self._vnode.vtype
        self._volume_type_box.set(self.vtype)
        self.__update_volume_icon()
        if self._vnode.description:
            self._description.insert(tkinter.END, self._vnode.description)

        self.__label_created.config(text=self._vnode.created)
        self.__label_updated.config(text=self._vnode.updated)
        self.__label_path.config(text=self._vnode.path)

        elements_count = self._storage.get_volume_elements_count(self._vnode)
        self.__label_elements_count.config(text=str(elements_count))

        elements_size = self._storage.get_volume_elements_size(self._vnode)
        self._label_elements_size.config(text=naturalsize(elements_size))

    def __update_volume_vtype(self, e):
        self.vtype = self._volume_type_box.get()
        self.__update_volume_icon()

    def __update_volume_icon(self) -> None:
        # self.__vtype_icon = volume_icon(self.vtype)
        self.__vtype_icon = ticons.vicon(self.vtype)
        self.__label_vtype_icon.config(image=self.__vtype_icon)

    def __do_save(self) -> None:
        name = self._volume_name_entry.get()
        name.strip()

        if len(name) == 0:
            return

        self._vnode.name = name
        self._vnode.vtype = self.vtype
        self._vnode.description = self._description.get(1.0, tkinter.END)

        # TODO: use dataclass
        row = {"uuid": self._vnode.uuid, "name": name, "vtype": self.vtype, "description": self._vnode.description}

        self._storage.update_volume_row(row, commit=True)
        # self.destroy()


# if __name__ == "__main__":
#     root = tkinter.Tk()

#     modal = AboutVolume(root)
#     ttk.Button(root, text="quit", command=quit).pack()

#     root.mainloop()
