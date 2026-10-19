from tkinter import ttk, font

from app.lib.user_settings import UpdateUserSettingsModel


class FrameStyle(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super(FrameStyle, self).__init__(master, *args, **kwargs)

        self.config(padding=10)

        style = ttk.Style()
        # self.tk.eval("source themes/pkgIndex.tcl")
        # self.tk.call("package", "require", "ttkthemes")
        # print(style.theme_names())
        # print(style.theme_use())
        # style.theme_use("clam")
        # style.configure('TButton', foreground='green')

        styles = style.theme_names()
        self._initial_style = style.theme_use()
        self.style_box = ttk.Combobox(self, values=styles, state="readonly")
        self.style_box.pack(side="left")
        self.style_box.bind("<<ComboboxSelected>>", self.__update_style)
        self.style_box.set(self._initial_style)

    def __update_style(self, e):
        new_style = self.style_box.get()
        style = ttk.Style()
        style.theme_use(new_style)

    def apply_changes(self, model: UpdateUserSettingsModel):
        style = ttk.Style()
        used_style = style.theme_use()

        if used_style != self._initial_style:
            model.ttk_theme = used_style
