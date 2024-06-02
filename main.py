import sqlite3
import tkinter as tk

class Item:
    def __init__(self, ID, type, name, model, length, width, height, count, size):
        print("class created")
        self.ID = ID
        self.type = type; self.name = name; self.model = model
        self.length = length; self.width = width; self.height = height
        self.count = count
    def get_size(self, len, wid, hei):
        if ((wid + hei + len) > 600): return 'V'
        elif (len > 100 or wid > 100 or hei > 100): return 'L'
        elif ((len+wid+hei)>100 and (len+wid+hei) <= 300): return 'M'
        elif ((len+wid+hei)<=100): return 'S'
        else: return 'M'

    def insert(self, curs, sq):
        print("\nID      = "); ID = int(input())
        print("\nTYPE    = "); type = str(input())
        print("\nNAME    = "); name = str(input())
        print("\nMODEL   = "); model = str(input())
        print("\nLENGTH  = "); length = str(input())
        print("\nWIDTH   = "); width = float(input())
        print("\nHEIGHT  = "); height = float(input())
        print("\nCOUNT   = "); count = int(input())
        it = Item(ID=ID, type=type,name=name,model=model,length=length,width=width,height=height,
              count=count,size=Item.get_size(len=length,width=width,height=height))
        #it.__init__(ID, type, name, model, length, width, height, count)
        it.__init__()
        inp = ("INSERT INTO STORAGE VALUES("+\
              str(it.ID)+", '"+it.type+"', '"+it.name+"', '"+\
              it.model+"', "+it.get_size(length, width, height)+", "+\
              str(it.length)+", "+str(it.width)+", "+str(it.height)+\
              ", "+str(it.count)+");")
        curs.execute(inp)

    def find(curs, id):
        curs.execute(f"SELECT * FROM STORAGE WHERE ID = {str(id)}")
        res = curs.fetchone()
        print(res)
        return res

    def delete(curs, id):
        count = Item.find(curs, id)
        return 0

#################################################################################################

def get_address():
    address = ""
    return address

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.
prog = True
if __name__ == '__main__':
    print_hi('PyCharm')
    while(prog):
        #address = get_address()
        address = "Testbase.db"
        con = sqlite3.connect(address)
        curs = con.cursor()



