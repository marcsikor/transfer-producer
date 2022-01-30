import tkinter as tk
# from tkinter import ttk
import os


def dialog_bar(string,entries): # function for creating editable fields
    
    tk.Label(root, font=40, text=string, bg='#343434', fg = '#ffffff').pack()
    
    e = tk.Entry(root, bg = "#E1BFFF")

    e.pack(ipadx = 100)

    entries.append(e)

def temp_files_collector():
    os.system("rm -rf newtransfer.aux newtransfer.log newtransfer.tex") # collecting pdflatex's temporary files (tex, log, aux) - optional functionality

def transfer(tab): 

    with open('transfer.tex') as g: # opening template tex file
        a = g.read()

    for i in range(8):
        a = a.replace('placeholder'+str(i), tab[i].get()) # creating new tex code while editing the template on "placeholder*" flags

    with open('newtransfer.tex', 'w') as f: # creating new tex file
        f.write(a)

    os.system("pdflatex newtransfer.tex") # compiling tex file to pdf

    os.system("evince newtransfer.pdf")  # to display the document in GNOME document viewer (should be altered on windows)

    temp_files_collector() # removing pdflatex's log and aux files


# main program

root = tk.Tk()
root.title("Przelewy 0.9.1")

root.configure(bg='#343434')

tk.Label(root, font=50, text="Program do autouzupełniania druku do przelewu\n", bg="#343434", fg='#ffffff').pack()

titles = ["Nazwa odbiorcy","Nazwa odbiorcy cd.","Nr rachunku odbiorcy","Kwota","Nr rachunku zleceniodawcy","Nazwa zleceniodawcy","Nazwa zleceniodawcy cd.","Tytuł"] # table of polish field names

entries = [] # table for storing tkinter objects

for i in titles:
    dialog_bar(i,entries) # loop for creating fields

tk.Button(root, text="Wykonaj", font=40, width=10, command=lambda: transfer(entries), bg = '#FFE8B3' ).pack(pady = 10) # run button

root.mainloop()
