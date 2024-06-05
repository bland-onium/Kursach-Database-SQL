import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import threading
from tkinter import ttk

global address
global acc
acc = 0
prog = True
baseexist = False

#######################################################################################################################

class DB(tk.Toplevel):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main=main

    def input(self):
        self.title("Adding new element...")
        self.resizable(False, False)
        self.geometry("150x380")
        self.focus_force()

        # Создание списка для хранения полей ввода
        label_list = ['ID', 'TYPE', 'VENDOR', 'MODEL', 'LENGTH', 'WIDTH', 'HEIGHT', 'COUNT']
        entry_list = []
        # Создание полей ввода
        for i in range(8):  # Создаем 7 полей ввода
            label = tk.Label(self, text=label_list[i]); label.pack()
            entry = tk.Entry(self); entry.pack()
            entry_list.append(entry)

        input_button = tk.Button(self, text="Add to base", command=lambda: self.get_data(entry_list=entry_list))
        input_button.pack()

    def get_data(self, entry_list):
        input_list = []
        for i in range(8):
            entry = entry_list[i]
            input_value = entry.get()
            if input_value!=None or str(input_value)!='0' or input_value != '':
                input_list.append(input_value)
            else:
                input_list.append("None")
        self.write(input_list=input_list)
        #input_list = []

    def write(self, input_list):
        global address
        print("working file: ",address)
        try:
            isrl = int(input_list[0])
        except:
            input_list[0] = '1'
        con = sqlite3.connect(str(address))
        curs = con.cursor()
        if input_list[0] == "None" or str(input_list[0]) == "0" or str(input_list[0])=="": input_list[0] = '1'
        if input_list[-1] == None or str(input_list[-1]) == "": input_list[-1] = '1'
        bl = 1
        i = 0
        while bl == 1:
            bl = self.find(id=int(input_list[0])+i, vendor=input_list[2], model=input_list[3])
            if bl == 0:
                break
            elif bl == 2:
                curs.execute("SELECT * FROM STORAGE WHERE ID = ?", (input_list[0],))
                row = curs.fetchone()
                input_list[-1]=(int(row[-1])+int(input_list[-1]))
                curs.execute(f"""DELETE FROM STORAGE WHERE ID = {input_list[0]}""")
            else:
                i+=1
        input_list[0] = str(int(input_list[0])+i)
        # Пример безопасного запроса с использованием параметризованных запросов
        query = """INSERT INTO "STORAGE" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        input_data = (input_list[0], input_list[1], input_list[2], input_list[3],
                      self.get_size(len=input_list[4], wid=input_list[5], hei=input_list[6]), input_list[4], input_list[5],
                      input_list[6], input_list[7])
        # Выполнение запроса с передачей данных как кортежа
        curs.execute(query, input_data)
        con.commit()
        con.close()
        self.destroy()

    def find(self, id, vendor, model):
        con = sqlite3.connect(str(address))
        curs = con.cursor()
        curs.execute(f"SELECT * FROM STORAGE WHERE ID = {str(id)}")
        res = curs.fetchone()
        con.close()
        if res == None: return 0
        elif (res[2] == vendor and res[3] == model and res != None): return 2
        else: return 1

    def display(self):
        global address
        self.title(f"Database -> {address}")
        self.geometry("1200x250")
        #self.resizable(False, False)
        self.focus()

        tree = ttk.Treeview(self)
        tree.pack()
        con = sqlite3.connect(address)
        curs = con.cursor()
        curs.execute("""SELECT * FROM 'STORAGE'""")
        rows = curs.fetchall()
        tree["columns"] = [i for i in range(len(rows[0]))]
        label_list = ['ID', 'TYPE', 'VENDOR', 'MODEL', 'SIZETYPE', 'LENGTH', 'WIDTH', 'HEIGHT', 'COUNT']
        for i in range(len(rows[0])):
            tree.column(i, anchor=tk.W, width=100)
            tree.heading(i, text=label_list[i], anchor=tk.W)
        # Добавляем данные в таблицу
        for row in rows:
            tree.insert("", tk.END, values=row)
        con.close()

    def get_ID(self, mode):
        self.title("Some new command...")
        self.resizable(False, False)
        self.focus_force()

        label = tk.Label(self, text="ID"); label.pack()
        entry = tk.Entry(self); entry.pack()

        input_button = tk.Button(self, text="PUSH", command=lambda: self.get_input(entry = entry, mode=mode))
        input_button.pack()

    def get_IDNAME(self, mode):
        self.title("Adding new element...")
        self.resizable(False, False)
        self.focus_force()

        label = tk.Label(self, text="ID or Name"); label.pack()
        entry = tk.Entry(self); entry.pack()

        input_button = tk.Button(self, text="PUSH", command=lambda: self.get_input(entry=entry, mode=mode))
        input_button.pack()

    def get_input(self, entry, mode):
        inp = entry.get()
        print("Введенное значение:", inp)
        self.destroy()
        if mode == 1:
            self.delete_one(ID=inp)
        elif mode == 2:
            self.delete_fullelem(ID=inp)
        else:
            self.rl_find(ID=inp)
        #self.destroy()  # Закрываем окно после получения значения

    def delete_one(self, ID):
        global address
        con = sqlite3.connect(address)
        curs = con.cursor()
        try:
            curs.execute("""SELECT * FROM 'STORAGE' WHERE ID=?""", (ID,))
            row = curs.fetchone()
            count = int(row[-4])
            if count > 1:
                count = count - 1
                curs.execute("""UPDATE STORAGE SET COUNT = ? WHERE ID = ?""", (count, ID))
                print("removed one from group")
            else:
                curs.execute(f"""DELETE FROM STORAGE WHERE ID = {str(ID)})""")
                print("removed element")
                con.commit()
                con.close()
                self.destroy()
        except:
            print(f"Probably, var with ID={ID} does not exist")
            self.destroy()

    def delete_fullelem(self, ID):
        global address
        con = sqlite3.connect(address)
        curs = con.cursor()
        try:
            curs.execute("""SELECT * FROM STORAGE WHERE ID=?""", (ID,))
            row = curs.fetchone()
            curs.execute(f"""DELETE FROM STORAGE WHERE ID=?""",(ID,))
            print("removed element")
            con.commit()
            con.close()
            self.destroy()
        except:
            print(f"Probably, var with ID={ID} does not exist")
            self.destroy()

    def form_out(self, row):
        out = ""
        for i in range(len(row)):
            out += str(row[i])+" | "
        return out

    def rl_find(self, ID):
        global address
        con = sqlite3.connect(address)
        curs = con.cursor()
        nrt = tk.Toplevel()
        nrt.title("founded element")
        nrt.resizable(False, False)
        turnoff = tk.Button(nrt, text="Close", command=lambda: nrt.destroy())
        turnoff.pack(anchor='se')

        gd = True
        try:
            int_ID = int(ID)
            curs.execute(f"SELECT * FROM STORAGE WHERE ID = {ID}")
            res = curs.fetchone()
            print(res)
            label = tk.Label(nrt, text="Характеристики найденного элемента:");
            label.pack()
            label_out = tk.Label(nrt, text=res);
            label_out.pack()
            gd = True
        except:
            print("Can't find element by ID")
            gd = False
        if gd == False:
            try:
                rows1 = []; rows2 = []; rows3 = []
                curs.execute("""SELECT * FROM STORAGE WHERE NAME LIKE ?""", ('%' + ID + '%',))
                rows1 = curs.fetchall()
                curs.execute("""SELECT * FROM STORAGE WHERE MODEL LIKE ?""",('%' + ID + '%',))
                rows2 = curs.fetchall()
                curs.execute("""SELECT * FROM STORAGE WHERE TYPE LIKE ?""",('%' + ID + '%',))
                rows3 = curs.fetchall()
                label = tk.Label(nrt, text="Найденные элементы\nID | type | vendor | model | size | count | len | wid | hei\n"
                                           "_______________________________________________________________________________"); label.pack()
                i = 0
                if len(rows1) > 0:
                    while (i<len(rows1)):
                        label_out = tk.Label(nrt, text=self.form_out(row=rows1[i]));
                        label_out.pack()
                        i+=1
                i=0
                if len(rows2) > 0:
                    while (i<len(rows2)):
                        label_out = tk.Label(nrt, text=self.form_out(row=rows2[i]));
                        label_out.pack()
                        i += 1
                i = 0
                if len(rows3) > 0:
                    while (i < len(rows3)):
                        label_out = tk.Label(nrt, text=self.form_out(row=rows3[i]));
                        label_out.pack()
                        i += 1
            except:
                print("Probably, elements are not founded")
        nrt.mainloop()

    def get_size(self, len, wid, hei):
        try:
            len = int(len); wid = int(wid); hei = int(hei)
            if ((wid + hei + len) > 600):
                return 'V'
            elif (len > 100 or wid > 100 or hei > 100):
                return 'L'
            elif ((len + wid + hei) > 100 and (len + wid + hei) <= 300):
                return 'M'
            elif ((len + wid + hei) <= 100):
                return 'S'
            else:
                return 'M'
        except:
            return 'M'

#######################################################################################################################
class Loginform(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_reg()

    def log_reg(self):
        self.title("How you want to work?")
        self.resizable(False, False)
        self.focus_force()
        label = tk.Label(self, text="Choose how \nYou wanna work:"); label.pack()
        button1 = tk.Button(self, text="As an administrator", height=5, width=20, command=lambda: self.log_admin())
        button1.pack()
        button2 = tk.Button(self, text="As an     guest    ", height=5, width=20, command=lambda: self.log_user())
        button2.pack()
        turnoff = tk.Button(self, text="Close", command=lambda: exit())
        turnoff.pack(anchor='ne')

    def log_admin(self):
        ntk = tk.Toplevel()
        ntk.title("Loggining")
        ntk.resizable(False, False)
        ntk.focus_force()
        label = tk.Label(ntk, text="Input login and password"); label.pack()
        label = tk.Label(ntk, text="Login:"); label.pack()
        entry_login = tk.Entry(ntk); entry_login.pack()
        label = tk.Label(ntk, text="Password"); label.pack()
        entry_pass  = tk.Entry(ntk); entry_pass.pack()
        inp_button = tk.Button(ntk, text="PUSH ME",  width=20, height=5, command=
        lambda: self.admit_login(TK=ntk, login=entry_login, pswd=entry_pass)); inp_button.pack()
        turnoff = tk.Button(ntk, text="Close",command=lambda: exit())
        turnoff.pack(anchor='ne')
        ntk.mainloop()

    def admit_login(self, TK, login, pswd):
        global acc
        inplog = login.get(); inppass = login.get()
        log = "admin"; password = "admin"
        if (inplog == log and inppass == password):
            acc = 1
            label = tk.Label(TK, text="Good login"); label.pack()
        else:
            label = tk.Label(TK, text="Wrong login"); label.pack()
            acc = 0
        self.destroy()

    def log_user(self):
        global acc
        acc = 2
        self.destroy()

class Get_file(tk.Toplevel):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.input()

    def input(self):
        #super().__init__(*args, **kwargs)
        self.title("Choosing type of work")
        self.resizable(False, False)
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", lambda: exit())
        label = tk.Label(self, text="Mode of database:"); label.pack()
        button1 = tk.Button(self, text="Open existing file", width=25, height=5, command=lambda: self.get_address())
        button1.pack(pady=10, padx=40)
        button2 = tk.Button(self, text="Create new file", width=25, height=5, command=lambda: self.new_base())
        button2.pack(pady=20, padx=40)
        turnoff = tk.Button(self, text="Close", command=lambda: exit())
        turnoff.pack(anchor='ne')

    def new_base(self):
        address = simpledialog.askstring("Input", "Input name of new base:")
        if '.db' not in address: address = address + '.db'
        try:
            con = sqlite3.connect(address)
            curs = con.cursor()
            con.close()
        except:
            return 0

        if address == "": address = "no_way.db"
        con = sqlite3.connect(address)
        curs = con.cursor()
        curs.execute("""
                    CREATE TABLE "STORAGE"(
                    ID INTEGER PRIMARY KEY,
                    TYPE TEXT NOT NULL,
                    NAME TEXT,
                    MODEL TEXT NOT NULL,
                    SIZETYPE CHAR NOT NULL,
                    COUNT INT NOT NULL,
                    LENGTH INT,
                    WIDTH INT,
                    HEIGHT INT
                    )
                    """)
        con.commit()
        con.close()
        self.destroy()

    def get_address(self):
        global address
        address = filedialog.askopenfilename()

        try:
            con = sqlite3.connect(str(address))
            curs = con.cursor()
            curs.execute("""SELECT * FROM STORAGE""")
            curs.close()
            con.close()
            print("address is: ", address)
        except:
            print("Something went wrong, let's create new database")
            address = self.new_base()
        self.main.attributes("-disabled", False)
        self.destroy()
#######################################################################################################################

class Menu(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global acc
        if acc == 1:
            self.title("Choose what you wanna see:")
            self.resizable(False, False)
            button_insert = tk.Button(self, text="Insert new", width=20, height=4, command=lambda: self.open_input()); button_insert.pack(anchor='n') # Create and insert new writing in DB
            button_delete = tk.Button(self, text="Delete part", width=20, height=4, command=lambda: self.del_one()); button_delete.pack(anchor='n') # Remove 1 count of choosen thing
            butt_clearvar = tk.Button(self, text="Delete elem", width=20, height=4, command=lambda: self.del_elem()); butt_clearvar.pack(anchor='n') # Remove var with all het info
            button_find   = tk.Button(self, text="Find  item", width=20, height=4, command=lambda: self.find_db()); button_find.pack(anchor='n') # Find element by ID
            button_display= tk.Button(self, text="Show   all", width=20, height=4, command=lambda: self.show_db()); button_display.pack(anchor='n') # Show database
            turnoff =       tk.Button(self, text="Close", command=lambda: exit()); turnoff.pack(anchor='ne')
            self.attributes('-disabled',True)
            threading.Thread(target=Get_file, args=[self, ]).start()
        elif acc == 2:
            self.title("Choose what you wanna see:")
            self.resizable(False, False)
            button_find = tk.Button(self, text="Find  item", width=20, height=4, command=lambda: self.find_db());
            button_find.pack(anchor='n')  # Find element by ID
            button_display = tk.Button(self, text="Show   all", width=20, height=4, command=lambda: self.show_db());
            button_display.pack(anchor='n')  # Show database
            turnoff = tk.Button(self, text="Close", command=lambda: exit());
            turnoff.pack(anchor='ne')
            self.attributes('-disabled', True)
            threading.Thread(target=Get_file, args=[self, ]).start()

    def open_input(self):
        tbl = DB(self)
        tbl.input()
    def del_one(self):
        tbl = DB(self)
        tbl.get_ID(mode=1)
    def del_elem(self):
        tbl = DB(self)
        tbl.get_ID(mode=2)
    def find_db(self):
        tbl = DB(self)
        tbl.get_IDNAME(mode=3)
    def show_db(self):
        tbl = DB(self)
        tbl.display()

#######################################################################################################################
if __name__ == '__main__':
    acc = 0
    prog = True
    log = Loginform()
    log.mainloop()
    if acc != 0 and prog == True:
        #root
        app = Menu()
        app.mainloop()
        prog = False



