from pickle import FALSE
from tkinter import filedialog
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

from sympy import false 

class MyTextEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.font = QFont("Consolas",pointSize=14)

        self.setFont(self.font)


class TextEditingWidget(QMainWindow):
    def __init__(self,widget_parent):
        super().__init__()

        self.file_name = ""
        # Si le code est sauvegardé
        self.saved = True 
        # Si on le code est dans un fichier
        self.has_file = False

        self.widget_parent = widget_parent

        self.text_editor = MyTextEditor()
        self.code_output = QPlainTextEdit()
        self.code_output.setReadOnly(True)
        self.code_output.setMaximumHeight(self.height()//3)
        

        self.menu_fichier =  self.menuBar().addMenu("Fichier")
        self.menu_code = self.menuBar().addMenu("Code")

        self.toolbar = self.addToolBar("Fichier")


        self.init_UI()

    def init_UI(self):

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.text_editor)
        self.main_layout.addWidget(self.code_output)

        # The main widget
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        # Play 
        self.play_action = QAction(QIcon("images/play.png"),"Executer",self)
        self.toolbar.addAction(self.play_action)
        self.menu_code.addAction(self.play_action)
        self.play_action.triggered.connect(self.widget_parent.exec_code)
        
        self.toolbar.addSeparator()

        # Ouvrir
        self.open_action = QAction(QIcon("images/open.png"),"Ouvrir",self)
        self.toolbar.addAction(self.open_action)
        self.menu_fichier.addAction(self.open_action)
        self.open_action.triggered.connect(self.open_file)

        # Enrégistrer
        self.save_action = QAction(QIcon("images/save.png"),"Enrégistrer",self)
        self.toolbar.addAction(self.save_action)
        self.menu_fichier.addAction(self.save_action)
        self.save_action.triggered.connect(self.save_file)
        
        self.text_editor.textChanged.connect(self.set_save_state)
        self.setCentralWidget(self.main_widget)

    def set_save_state(self):
        self.saved = False

    def save_file(self):
        if self.has_file:
            f = open(self.file_name,"w")
            f.write(self.toPlainText())
            f.close()    
            self.saved = True

        else:
            file_dialog = QFileDialog.getSaveFileName(self,"Ouvrir un fichier",str(),"*.py")
            if(file_dialog[0]):
                self.file_name = file_dialog[0]
                f = open(self.file_name,"w")
                f.write(self.toPlainText())
                f.close()
                self.has_file = True 
                self.saved = True

    
    def open_file(self):
        file_dialog = QFileDialog.getOpenFileName(self,"Ouvrir un fichier",str(),"*.py")

        if(file_dialog[0]):
            self.file_name = file_dialog[0]
            f = open(self.file_name,"r")
            self.setPlainText(f.read())
            f.close()
            self.has_file = True 
            self.saved = True

    def setPlainText(self,text):
        self.text_editor.setPlainText(text)

    def toPlainText(self):
        return self.text_editor.toPlainText()

    def set_output(self,output):
        self.code_output.setPlainText(output)


    def closeEvent(self, event) -> None:
        if not self.saved:
            self.save_file()


        return super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TextEditingWidget()
    w.show()
    sys.exit(app.exec_())