import tkinter as tk
from tkinter import ttk
from sys import platform 
import subprocess
from csv import reader

class App:
    def __init__(self, root, sysinfo):
        
        self.root = root
        self.root.resizable(True, True)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # lists for storing entry and label objects - do not repeat yourself (too much)

        self.entries = [] 
        self.labels = [] 
    
        # variables for writing to file

        self.temp_lang = 0
        self.temp_dark = 0
       
        # determining the operationg system

        if sysinfo == 'linux':
            self.sysinfo = True
        else:
            self.sysinfo = False

        # setting up the font based on the system

        if self.sysinfo:
            self.font = 'Ubuntu'
        else:
            self.font = 'Arial'

        # importing saved settings

        try:
            with open('config.txt', 'r') as f:
                lines = f.readlines()
    
            self.language_tracker = bool(int(lines[0]))
            self.dark_mode_flag = bool(int(lines[1]))
        
        except (FileNotFoundError, IndexError): # defaults

            self.language_tracker = True
            self.dark_mode_flag = True

        # top label definition

        self.title_label = tk.Label(self.root, font=(self.font,18,'bold'), text="Transfer order creator\n")

        # currency combobox menu code

        self.currency_label= tk.Label(self.root, font=(self.font,16), text="Currency") #label for currency defined here to avoid collision with initial widget positioning

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

        # finally dropdown menu

        self.combo = ttk.Combobox(self.root)
        self.combo["values"] = ['PLN','USD','GBP']
        self.combo.current(0) 

        # run button setup

        self.run_button = tk.Button(
        self.root, 
        text="Run", 
        font=(self.font,16), 
        width=10, 
        command=self.transfer, 
        bg = '#86C5DA',
        highlightcolor="#779ecb", 
        activebackground="#779ecb",
        activeforeground="white", 
        relief='flat'
        )

        # dropdown top bar menus

        self.menubar = tk.Menu(root, bg = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white")
        self.filemenu = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white" ) # submenus
        self.saved = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white" )
        
        self.menubar.config(font = self.font)
        self.filemenu.config(font = self.font)
        self.saved.config(font = self.font)

        # submenus

        self.filemenu.add_command(command=self.change_language)
        self.filemenu.add_command(command=self.dark_mode)
        self.filemenu.add_command(command=root.quit)

        self.saved.add_command(command=lambda: self.save_csv(True))
        self.saved.add_command(command=lambda: self.save_csv(False))

        # subsubmenu for saving

        saved_rece = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white") # cascade sub sub menu
        saved_send = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white")

        # subsubmenu for removing

        remov_rece = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white") 
        remov_send = tk.Menu(self.menubar, tearoff = 0, background = '#86C5DA', relief = 'flat', activebackground='#779ecb', activeforeground = "white")

        # adding the cascade menu for senders/receivers
        # try block in case the files are not present

        try:
            
            # file with saved receivers

            f = open('receivers.csv', 'r') 
            csvreader = list(reader(f, delimiter='|'))
            for i in csvreader:
                saved_rece.add_command(label = i[0], command=lambda i=i: self.fill(i, True))
                remov_rece.add_command(label = i[0], command=lambda i=i: self.remove_saved(i,True))

            # first receiver on startup

            receiver_present = list(csvreader[0])

            f.close()

        except (FileNotFoundError, IndexError): # exception when there is no file or the file is empty
            
            receiver_present = ''

        try:

            # file with saved senders

            f = open('senders.csv', 'r') 
            csvreader = list(reader(f, delimiter='|'))

            for i in csvreader:
                saved_send.add_command(label = i[0], command=lambda i=i: self.fill(i, False))
                remov_send.add_command(label = i[0], command=lambda i=i: self.remove_saved(i, False))

            # first sender on startup 

            sender_present = csvreader[0]
            
            f.close()
                
        except (FileNotFoundError, IndexError): 
            
            sender_present = ''

        # placing the submenus in the proper 
        
        self.menubar.add_cascade(menu=self.filemenu)
        self.menubar.add_cascade(menu=self.saved)

        self.saved.add_cascade(menu=saved_rece)
        self.saved.add_cascade(menu=saved_send)
        self.saved.add_cascade(menu=remov_rece)
        self.saved.add_cascade(menu=remov_send)
        
        self.root.config(menu=self.menubar)        
        
        # adding text to everything with change_language method
        
        self.change_language() 

        # placing all widgets
        # .grid() method used for displaying UI elements

        self.title_label.grid(columnspan = 2) 
        
        # setting up the labels and entry bars 
        
        for i in self.titles: 
            
            l = tk.Label(root, font=(self.font,16), text=i)
            self.labels.append(l)
            
            e = tk.Entry(root, bd=2, relief='flat')
            self.entries.append(e)

        j = 0
        k = 0
        for a in range(2):
            for i in range(1,9):
                if i % 2 == 1:
                    self.labels[j].grid(column = a, row = i)
                    j += 1
                else:
                    self.entries[k].grid(column = a, row = i, ipadx = 100, padx = 10)
                    k += 1


        self.currency_label.grid(columnspan = 2, pady = 10)
        
        self.combo.grid(columnspan = 2)

        self.run_button.grid(columnspan = 2, pady = 10)

        # filling the first sender/receiver on startup:
        
        if receiver_present != '':
            self.fill(receiver_present,True)
        if sender_present != '':
            self.fill(sender_present,False)

        # running dark mode based on initial configuration

        self.dark_mode()

    # run button function

    def transfer(self):

        with open('transfer.tex') as g: # opening template tex file
            a = g.read()

        for i in range(8):
            a = a.replace('placeholder'+str(i), self.entries[i].get().upper()) # creating new tex code while editing the template on "placeholder*" flag
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
            status = subprocess.call("xdg-open newtransfer.pdf", shell=True)  # to display pdf in linux (xdg-open is an x11 command to open in default pdf editor)  
        else:
            subprocess.call("newtransfer.pdf") # same for windows

    # removing pdflatex's remaining files (tex, log, aux)

        if self.sysinfo:    
            subprocess.call("rm -rf newtransfer.aux newtransfer.log newtransfer.tex", shell=True) 
        else:
            subprocess.call('del "newtransfer.aux" "newtransfer.log" "newtransfer.tex" ')

    # changing_language and adding text method

    def change_language(self): 

        if self.language_tracker:
            self.titles = ["Nazwa odbiorcy","Nazwa odbiorcy cd.","Nr rachunku odbiorcy","Kwota","Nr rachunku zleceniodawcy","Nazwa zleceniodawcy","Nazwa zleceniodawcy cd.","Tytuł"]
            self.additional_titles = ["Pieczęć, data i podpis zleceniodawcy", "Pieczęć", "Opłata", "Odcinek dla banku zleceniodawcy", "Odcinek dla zleceniodawcy", "W", "P"]
            self.root.title("Kreator poleceń przelewu 1.1")
            self.title_label.configure(text = "Kreator polecenia przelewu\n")
            self.run_button.config(text='Wykonaj')
            self.currency_label.config(text='Waluta')

            self.menubar.entryconfig(1, label = "Opcje")
            self.menubar.entryconfig(2, label = "Zapisani")
            
            self.filemenu.entryconfig(0, label = "Change language to english")
            self.filemenu.entryconfig(1, label = "Tryb ciemny")
            self.filemenu.entryconfig(2, label = "Wyjście")

            save_names = ["Zapisz bieżącego odbiorcę", "Zapisz bieżącego zleceniodawcę", "Odbiorcy", "Zleceniodawcy", "Usuń zapisanego odbiorcę", "Usuń zapisanego zleceniodawcę"]

            for i in range(6):
                self.saved.entryconfig(i, label = save_names[i])

            self.temp_lang = 1

            self.language_tracker = False

        else:
            self.titles = ["Receiver name", "Receiver name cont.", "Receiver account number", "Value","Sender account number", "Sender name", "Sender name cont.", "Title"]
            self.additional_titles = ["Stamp, date and signature of the sender", "Stamp", "Fee", "Voucher for the sender's bank", "Voucher for the sender", "D", "T"]
            self.root.title("Transfer order creator 1.1")
            self.title_label.configure(text = "Transfer order creator\n")
            self.run_button.config(text='Run')
            self.currency_label.config(text='Currency')

            self.menubar.entryconfig(1, label = "Options")
            self.menubar.entryconfig(2, label = "Saved")
            
            self.filemenu.entryconfig(0, label = "Zmień język na polski")
            self.filemenu.entryconfig(1, label = "Dark mode")
            self.filemenu.entryconfig(2, label = "Exit")
            
            save_names = ["Save current receiver", "Save current sender", "Receivers", "Senders", "Remove saved receiver", "Remove saved sender"]

            for i in range(6):
                self.saved.entryconfig(i, label = save_names[i])

            self.temp_lang = 0
            
            self.language_tracker = True

        # renaming labels

        for i in range(len(self.labels)):
            self.labels[i].configure(text=self.titles[i])

    # dark mode function

    def dark_mode(self):

        # changing colors depending on the flag

        if self.dark_mode_flag:
          
            self.root.configure(bg = '#212121' )
            for i in self.labels: 
                i.configure(bg = '#212121', fg='#dddddd')
            self.currency_label.config(bg = '#212121', fg='#dddddd')
            for i in self.entries:
                i.configure(bg = '#3d3d3d', fg='#dddddd', highlightcolor = "#dddddd", highlightbackground="#000000")
            self.title_label.configure(bg = '#212121', fg='#dddddd')
            self.temp_dark = 1
            self.dark_mode_flag = False

        else:
            
            self.root.configure(bg = '#d198b7' )
            for i in self.labels:
                i.configure(bg = '#d198b7', fg='#000000')
            self.currency_label.config(bg = '#d198b7', fg='#000000')
            for i in self.entries:
                i.configure(bg = '#dddddd', fg='#000000', highlightcolor = "black", highlightbackground="#d198b7")
            self.title_label.configure(bg = '#d198b7', fg='#000000')
            self.temp_dark = 0
            self.dark_mode_flag = True

    # saving receiver/sender
  
    def save_csv(self, test): 

        # technically do not repeat yourself :D

        if test:
            
            filename = 'receivers.csv'

            if self.language_tracker:
                name = 'receiver'
            else:
                name = 'odbiorcy'
            index = [0,1,2]
        
        else:

            filename = 'senders.csv'

            if self.language_tracker:
                name = 'sender'
            else:
                name = 'zleceniobiorcy'
            index = [4,5,6]

        # pop-up window on top

        top = tk.Toplevel(self.root)
 
        # adding identification code which will be viewed in the menu

        if self.language_tracker:
            top.title('Saving')
            temp_label = tk.Label(top, text = f"Enter {name}'s identification code.\n This code will allow you to distinguish saved positions in the menu. \n Restart the program in order to view changes.", pady = 5)
        else:
            top.title('Zapisywanie') 
            temp_label = tk.Label(top, text = f"Wpisz kod identyfikacyjny {name}.\n Ten kod pozwoli ci rozróżnić zapisane pozycje w menu. \n Zrestartuj program, aby zobaczyć zmiany.", pady = 5)
        
        e = tk.Entry(top)

        # dark mode provision

        if self.dark_mode_flag:
            top.configure(bg='#d198b7')
            temp_label.config(bg = '#d198b7', fg='#000000')
            e.config(bg = '#dddddd', fg='#000000', highlightcolor = "black", highlightbackground="#d198b7", relief = 'flat')
        else:
            top.configure(bg = '#212121')
            temp_label.config(bg = '#212121', fg='#dddddd')
            e.config(bg = '#3d3d3d', fg='#dddddd', highlightcolor = "#dddddd", highlightbackground="#000000", relief = 'flat')

        # packing the widgets in the pop-up

        temp_label.pack()
        e.pack(pady = 10)

        tk.Button(
        top, 
        pady = 5,
        text="Save", 
        font=(self.font,16), 
        width=10, 
        command=lambda: self.sub_save(e.get(), index, name, top, filename),
        bg = '#86C5DA',
        highlightcolor="#779ecb", 
        activebackground="#779ecb",
        activeforeground="white", 
        relief='flat',
        ).pack()
        
    # saving the code from the pop-up and entered data

    def sub_save(self, value, index, name, top, filename):

        if value == '':

            # error pop-up

            if self.language_tracker:
                self.error(f"Enter {name}'s identification code.")
            else:
                self.error(f"Wpisz kod identyfikacyjny {name}.")

            return 1

        else:

            a = value.upper()

            for i in index:
                a += f"|{self.entries[i].get()}"

            with open(filename, 'a') as f:
                f.write(a+"\n")

        top.destroy()

    # filling data function

    def fill(self, line, test):

        if test:
            for i in range(3):
                self.entries[i].delete(0,'end')
                self.entries[i].insert(0,line[i+1])

        else:
            for i in range(3):
                self.entries[i+4].delete(0,'end')
                self.entries[i+4].insert(0,line[i+1])
                
    def remove_saved(self, line, test):

        if test:
            filename = 'receivers.csv'
        else:
            filename = 'senders.csv'
        with open(filename, 'r') as f:
            lines = list(reader(f, delimiter='|'))
        with open(filename, 'w') as f:
            for i in lines:
                if i != line:
                    f.write("|".join(i))

        # pop-up window

        top = tk.Toplevel(self.root) # top 
 
        # instructing the user that the changes will be visible after a restart

        if self.language_tracker:
            if test:
                name = "receiver"
            else:
                name = "sender"
            top.title('Deleting')
            temp_label = tk.Label(top, text = f"The {name} has been removed. \n Restart the program in order to view changes.", pady = 5)
        else:
            if test:
                name = "Odbiorca"
            else:
                name = "Zleceniodawca"
            top.title('Usuwanie') 
            temp_label = tk.Label(top, text = f"{name} został usunięty. \n Zrestartuj program aby zobaczyć zmiany.", pady = 5)

        temp_label.pack()

        # dark mode provision

        if self.dark_mode_flag:
            top.configure(bg='#d198b7')
            temp_label.config(bg = '#d198b7', fg='#000000')
        else:
            top.configure(bg = '#212121')
            temp_label.config(bg = '#212121', fg='#dddddd')

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

# saving configuration after closing the window

app.save_config()