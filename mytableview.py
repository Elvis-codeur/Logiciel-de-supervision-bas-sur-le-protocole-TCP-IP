# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:46:09 2020

@author: elvis
"""
import sys
from wsgiref.headers import Headers 


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from constants import M_HEADERS

from mytablemodel import MyTableModel

class MyTableView(QTableView):
    table_view_rowmodified = pyqtSignal(dict)
    def __init__(self,headers):
        super().__init__()

        self.headers = headers
        self.table_model = MyTableModel(headers=headers)
        self.table_model.table_model_rowmodified.connect(self.table_view_rowmodified)
     
        self.init_UI()



    def set_item(self,text,row,column):
        #Modifie la cellule à la ligne row et à column column
        print("text--river--",text)
        self.table_model.setItem(row,column,QStandardItem(text))


    def printmodrow(self,dic):
        print(dic)

    def init_UI(self):
        self.setModel(self.table_model)

    def append_row(self,itterable):
        self.table_model.appendRow(itterable)

    def get_data(self):
        generalList = []
        rowCount = self.table_model.rowCount(QModelIndex())

        for i in range(rowCount):
            l =[]
            for u in range(len(self.headers)):
                l.append(self.table_model.item(i,u).text())
            generalList.append(l)
        
        print(generalList)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_view = MyTableView(M_HEADERS)
    table_model = MyTableModel(M_HEADERS)
    table_view.setModel(table_model)

    widget = QWidget()
    layout = QHBoxLayout()
    layout.addWidget(table_view)
    widget.setLayout(layout)
    widget.show()

    sys.exit(app.exec())