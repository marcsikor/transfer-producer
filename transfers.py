import tkinter as tk
from tkinter import ttk
from sys import platform 
import os
import subprocess
import shlex

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
        self.dark_mode_flag = True
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

        self.title_label = tk.Label(self.root, font=(self.font,18,'bold'), text="Transfer order creator\n", bg="#d198b7", fg='#000000') #top label
        self.title_label.grid(columnspan = 2) # .pack() method used for displaying UI elements

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
        self.run_button.grid(columnspan = 2, pady = 10)

        self.menu()

    def currency_dropdown(self):

        # making a label for a dropdown

        l = tk.Label(root, font=(self.font,16), text="Currency", bg='#d198b7', fg='#000000')
        l.grid(columnspan = 2, pady = 10)
        self.labels.append(l)

        # styling (ttk is a pain)

        ttk.Style().configure('TCombobox', fieldbackground = "#86C5DA", background = '#86C5DA', selectbackground = '#779ecb', selectforeground = "white", relief='flat', borderwidth = "0")
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

        
        status = subprocess.call('pdflatex newtransfer.tex', shell=True) # compiling tex file to pdf
        if status != 0:
            
            if self.language_tracker:
                self.error("An error occured during LaTeX compilation.\nPlease check whether LaTeX and pdflatex are installed.")
            else:
                self.error("Wystąpił błąd podczas kompilacji LaTeX.\nProszę sprawdzić, czy LaTeX i pdflatex są zainstalowane.")
            return 1

        if self.sysinfo:
            subprocess.call("evince newtransfer.pdf", shell=True)  # to display the document in GNOME document viewer (should be altered on windows or other)
        else:
            subprocess.call("newtransfer.pdf") # same for windows

        self.temp_files_collector() # removing pdflatex's log and aux files

    def temp_files_collector(self): # collecting pdflatex's temporary files (tex, log, aux) - optional functionality

        if self.sysinfo:    
            subprocess.call("rm -rf newtransfer.aux newtransfer.log newtransfer.tex", shell=True) 
        else:
            subprocess.call('del "newtransfer.aux" "newtransfer.log" "newtransfer.tex" ')

    def change_language(self): # translating method 

        if self.language_tracker:
            self.titles = ["Nazwa odbiorcy","Nazwa odbiorcy cd.","Nr rachunku odbiorcy","Kwota","Nr rachunku zleceniodawcy","Nazwa zleceniodawcy","Nazwa zleceniodawcy cd.","Tytuł", "Waluta"]
            self.additional_titles = ["Pieczęć, data i podpis zleceniodawcy", "Pieczęć", "Opłata", "Odcinek dla banku zleceniodawcy", "Odcinek dla zleceniodawcy", "W", "P"]
            self.root.title("Kreator poleceń przelewu 1.0")
            self.title_label.configure(text = "Kreator polecenia przelewu\n")
            # self.language_button.configure(text = "Change language to english")
            self.run_button.config(text='Wykonaj')
            self.filemenu.entryconfig(0, label = "Change language to english")
            self.filemenu.entryconfig(1, label = "Tryb ciemny")
            self.filemenu.entryconfig(2, label = "Wyjście")

            save_names = ["Zapisz bieżącego odbiorcę", "Zapisz bieżącego nadawcę", "Odbiorcy", "Nadawcy"]

            for i in range(4):
                self.saved.entryconfig(i, label = save_names[i])

            self.language_tracker = False

        else:
            self.titles = ["Receiver name", "Receiver name cont.", "Receiver account number", "Value","Sender account number", "Sender name", "Sender name cont.", "Title", "Currency"]
            self.additional_titles = ["Stamp, date and signature of the sender", "Stamp", "Fee", "Voucher for the sender's bank", "Voucher for the sender", "D", "T"]
            self.root.title("Transfer order creator 1.0")
            self.title_label.configure(text = "Transfer order creator\n")
            # self.language_button.configure(text = "Zmień język na polski")
            self.run_button.config(text='Run')
            self.filemenu.entryconfig(0, label = "Zmień język na polski")
            self.filemenu.entryconfig(1, label = "Dark mode")
            self.filemenu.entryconfig(2, label = "Exit")
            
            save_names = ["Save current receiver", "Save current sender", "Receivers", "Senders"]

            for i in range(4):
                self.saved.entryconfig(i, label = save_names[i])

            
            self.language_tracker = True

        a = 0
        for i in self.labels: # renaming labels
            i.configure(text=self.titles[a])
            a += 1

    def dark_mode(self):

        if self.dark_mode_flag:
          
            self.root.configure(bg = '#212121' )
            for i in self.labels: # renaming labels
                i.configure(bg = '#212121', fg='#aaaaaa')
            for i in self.entries:
                i.configure(bg = '#3d3d3d', fg='#aaaaaa')
            self.title_label.configure(bg = '#212121', fg='#aaaaaa')
            self.dark_mode_flag = False

        else:
            
            self.root.configure(bg = '#d198b7' )
            for i in self.labels: # renaming labels
                i.configure(bg = '#d198b7', fg='#000000')
            for i in self.entries:
                i.configure(bg = '#ffffff', fg='#000000')
            self.title_label.configure(bg = '#d198b7', fg='#000000')
            self.dark_mode_flag = True
        

    def menu(self):

        import csv

        menubar = tk.Menu(root, bg = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white")

        self.filemenu = tk.Menu(menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white" )
        self.saved = tk.Menu(menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white" )

        menubar.config(font = self.font)
        
        self.filemenu.config(font = self.font)
        self.saved.config(font = self.font)

        self.filemenu.add_command(label="Zmień język na polski", command=self.change_language)
        self.filemenu.add_command(label="Dark mode", command=self.dark_mode)
        self.filemenu.add_command(label="Exit", command=root.quit)

        self.saved.add_command(label="Save current receiver", command=lambda: self.save_csv(True))
        self.saved.add_command(label="Save current sender", command=lambda: self.save_csv(False))

        saved_rece = tk.Menu(menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white")
        saved_send = tk.Menu(menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white")

        try:
            f = open('receivers.csv')
            reader = list(csv.reader(f))

            for i in reader:
                saved_rece.add_command(label = i[0], command=lambda i=i: self.fill(i, True))
            
            f.close()
        except:
            pass

        try:

            f = open('senders.csv')
            reader = list(csv.reader(f))

            for i in reader:
                saved_send.add_command(label = i[0], command=lambda i=i: self.fill(i, False))
                    
            f.close()
                
        except:
            pass

        menubar.add_cascade(label="Options", menu=self.filemenu)
        menubar.add_cascade(label="Saved", menu=self.saved)

        self.saved.add_cascade(label="Receivers", menu=saved_rece)
        self.saved.add_cascade(label="Senders", menu=saved_send)
        
        self.root.config(menu=menubar)

    def save_csv(self, test):

        if test:
            if self.language_tracker:
                name = 'receiver'
            else:
                name = 'odbiorcy'
            index = [0,1,2]
        
        else:
            if self.language_tracker:
                name = 'sender'
            else:
                name = 'nadawcy'
            index = [4,5,6]
        
        top = tk.Toplevel(self.root)
        top.configure(bg='#d198b7')
        if self.language_tracker:
            top.title('Saving')
            tk.Label(top, text = f"Enter {name}'s identification code\n Please restart the program in order to view changes", padx = 10, pady = 20, bg='#d198b7').pack()
        else:
            top.title('Zapisywanie')
            tk.Label(top, text = f"Wpisz kod identyfikacyjny {name}\n Zrestartuj program, aby zobaczyć zmiany", padx = 10, pady = 20, bg='#d198b7').pack()

        e = tk.Entry(top)
        e.pack()

        tk.Button(
        top, 
        text="Save", 
        font=(self.font,16), 
        width=10, 
        command=lambda: self.sub_save(e.get(),index, name, top), 
        bg = '#86C5DA',
        highlightcolor="#779ecb", 
        activebackground="#779ecb",
        activeforeground="white", 
        relief='flat'
        ).pack()
        
    def sub_save(self, value, index, name,top):

        if value == '':

            if self.language_tracker:
                self.error(f"Enter {name}'s identification code")
            else:
                self.error(f"Wpisz kod identyfikacyjny {name}")

            return 1

        else:

            a = value.upper()

            for i in index:
                a += f",{self.entries[i].get()}"

            with open(f'{name}s.csv', 'a') as f:
                f.write(a+"\n")

        top.destroy()

    def fill(self, line, test):

        if test:
            for i in range(3):
                self.entries[i].delete(0,'end')
                self.entries[i].insert(0,line[i+1])

        else:

            for i in range(3):
                self.entries[i+4].delete(0,'end')
                self.entries[i+4].insert(0,line[i+1])

    def error(self,text):

        top = tk.Toplevel(self.root)
        if self.language_tracker:
            top.title('Error')
        else:
            top.title('Błąd')
        top.configure(bg='#d198b7')
        tk.Label(top, text = text, padx = 10, pady = 20, bg='#d198b7').pack()
 


root = tk.Tk()
app = App(root, platform)
root.mainloop()