#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import json, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def Help():
    # Message box of keybind info
    messagebox.showinfo("Keybinds", "ctrl + s : Save\n" "ctrl + n : New File\n" "ctrl + e : Exit\n")

def deleteFile():
    # grab filename
    fileName = name.get().strip()
    # does path exist
    path = os.path.join(BASE_DIR, f"data/notes/files/{fileName}.json")
    bakpath = os.path.join(BASE_DIR, f"data/notes/bak/{fileName}.bak")
    
    # Ask user if they are sure to make a new file
    result = messagebox.askyesno("Are you Sure?", "Are you sure you want to make to delete this file", detail="This will be saved in a backup!", icon="info", default="no")
    # if yes, delete all entries and texts
    if result:
        name.delete(0, tk.END)
        desc.delete("1.0", tk.END)
        text.delete("1.0", tk.END)
        
        try:
            with open(path, "r") as f: data = f.readlines()
            for i in data:
                with open(bakpath, "a") as f: f.write(i)
        except FileNotFoundError:
            messagebox.showerror("Error", "File Not Found\n\n Be sure you have opened a file that exists, not the base one")
        except Exception as e:
            messagebox.showerror("Error", "An Exception Occured", detail=e)
            
        os.remove(path)
        
    # if no, return
    else:
        return
        

def OpenFile():
    top = tk.Toplevel()
    top.title("Notes Files")
    
    label = tk.Label(top, text="Double click on files below to open them")
    label.grid(row=0, column=0)

    # Create Treeview
    tree = ttk.Treeview(top, columns=("Title", "Size"), show="headings")
    tree.heading("Title", text="Title")
    tree.heading("Size", text="Size (KB)")
    tree.column("Title", width=250)
    tree.column("Size", width=100, anchor="center")
    tree.grid(row=1, column=0)

    path = os.path.join(BASE_DIR, "data/notes/files")
    if not os.path.exists(path):
        os.makedirs(path)

    # Populate Treeview
    for fname in os.listdir(path):
        if fname.endswith(".json"):
            fpath = os.path.join(path, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                title = data.get("title", fname)
                size_mb = os.path.getsize(fpath) / (1024)
                tree.insert("", "end", values=(title, f"{size_mb:.2f}"))
            except Exception as e:
                print(f"Failed to load {fname}: {e}")

    def onOpen(event):
        result = messagebox.askyesno("Are you Sure?", "Are you sure you want to open this file", detail="Any unsaved data will be lost!", icon="info", default="no")
        if result:
            # clean texts and entries
            name.delete(0, tk.END)
            desc.delete("1.0", tk.END)
            text.delete("1.0", tk.END)     
                   
            item = tree.selection()
            if item:
                values = tree.item(item, "values")
                file_title = values[0]
                # Find the file by title
                for fname in os.listdir(path):
                    if fname.endswith(".json"):
                        fpath = os.path.join(path, fname)
                        with open(fpath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        if data.get("title") == file_title:
                            # insert data to texts and entries
                            aTITLE = data["title"]
                            name.insert(0, aTITLE)
                            aDESC = data["desc"]
                            for i in aDESC:
                                desc.insert(tk.END, i)
                            aTEXT = data["text"]
                            for i in aTEXT:
                                text.insert(tk.END, i)
                            break
            top.destroy()
        else:
            top.destroy()
            return

    tree.bind("<Double-Button-1>", onOpen)

def newFile():
    # Ask user if they are sure to make a new file
    result = messagebox.askyesno("Are you Sure?", "Are you sure you want to make a new file", detail="Any unsaved data will be lost!", icon="info", default="no")
    # if yes, delete all entries and texts
    if result:
        name.delete(0, tk.END)
        desc.delete("1.0", tk.END)
        text.delete("1.0", tk.END)
    # if no, return
    else:
        return

def save():
    # grab filename
    fileName = name.get().strip()
    # does path exist
    path = os.path.join(BASE_DIR, f"data/notes/files/{fileName}.json")

    # data points
    data = {
        "title": "",
        "desc": "",
        "text": []
    }

    # If file exists, load it first
    if os.path.isfile(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

    # Update data from Tkinter entries
    data["title"] = fileName
    data["desc"] = desc.get("1.0", "end-1c")
    textspre = text.get("1.0", "end-1c").splitlines()
    texts=[]
    for i in texts:
        texts.append(i+"\n")
    data["text"] = texts
    

    # Make sure directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Save file (overwrites or creates)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    messagebox.showinfo("Saved!", "Saved!")
    
version = 1.0
build = "2.10.2026"

icon_path = os.path.join(BASE_DIR, "Assets/notes/NoteLogo.png")

# window ini
root = tk.Tk()
root.update()
root.title("Notes")
root.geometry("480x320")
root.attributes("-fullscreen", True)
icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

root.bind("<Control-e>", lambda e: root.destroy())
root.bind("<Control-n>", lambda e: newFile())
root.bind("<Control-s>", lambda e: save())
root.bind("<Control-h>", lambda e: Help())

# window structure
panes = tk.PanedWindow(root, orient=tk.HORIZONTAL)
panes.grid(row=0, column=0, sticky="nsew")

# Sidebar frame
side = tk.Frame(panes, width=80)
side.pack_propagate(False)
side.columnconfigure(0, weight=1)
side.rowconfigure(4, weight=1)
side.config(bg="#aaaaaa")

# main text frame
main = tk.Frame(panes)
main.config(bg="#aaaaaa")

# add panes
panes.add(side)
panes.add(main)

topFrame = tk.Frame(side, bg="#aaaaaa")
topFrame.grid(row=0, column=0, sticky="new")
topFrame.columnconfigure(0, weight=1)

new = tk.Button(topFrame, text="New", bg="#aaaaaa", width=14, command=newFile)
new.grid(row=0, column=0, sticky="w", padx=3, pady=3)

more = tk.Menubutton(topFrame, text="+", bg="#aaaaaa", relief="raised")
more.grid(row=0, column=1, sticky="e", padx=3, pady=3)

# dropdown menu
menu = tk.Menu(more, tearoff=0)
menu.add_command(label="Save", command=save)
menu.add_separator()
menu.add_command(label="Open", command=OpenFile)
menu.add_command(label="New", command=newFile)
menu.add_command(label="Delete", command=deleteFile)
menu.add_separator()
menu.add_command(label="Help", command=Help)
menu.add_separator()
menu.add_command(label="Close", command=root.destroy)
more.config(menu=menu)

nameFrame = tk.LabelFrame(side, text="Name", bg="#aaaaaa")
nameFrame.grid(row=1, column=0, sticky="new", padx=2, pady=2)

name = tk.Entry(nameFrame)
name.grid(row=0, column=0, padx=3, pady=3)
name.insert(0, "Lorem Ipsum")

descLabel = tk.Label(side, text=f"Description", bg="#aaaaaa")
descLabel.grid(row=2, column=0, sticky="w")

desc = tk.Text(side, width=16, height=4, font=("Arial"))
desc.grid(row=3, column=0, padx=3, pady=3)

# version and build

appData = tk.Frame(side, bg="#aaaaaa")
appData.grid(row=4, column=0, sticky="nsew")
appData.rowconfigure(0, weight=1)

v = tk.Label(appData, text=f"v{version}", bg="#aaaaaa", fg="#747474")
v.grid(row=0, column=0, sticky="ws")

b = tk.Label(appData, text=f"b{build}", bg="#aaaaaa", fg="#747474")
b.grid(row=1, column=0, sticky="ws")

# main textbox
text = tk.Text(main, font=("Arial"))
text.grid(row=0, column=0, sticky="news")

scrollbar = tk.Scrollbar(root, command=text.yview)
scrollbar.grid(row=0, column=1, sticky="nes")
text.config(yscrollcommand=scrollbar.set)


root.mainloop()
