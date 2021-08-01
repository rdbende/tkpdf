import tkinter as tk
from tkinter import ttk

import tkpdf

root = tk.Tk()

pdf_view = tkpdf.PdfView(root, file="something.pdf")
pdf_view.pack(fill="both", expand=True)

root.mainloop()
