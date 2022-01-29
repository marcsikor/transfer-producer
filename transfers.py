#!/usr/bin/env python3

import tkinter as tk
import os


def dialog_bar(string,entries):
    
    tk.Label(root, font=40, text=string).pack()
    
    e = tk.Entry(root)

    e.pack()

    entries.append(e)

def temp_files_collector():
    os.system("rm -rf newtransfer.aux newtransfer.log newtransfer.tex")

def transfer(tab):

    with open('transfer.tex') as g:
        a = g.read()

    for i in range(8):
        a = a.replace('placeholder'+str(i), tab[i].get())

    with open('newtransfer.tex', 'w') as f:
        f.write(a)

    os.system("pdflatex newtransfer.tex")

    temp_files_collector()


root = tk.Tk()
root.title("Przelewy 0.9.1")

tk.Label(root, font=50, text="Program do autouzupełniania druku do przelewu\n").pack()

titles = ["Nazwa odbiorcy","Nazwa odbiorcy cd.","Nr rachunku odbiorcy","Kwota","Nr rachunku zleceniodawcy","Nazwa zleceniodawcy","Nazwa zleceniodawcy cd.","Tytuł"]

entries = []

for i in titles:
    dialog_bar(i,entries)

tk.Button(
    root, text="Wykonaj", font=40, width=10, command=lambda: transfer(entries)
).pack()

root.mainloop()
