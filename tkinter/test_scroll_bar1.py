from argparse import _MutuallyExclusiveGroup
import imp
from msilib.schema import ListBox
from tkinter import *

root = Tk()

scrollbar = Scrollbar(root)
scrollbar.pack(side = RIGHT, fill = Y)


mylist = Listbox(root,yscrollcommand = scrollbar.set)

for line in range(100):
    mylist.insert(END,"This  {}".format(line))

mylist.pack(side = LEFT,fill = BOTH)
scrollbar.config(command = mylist.yview)

mainloop()