import tkinter as tk
from tkinter import ttk
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(BASE_DIR, "Assets/notes/NoteLogo.png")

root = tk.Tk()
root.title("Notes")
root.geometry("320x240")
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

panes = tk.PanedWindow(root, orient=tk.HORIZONTAL)
panes.grid(row=0, column=0, sticky="nsew")

side = tk.Frame(panes, width=80)
side.pack_propagate(False)
side.columnconfigure(0, weight=1)
side.config(bg="#aaaaaa")
main = tk.Frame(panes)
main.config(bg="#aaaaaa")

panes.add(side)
panes.add(main)



topFrame = tk.Frame(side, bg="#aaaaaa")
topFrame.grid(row=0, column=0, sticky="new")
topFrame.columnconfigure(0, weight=1)

new = tk.Button(topFrame, text="New", bg="#aaaaaa", width=14)
new.grid(row=0, column=0, sticky="w", padx=3, pady=3)

more = tk.Menubutton(topFrame, text="+", bg="#aaaaaa", relief="raised")
more.grid(row=0, column=1, sticky="e", padx=3, pady=3)

menu = tk.Menu(more, tearoff=0)
menu.add_command(label="Open")
menu.add_command(label="Delete")
menu.add_separator()
menu.add_command(label="Close", command=root.destroy)
more.config(menu=menu)

nameFrame = tk.LabelFrame(side, text="Name", bg="#aaaaaa")
nameFrame.grid(row=1, column=0, sticky="new", padx=2, pady=2)

name = tk.Entry(nameFrame)
name.grid(row=0, column=0, padx=3, pady=3)
name.insert(0, "Lorem Ipsum")

desc = tk.Text(side, width=16, height=3)
desc.grid(row=2, column=0, padx=3, pady=3, sticky="w")

text = tk.Text(main)
text.grid(row=0, column=0, sticky="news")


root.mainloop()