import tkinter as tk
from tkinter import ttk
from sys import platform 
import os
import subprocess
import shlex

class App:
    def __init__(self, root, sysinfo):
        
        self.root = root
        # self.titles = ["Receiver name", "Receiver name cont.", "Receiver account number", "Value","Sender account number", "Sender name", "Sender name cont.", "Title"]
        # self.additional_titles = ["Stamp, date and signature of the sender", "Stamp", "Fee", "Voucher for the sender's bank", "Voucher for the sender", "D", "T"]
        self.entries = [] # list for storing entry objects
        self.labels = [] # list for storing label objects (for translation)
        # self.root.title("Transfer order creator 1.0") # window title
        self.root.configure()
        # self.root.geometry('300x300')

        self.temp_lang = 0
        self.temp_dark = 0
       
        if sysinfo == 'linux':
            self.sysinfo = True
        else:
            self.sysinfo = False

        if self.sysinfo:
            self.font = 'Ubuntu'
        else:
            self.font = 'Arial'

        
        with open('config.txt', 'r') as f:
            lines = f.readlines()
 
        self.language_tracker = bool(int(lines[0]))
        self.dark_mode_flag = bool(int(lines[1]))

       
        #     self.language_tracker = True
        #     self.dark_mode_flag = False

        self.title_label = tk.Label(self.root, font=(self.font,18,'bold'), text="Transfer order creator\n") #top label

        self.currency_dropdown() # currency combobox  

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
        
        self.menu() # top menubar        
        
        self.change_language() # adding text to everything

        
        self.start()

    def start(self):
        
        self.title_label.grid(columnspan = 2) # .grid() method used for displaying UI elements

        for i in self.titles: # setting up the labels and entry bars 
            
            l = tk.Label(root, font=(self.font,16), text=i)
            self.labels.append(l)
            
            e = tk.Entry(root, bd=2, relief='flat')
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


        self.l.grid(columnspan = 2, pady = 10)
        
        self.combo.grid(columnspan = 2)

        self.run_button.grid(columnspan = 2, pady = 10)

        self.dark_mode()

    def currency_dropdown(self):

        self.l = tk.Label(root, font=(self.font,16), text="Currency") #label for currency defined here to avoid collision with initial widget positioning

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
            self.titles = ["Nazwa odbiorcy","Nazwa odbiorcy cd.","Nr rachunku odbiorcy","Kwota","Nr rachunku zleceniodawcy","Nazwa zleceniodawcy","Nazwa zleceniodawcy cd.","Tytuł"]
            self.additional_titles = ["Pieczęć, data i podpis zleceniodawcy", "Pieczęć", "Opłata", "Odcinek dla banku zleceniodawcy", "Odcinek dla zleceniodawcy", "W", "P"]
            self.root.title("Kreator poleceń przelewu 1.0")
            self.title_label.configure(text = "Kreator polecenia przelewu\n")
            self.run_button.config(text='Wykonaj')
            self.l.config(text='Waluta')

            self.menubar.entryconfig(1, label = "Opcje")
            self.menubar.entryconfig(2, label = "Zapisani")
            
            self.filemenu.entryconfig(0, label = "Change language to english")
            self.filemenu.entryconfig(1, label = "Tryb ciemny")
            self.filemenu.entryconfig(2, label = "Wyjście")

            save_names = ["Zapisz bieżącego odbiorcę", "Zapisz bieżącego nadawcę", "Odbiorcy", "Nadawcy"]

            for i in range(4):
                self.saved.entryconfig(i, label = save_names[i])

            self.temp_lang = 1

            self.language_tracker = False

        else:
            self.titles = ["Receiver name", "Receiver name cont.", "Receiver account number", "Value","Sender account number", "Sender name", "Sender name cont.", "Title"]
            self.additional_titles = ["Stamp, date and signature of the sender", "Stamp", "Fee", "Voucher for the sender's bank", "Voucher for the sender", "D", "T"]
            self.root.title("Transfer order creator 1.0")
            self.title_label.configure(text = "Transfer order creator\n")
            self.run_button.config(text='Run')
            self.l.config(text='Currency')

            self.menubar.entryconfig(1, label = "Options")
            self.menubar.entryconfig(2, label = "Saved")
            
            self.filemenu.entryconfig(0, label = "Zmień język na polski")
            self.filemenu.entryconfig(1, label = "Dark mode")
            self.filemenu.entryconfig(2, label = "Exit")
            
            save_names = ["Save current receiver", "Save current sender", "Receivers", "Senders"]

            for i in range(4):
                self.saved.entryconfig(i, label = save_names[i])

            self.temp_lang = 0
            
            self.language_tracker = True

        a = 0
        for i in self.labels: # renaming labels
            i.configure(text=self.titles[a])
            a += 1

    def dark_mode(self):

        if self.dark_mode_flag:
          
            self.root.configure(bg = '#212121' )
            for i in self.labels: # renaming labels
                i.configure(bg = '#212121', fg='#dddddd')
            self.l.config(bg = '#212121', fg='#dddddd')
            for i in self.entries:
                i.configure(bg = '#3d3d3d', fg='#dddddd')
            self.title_label.configure(bg = '#212121', fg='#dddddd')
            self.temp_dark = 1
            self.dark_mode_flag = False

        else:
            
            self.root.configure(bg = '#d198b7' )
            for i in self.labels: # renaming labels
                i.configure(bg = '#d198b7', fg='#000000')
            self.l.config(bg = '#d198b7', fg='#000000')
            for i in self.entries:
                i.configure(bg = '#dddddd', fg='#000000')
            self.title_label.configure(bg = '#d198b7', fg='#000000')
            self.temp_dark = 0
            self.dark_mode_flag = True
        

    def menu(self): # top menu

        import csv # csv format used to save senders/receivers

        self.menubar = tk.Menu(root, bg = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white")

        self.filemenu = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white" ) # submenus
        self.saved = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white" )

        self.menubar.config(font = self.font)
        
        self.filemenu.config(font = self.font)
        self.saved.config(font = self.font)

        self.filemenu.add_command(command=self.change_language)
        self.filemenu.add_command(command=self.dark_mode)
        self.filemenu.add_command(command=root.quit)

        self.saved.add_command(command=lambda: self.save_csv(True))
        self.saved.add_command(command=lambda: self.save_csv(False))

        saved_rece = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white") # cascade sub sub menu
        saved_send = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white")

        try:
            f = open('receivers.csv') # file with saved receivers
            reader = list(csv.reader(f))

            for i in reader:
                saved_rece.add_command(label = i[0], command=lambda i=i: self.fill(i, True))
            
            f.close()
        except FileNotFoundError: 
            pass # ignoring the code if there is no file

        try:

            f = open('senders.csv') # file with saved senders
            reader = list(csv.reader(f))

            for i in reader:
                saved_send.add_command(label = i[0], command=lambda i=i: self.fill(i, False))
                    
            f.close()
                
        except FileNotFoundError:
            pass

        self.menubar.add_cascade(menu=self.filemenu)
        self.menubar.add_cascade(menu=self.saved)

        self.saved.add_cascade(menu=saved_rece)
        self.saved.add_cascade(menu=saved_send)
        
        self.root.config(menu=self.menubar)

    # saving receiver/sender
  
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

        # pop-up window

        top = tk.Toplevel(self.root) # top 
 
        # adding identification code which will be viewed in the menu

        if self.language_tracker:
            top.title('Saving')
            temp_label = tk.Label(top, text = f"Enter {name}'s identification code\n This code will allow you to distinguish saved positions in the menu \n Restart the program in order to view changes", padx = 10, pady = 20)
        else:
            top.title('Zapisywanie') 
            temp_label = tk.Label(top, text = f"Wpisz kod identyfikacyjny {name}\n Ten kod pozwoli ci rozróżnić zapisane pozycje w menu \n Zrestartuj program, aby zobaczyć zmiany", padx = 10, pady = 20)
        
        e = tk.Entry(top)

        # dark mode provision

        if self.dark_mode_flag:
            top.configure(bg='#d198b7')
            temp_label.config(bg='#d198b7')
        else:
            top.configure(bg = '#212121')
            temp_label.config(bg = '#212121', fg='#dddddd')
            e.config(bg = '#3d3d3d', fg='#dddddd')


        temp_label.pack()
        e.pack(pady = 10)

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
        relief='flat',
        ).pack()
        
    # saving the code from the pop-up and entered data

    def sub_save(self, value, index, name, top):

        if value == '':

            # pop-up error

            if self.language_tracker:
                self.error(f"Enter {name}'s identification code")
            else:
                self.error(f"Wpisz kod identyfikacyjny {name}")

            return 1

        else:

            a = value.upper()

            for i in index:
                a += f",{self.entries[i].get()}"

            with open(f'receivers.csv', 'a') as f:
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

    # pop-up error method

    def error(self,text):

        top = tk.Toplevel(self.root)
        if self.language_tracker:
            top.title('Error')
        else:
            top.title('Błąd')

        temp_label = tk.Label(top, text = text, padx = 10, pady = 20)
        if self.dark_mode_flag:
            top.configure(bg='#d198b7')
            temp_label.config(bg='#d198b7')
        else:
            top.configure(bg = '#212121')
            temp_label.config(bg = '#212121', fg='#dddddd')
        temp_label.pack()

    # saving configuration (dark mode and language)

    def save_config(self):

        with open('config.txt', 'w') as f:
            f.write(str(self.temp_lang) + '\n' + str(self.temp_dark))

root = tk.Tk()
app = App(root, platform)
root.mainloop()

# saving configuration upon closing the window

app.save_config()