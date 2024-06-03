import sqlite3
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import threading
from tkinter import ttk

global address
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
        self.focus_force()

        # Создание списка для хранения полей ввода
        label_list = ['ID', 'TYPE', 'VENDOR', 'MODEL', 'LENGTH', 'WIDTH', 'HEIGHT', 'COUNT']
        entry_list = []
        # Создание полей ввода
        for i in range(8):  # Создаем 7 полей ввода
            label = tk.Label(self, text=label_list[i]); label.pack()
            entry = tk.Entry(self); entry.pack()
            entry_list.append(entry)
        print("got that(delete me)")
        input_button = tk.Button(self, text="Add to base", command=lambda: self.get_data(entry_list=entry_list))
        input_button.pack()
        print(entry_list, "entry (delete me)")

    def get_data(self, entry_list):
        input_list = []
        for i in range(8):
            entry = entry_list[i]
            input_value = entry.get()
            input_list.append(input_value)
        self.write(input_list=input_list)
        print(input_list, "input (delete me)")
        #input_list = []

    def write(self, input_list):
        global address
        print(address)
        print(input_list)
        con = sqlite3.connect(str(address))
        curs = con.cursor()
        bl = True
        i = 0
        while bl == True:
            bl = self.find(id=int(input_list[0])+i)
            if bl == False:
                break
            else:
                i+=1
        input_list[0] = str(int(input_list[0])+i)
        # Пример безопасного запроса с использованием параметризованных запросов
        query = """INSERT INTO "STORAGE" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        input_data = (input_list[0], input_list[1], input_list[2], input_list[3],
                      Item.get_size(int(input_list[4]), int(input_list[5]), int(input_list[6])), input_list[4], input_list[5],
                      input_list[6], input_list[7])
        # Выполнение запроса с передачей данных как кортежа
        curs.execute(query, input_data)
        con.commit()
        con.close()
        self.destroy()
        self.main.attributes('-disabled', False)

    def display(self):
        global address
        self.title(f"Database -> {address}")
        self.resizable(False, False)
        self.focus()

        tree = ttk.Treeview(self)
        tree["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
        tree.column("#0", width=0, stretch=tk.NO);       tree.heading("#0", text="", anchor=tk.W)
        tree.column("1", anchor=tk.W, width=100);        tree.heading("1", text="ID", anchor=tk.W)
        tree.column("2", anchor=tk.W, width=100);        tree.heading("2", text="Type", anchor=tk.W)
        tree.column("3", anchor=tk.W, width=100);        tree.heading("3", text="Vendor", anchor=tk.W)
        tree.column("4", anchor=tk.W, width=100);        tree.heading("4", text="Model", anchor=tk.W)
        tree.column("5", anchor=tk.W, width=100);        tree.heading("5", text="Size", anchor=tk.W)
        tree.column("6", anchor=tk.W, width=100);        tree.heading("6", text="Length", anchor=tk.W)
        tree.column("7", anchor=tk.W, width=100);        tree.heading("7", text="Width", anchor=tk.W)
        tree.column("8", anchor=tk.W, width=100);        tree.heading("8", text="Height", anchor=tk.W)
        tree.column("9", anchor=tk.W, width=100);        tree.heading("9", text="count", anchor=tk.W)
        con = sqlite3.connect(address)
        curs = con.cursor()
        curs.execute("""SELECT * FROM 'STORAGE'""")
        rows = curs.fetchall()
        for row in rows:
            tree.insert("", tk.END, text=row[0],
                        values=(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    def find(self, id):
        con = sqlite3.connect(str(address))
        curs = con.cursor()
        curs.execute(f"SELECT * FROM STORAGE WHERE ID = {str(id)}")
        res = curs.fetchone()
        print(res)
        con.close()
        if res == None: return False
        else: return True

    def get_ID(self):
        self.title("Adding new element...")
        self.resizable(False, False)
        self.focus_force()

        label = tk.Label(self, text="ID");
        label.pack()
        entry = tk.Entry(self);
        entry.pack()

        input_button = tk.Button(self, text="PUSH", command=lambda: self.get_input(entry = entry))
        input_button.pack()

    def get_input(self, entry):
        inp = entry.get()
        print("Введенное значение:", inp)
        self.delete_one(ID=inp)
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
                print("removed one")
            else:
                curs.execute(f"""DELETE FROM STORAGE WHERE ID = {str(ID)})""")
                print("removed element")
                con.commit()
                con.close()
                self.destroy()
        except:
            print(f"Probably, var with ID={ID} does not exist")
            self.destroy()
#######################################################################################################################

class Item:
    def __init__(self, ID, type, name, model, length, width, height, count):
        print("class created")
        self.ID = ID
        self.type = type; self.name = name; self.model = model
        self.length = length; self.width = width; self.height = height
        self.count = count
    @staticmethod
    def get_size(len, wid, hei):
        if ((wid + hei + len) > 600): return 'V'
        elif (len > 100 or wid > 100 or hei > 100): return 'L'
        elif ((len+wid+hei)>100 and (len+wid+hei) <= 300): return 'M'
        elif ((len+wid+hei)<=100): return 'S'
        else: return 'M'


#######################################################################################################################
'''
def new_base():
    address = simpledialog.askstring("Input", "Input name of new base:")
    if ('.db' not in address): address = address + '.db'
    try:
        con = sqlite3.connect(address)
        curs = con.cursor()
        curs.close(); con.close()
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

def get_address(main):
    global address
    address = filedialog.askopenfilename()

    try:
        con = sqlite3.connect(str(address))
        curs = con.cursor()
        curs.execute("""SELECT * FROM STORAGE""")
        curs.close()
        con.close()
        print("address is: ", address)
        return
    except:
        print("Something went wrong, let's create new database")
        address = new_base()
        return
    main.destroy()

def closeprog(root):
    root.destroy()
'''
class Get_file(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input()

    def input(self):
        #super().__init__(*args, **kwargs)
        self.title("Choosing type of work")
        self.resizable(False, False)
        self.focus_force()
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
            self.destroy()
        except:
            print("Something went wrong, let's create new database")
            address = self.new_base()
            self.destroy()

class Menu(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Choose what you wanna see:")
        self.resizable(False, False)
        tbl = DB(self)
        button_insert = tk.Button(self, text="Insert new", width=20, height=4, command=lambda: self.open_input()); button_insert.pack(anchor='n')
        button_delete = tk.Button(self, text="Delete one", width=20, height=4, command=lambda: self.del_one()); button_delete.pack(anchor='n')
        #butt_clearvar= tk.Button(self, text="Delete one", width=20, height=4, command=lambda:
        button_find   = tk.Button(self, text="Find  item", width=20, height=4, command=lambda: tbl.find   ()); button_find.pack(anchor='n')
        button_display= tk.Button(self, text="Show   all", width=20, height=4, command=lambda: tbl.display()); button_display.pack(anchor='n')
        turnoff =       tk.Button(self, text="Close", command=lambda: exit()); turnoff.pack(anchor='ne')
        self.attributes('-disabled',True)
        threading.Thread(target=Get_file).start()
    def open_input(self):
        tbl = DB(self)
        tbl.input()
    def del_one(self):
        tbl = DB(self)
        tbl.get_ID()
    def del_elem(self):
        tbl = DB(self)
        #tbl.del_elem()
    def find_db(self):
        tbl = DB(self)
        #tbl.rl_find()
    def show_db(self):
        tbl = DB(self)
        tbl.display()
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

#######################################################################################################################
if __name__ == '__main__':
    print_hi('PyCharm')
    #fil = Get_file()
    #fil.input()
    #fil.mainloop()
    prog = True
    while(prog):
        #root
        app = Menu()
        app.mainloop()
        prog = False



