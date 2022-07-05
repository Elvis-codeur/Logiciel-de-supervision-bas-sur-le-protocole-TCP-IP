# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from email import header
from wsgiref import headers
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from mystandarditem import MystandardItem

class MyTableModel(QStandardItemModel):
    table_model_rowmodified = pyqtSignal(dict)
    def __init__(self,headers):
        
        super().__init__()
        self.headers = headers 
        self.set_headers(headers)
        self.itemChanged.connect(self.send_info)

    def send_info(self,item):
        
        # On récupère toute les items de la ligne 
        a = [self.item(item.row(),i).text() for i in range(4)]


        self.table_model_rowmodified.emit({
                                "row":item.row(),
                                "column":item.column(),
                                "value":item.text(),
                                "label": a[0],
                                "ip_address": a[1],
                                "port_number":a[2],
                                
                              })
        
    def set_headers(self,headers):
        for i in range(len(headers)):
            self.setHorizontalHeaderItem(i,MystandardItem(headers[i]))
            
    def m_append_row(self):
        a = list()
        for i in range(len(self.headers)):
            a.append(MystandardItem(""))
        return a
            
    def increase_row(self,item):
        if item.row() == (self.rowCount() -1):
            self.appendRow(self.m_append_row())
        
            
    def clear(self):
        self.clear()
        self.set_headers()
        
        