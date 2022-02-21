import tkinter as tk
from tkinter import ttk
from sys import platform 
import os

class App:
    def __init__(self, root, sysinfo):
        self.root = root
        self.titles = ["Receiver name", "Receiver name cont.", "Receiver account number", "Value","Sender account number", "Sender name", "Sender name cont.", "Title"]
        self.additional_titles = ["Stamp, date and signature of the sender", "Stamp", "Fee", "Voucher for the sender's bank", "Voucher for the sender", "D", "T"]
        self.entries = [] # list for storing entry objects
        self.labels = [] # list for storing label objects (for translation)
        self.language_tracker = True # language flag
        self.root.title("Transfer order creator 1.0") # window title
        self.root.configure(bg='#d198b7')
        # self.root.geometry('300x300')

        if sysinfo == 'linux':
            self.sysinfo = True
        else:
            self.sysinfo = False

        if self.sysinfo:
            self.font = 'Ubuntu'
        else:
            self.font = 'Arial'

        self.start()

    def start(self):
        # maybe a scrollbar in the future?
        
        # scroll = tk.Scrollbar(self.root, orient = 'vertical')
        # scroll.pack(side = 'right', fill = 'y')

        self.title_label = tk.Label(self.root, font=(self.font,18,'bold'), text="Transfer order creator\n", bg="#d198b7", fg='#000000') #top label
        self.title_label.grid(columnspan = 2) # .pack() method used for displaying UI elements

        # migration to ttk for entries in the future?
        
        # ttk.Style().map('TEntry',
        # background = [('active','white')]
        # )

        for i in self.titles: # setting up the labels and entry bars 
            
            l = tk.Label(root, font=(self.font,16), text=i, bg='#d198b7', fg='#000000')
            self.labels.append(l)
            
            e = tk.Entry(root, bd=2, highlightcolor='#779ecb', selectbackground = '#779ecb', selectforeground = "white", relief='flat')
            self.entries.append(e)

        j = 0
        for a in range(2):
            for i in range(1,9,2):
                self.labels[j].grid(column = a, row = i)
                j += 1

        j = 0
        for a in range(2):
            for i in range(2,10,2):
                self.entries[j].grid(column = a, row = i, ipadx = 100, padx = 10)
                j += 1

            


        self.currency_dropdown()        

        self.run_button = tk.Button(
        self.root, 
        text="Run", 
        font=(self.font,16), 
        width=10, 
        command=lambda: self.transfer(), 
        bg = '#86C5DA',
        highlightcolor="#779ecb", 
        activebackground="#779ecb",
        activeforeground="white", 
        relief='flat'
        ) # run button
        self.run_button.grid(pady = 10)

        self.language_button = tk.Button(
        self.root, 
        text='Zmień język na polski', 
        font=(self.font,16),
        width=24, 
        command=lambda: self.change_language(), 
        bg = '#86C5DA',
        highlightcolor="#779ecb", 
        activebackground="#779ecb",
        activeforeground="white", 
        relief='flat'
        )
        self.language_button.grid(pady = 10, column = 1, row = 11) # translation/language button


    def currency_dropdown(self):

        # making a label for a dropdown

        l = tk.Label(root, font=(self.font,16), text="Currency", bg='#d198b7', fg='#000000')
        l.grid()
        self.labels.append(l)

        # styling (ttk is a pain)

        ttk.Style().configure('TCombobox', fieldbackground = "#E1BFFF", background = '#86C5DA', selectbackground = '#779ecb', selectforeground = "white", relief='flat', borderwidth = "0")
        ttk.Style().map('TCombobox',
        background = [('active','#779ecb'), ('pressed', '#779ecb')],
        relief = [('active', 'flat'),('pressed', 'flat')],
        arrowcolor = [('active','white'), ('pressed','white')]
        )
  
        self.root.option_add('*TCombobox*Listbox*Background', '#86C5DA')
        self.root.option_add('*TCombobox*Listbox*selectBackground', '#779ecb')
        self.root.option_add('*TCombobox*Listbox*selectForeground', 'white')

        # dropdown menu

        self.combo = ttk.Combobox(self.root)
        self.combo["values"] = ['PLN','USD','GBP']
        self.combo.current(0)
        self.combo.grid(columnspan = 2)

    def transfer(self):

        with open('transfer.tex') as g: # opening template tex file
            a = g.read()

        for i in range(8):
            a = a.replace('placeholder'+str(i), self.entries[i].get()) # creating new tex code while editing the template on "placeholder*" flag
            a = a.replace('new*placeh'+str(i), self.titles[i]) # renaming the boxes names with "new*placeh" flag
        
        for i in range(7):
            a = a.replace('additional*plch'+str(i), self.additional_titles[i]) # changing the constant boxes names
        
        for i in range(2):
            a = a.replace('currplaceh'+str(i), self.combo.get().upper() ) # changing the currency

        with open('newtransfer.tex', 'w') as f: # creating new tex file
            f.write(a)


        os.system("pdflatex newtransfer.tex") # compiling tex file to pdf

        if self.sysinfo:
            os.system("evince newtransfer.pdf")  # to display the document in GNOME document viewer (should be altered on windows or other)
        else:
            os.system("newtransfer.pdf") # same for windows

        self.temp_files_collector() # removing pdflatex's log and aux files

    def temp_files_collector(self): # collecting pdflatex's temporary files (tex, log, aux) - optional functionality

        if self.sysinfo:    
            os.system("rm -rf newtransfer.aux newtransfer.log newtransfer.tex") 
        else:
            os.system('del "newtransfer.aux" "newtransfer.log" "newtransfer.tex" ')

    def change_language(self): # translating method 

        if self.language_tracker:
            self.titles = ["Nazwa odbiorcy","Nazwa odbiorcy cd.","Nr rachunku odbiorcy","Kwota","Nr rachunku zleceniodawcy","Nazwa zleceniodawcy","Nazwa zleceniodawcy cd.","Tytuł", "Waluta"]
            self.additional_titles = ["Pieczęć, data i podpis zleceniodawcy", "Pieczęć", "Opłata", "Odcinek dla banku zleceniodawcy", "Odcinek dla zleceniodawcy", "W", "P"]
            self.root.title("Kreator poleceń przelewu 1.0")
            self.title_label.configure(text = "Kreator polecenia przelewu\n")
            self.language_button.configure(text = "Change language to english")
            self.run_button.config(text='Wykonaj')
            self.language_tracker = False

        else:
            self.titles = ["Receiver name", "Receiver name cont.", "Receiver account number", "Value","Sender account number", "Sender name", "Sender name cont.", "Title", "Currency"]
            self.additional_titles = ["Stamp, date and signature of the sender", "Stamp", "Fee", "Voucher for the sender's bank", "Voucher for the sender", "D", "T"]
            self.root.title("Transfer order creator 1.0")
            self.title_label.configure(text = "Transfer order creator\n")
            self.language_button.configure(text = "Zmień język na polski")
            self.run_button.config(text='Run')
            self.language_tracker = True

        a = 0
        for i in self.labels: # renaming labels
            i.configure(text=self.titles[a])
            a += 1


root = tk.Tk()
app = App(root, platform)
root.mainloop()