
from cmath import inf
from tkinter import *

from matplotlib.pyplot import grid

class Application(object):
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("Fenêtre du client Modbus")

        self.ip_entry_label = Label(self.root,text = "L'adresse IP")
        self.ip_entry_label.grid(row =1, column= 1,columnspan=3)

        self.port_entry_label = Label(self.root,text = "Port")
        self.port_entry_label.grid(row = 1,column=4,columnspan=3)


        self.ip_entree = Entry(self.root,width=14)
        self.ip_entree.grid(row = 3,column=1)

        self.port_entree = Entry(self.root,width=10)
        self.port_entree.grid(row = 3,column= 5) 

        self.entre_button = Button(self.root,text="Ok",command=self.set_ip_address,width=25)
        self.entre_button.grid(row = 4,column=1)
        self.root.mainloop()

    def set_ip_address(self):
        a  = 0
        print("elvis")

if __name__ =="__main__":
    f = Application()
