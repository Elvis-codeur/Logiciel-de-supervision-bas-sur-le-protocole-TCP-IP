# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 21:51:58 2021

@author: Elvis
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

class MystandardItem(QStandardItem):
    def __init__(self,name):
        super().__init__()
        self.setText(name)
        
        
    def mouseDoubleClickEvent(self,event):
        print("Hello")
    
    def keyReleaseEvent(self,event):
        print("Elvis est un enfant de Dieu")
    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MystandardItem("elvis")
    w.show()
    sys.exit(app.exec_())