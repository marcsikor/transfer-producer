import tkinter as tk
import os

class App:
    def __init__(self, root):
        self.root = root
        self.titles = ["Receiver name", "Receiver name cont.", "Receiver account number", "Value","Sender account number", "Sender name", "Sender name cont.", "Title"]
        self.additional_titles = ["Stamp, date and signature of the sender", "Stamp", "Fee", "Voucher for the sender's bank", "Voucher for the sender"]
        self.entries = [] # list for storing entry objects
        self.labels = [] # list for storing label objects (for translation)
        self.language_tracker = True # language flag

        self.root.title("Transfer order creator 1.0") # window title
        self.root.configure(bg='#d198b7')

        self.start()

    def start(self):
        self.title_label = tk.Label(self.root, font=('Ubuntu',18,'bold'), text="Transfer order creator\n", bg="#d198b7", fg='#000000') #top label
        self.title_label.pack() # .pack() method used for displaying UI elements

        for i in self.titles: # setting up the labels and entry bars 
            l = tk.Label(root, font=('Ubuntu Regular',16), text=i, bg='#d198b7', fg='#000000')
            l.pack()
            self.labels.append(l)
            e = tk.Entry(root, bg="#E1BFFF", bd=2, highlightcolor='#779ecb', relief='flat')
            e.pack(ipadx = 100)
            self.entries.append(e)

        self.run_button = tk.Button(
        self.root, 
        text="Run", 
        font=('Ubuntu Regular',16), 
        width=10, 
        command=lambda: self.transfer(), 
        bg = '#86C5DA',
        highlightcolor="#779ecb", 
        activebackground="#779ecb",
        activeforeground="white", 
        relief='flat'
        ) # run button
        self.run_button.pack(pady = 10)

        self.language_button = tk.Button(
        self.root, 
        text='Zmień język na polski', 
        font=('Ubuntu Regular',16),
        width=20, 
        command=lambda: self.change_language(), 
        bg = '#86C5DA',
        highlightcolor="#779ecb", 
        activebackground="#779ecb",
        activeforeground="white", 
        relief='flat'
        )
        self.language_button.pack(pady = 10) # translation/language button

    def transfer(self):

        with open('transfer.tex') as g: # opening template tex file
            a = g.read()

        for i in range(8):
            a = a.replace('placeholder'+str(i), self.entries[i].get()) # creating new tex code while editing the template on "placeholder*" flag
            a = a.replace('new*placeh'+str(i), self.titles[i]) # renaming the boxes names with "new*placeh" flag
        
        for i in range(5):
            a = a.replace('additional*plch'+str(i), self.additional_titles[i]) # changing the constant boxes names
        with open('newtransfer.tex', 'w') as f: # creating new tex file
            f.write(a)

        os.system("pdflatex newtransfer.tex") # compiling tex file to pdf

        os.system("evince newtransfer.pdf")  # to display the document in GNOME document viewer (should be altered on windows or other)

        self.temp_files_collector() # removing pdflatex's log and aux files

    def temp_files_collector(self): # collecting pdflatex's temporary files (tex, log, aux) - optional functionality
    
        os.system("rm -rf newtransfer.aux newtransfer.log newtransfer.tex") 

    def change_language(self): # translating method 

        if self.language_tracker:
            self.titles = ["Nazwa odbiorcy","Nazwa odbiorcy cd.","Nr rachunku odbiorcy","Kwota","Nr rachunku zleceniodawcy","Nazwa zleceniodawcy","Nazwa zleceniodawcy cd.","Tytuł"]
            self.additional_titles = ["Pieczęć, data i podpis zleceniodawcy", "Pieczęć", "Opłata", "Odcinek dla banku zleceniodawcy", "Odcinek dla zleceniodawcy"]
            self.root.title("Kreator poleceń przelewu 1.0")
            self.title_label.configure(text = "Kreator polecenia przelewu\n")
            self.language_button.configure(text = "Change language to english")
            self.run_button.config(text='Wykonaj')
            self.language_tracker = False

        else:
            self.titles = ["Receiver name", "Receiver name cont.", "Receiver account number", "Value","Sender account number", "Sender name", "Sender name cont.", "Title"]
            self.additional_titles = ["Stamp, date and signature of the sender", "Stamp", "Fee", "Voucher for the sender's bank", "Voucher for the sender"]
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
app = App(root)
# app.start()
root.mainloop()