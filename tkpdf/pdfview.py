import threading
import tkinter as tk
from tkinter import ttk
from typing import Any

import fitz


class PdfView(ttk.Frame):
    def __init__(self, master: tk.Misc = None, file: str = None) -> None:
        ttk.Frame.__init__(self, master)

        self._file = file
        self._image_list = []  # To avoid garbage collection

        self.text = tk.Text(self)
        self.text.grid(row=0, column=0, sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.horizontal_scroll = ttk.Scrollbar(
            self, orient="horizontal", command=self.text.xview
        )
        self.vertical_scroll = ttk.Scrollbar(
            self, orient="vertical", command=self.text.yview
        )
        self.text.configure(
            xscrollcommand=self.horizontal_scroll.set,
            yscrollcommand=self.vertical_scroll.set,
        )

        self.horizontal_scroll.grid(row=1, column=0, sticky="ew")
        self.vertical_scroll.grid(row=0, column=1, sticky="ns")

        threading.Thread(target=self.add_images).start()

    def add_images(self) -> None:
        pdf = fitz.open(self._file)

        for page in pdf:
            pixmap = page.getPixmap()
            data = pixmap.getImageData("gif")
            image = tk.PhotoImage(data=data)

            self._image_list.append(image)
            self.text.image_create("end", image=image)
            self.text.insert("end", "\n\n")

        self.text.delete("end - 2 line", "end")
        self.text.configure(state="disabled")

    def __setitem__(self, key: str, value: Any) -> None:
        self.configure(**{key: value})

    def __getitem__(self, key: str):
        return self.cget(key)

    def __repr__(self) -> str:
        name = f"{type(self).__module__}.{type(self).__name__}"

        if not self.winfo_exists():
            return f"<destroyed {name}>"

        return f"<{name} widget, pdf file: {self._file}>"

    def keys(self) -> list:
        keys = self.text.keys()
        keys.append("file")
        return sorted(keys)

    def cget(self, key: str) -> Any:
        if key == "file":
            return self._file
        else:
            return tk.Text.cget(self, key)

    def configure(self, **kwargs) -> None:
        file = kwargs.pop("file", None)
        if file:
            self.text.delete("1.0", "end")
            threading.Thread(target=self.add_images).start()
        self.text.configure(self, **kwargs)

    config = configure
