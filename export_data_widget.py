from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sqlite3
import sys 


class ExportDataWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.database_checkbox = QCheckBox()
        self.csv_checkbox = QCheckBox()

        self.create_database_file_button = QPushButton("Nouveau")
        self.open_existing_csv_file_button = QPushButton("Ouvrir")

        self.open_existing_database_file_button = QPushButton("Ouvrir")
        self.create_csv_file_button = QPushButton("Nouveau")


        self.database_path_line_edit = QLineEdit()
        self.csv_path_button_line_edit = QLineEdit()

        self.main_layout = QFormLayout()

        self.database_file_path = ""
        self.csv_file_path = ""

        # Les booléen pour activer ou désactiver l'écriture
        self.write_csv = False 
        self.write_database = False

        self.init_UI()

    def open_existing_csv_file(self):
        file_dialog  = QFileDialog.getOpenFileName(self,"Ouvrir un fichier",str(),"*.csv")
        if(file_dialog[0]):
            self.csv_file_path = file_dialog[0]
            self.csv_path_button_line_edit.setText(self.csv_file_path)

    def open_existing_database_file(self):
        file_dialog  = QFileDialog.getOpenFileName(self,"Ouvrir un fichier",str(),"*.sqlite3")
        if(file_dialog[0]):
            self.database_file_path = file_dialog[0]
            self.database_path_line_edit.setText(self.database_file_path)


    def create_csv_file(self):
        file_dialog  = QFileDialog.getSaveFileName(self,"Ouvrir un fichier",str(),"*.csv")
        if(file_dialog[0]):
            self.csv_file_path = file_dialog[0]
            f = open(self.csv_file_path,"w")
            f.write("")
            f.close()
            self.csv_path_button_line_edit.setText(self.csv_file_path)

    def create_database_file(self):
        file_dialog  = QFileDialog.getSaveFileName(self,"Ouvrir un fichier",str(),"*.sqlite3")
        if(file_dialog[0]):
            self.database_file_path = file_dialog[0]

            self.database_connexion = sqlite3.connect(self.database_file_path)
            self.database_cursor = self.database_connexion.cursor()

            requete1 = """CREATE TABLE IF NOT EXISTS donnees(id
                            INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                            datetime TEXT,
                            label TEXT,
                          ip_address TEXT,
                          port_number TEXT,
                          type TEXT,
                           value TEXT)"""

            try:
                self.database_cursor.execute(requete1)
            except Exception as e:
                print(e)


    def write_data(self,data):
        
        """ Recois les donnée et décide si il doit les enrégister au format 
        csv ou dans une base de données"""
        if self.write_csv:
            self.csv_write(data)

        if self.write_database:
            self.database_write(data)

    def csv_write(self,data):
        """Reçois un tableau de donnée et les écris dans le fichier
        Le fichier est considéré comme existant déjà"""

        if self.write_csv:
            f = open(self.csv_file_path,"a")
            f.write(",".join(data)+"\n")
            f.close()


    def database_write(self,data):
        self.database_connexion = sqlite3.connect(self.database_file_path)
        self.database_cursor = self.database_connexion.cursor()


        if self.write_database:
            requete = """INSERT INTO donnees (datetime, label, ip_address,port_number,type,value)
                        VALUES (?,?,?,?,?,?)"""

            try:
                self.database_cursor.execute(requete,data)
                self.database_connexion.commit()

            except Exception as e:
                print(e)
        print("database written")




    def init_UI(self):
        
        database_layout = QHBoxLayout()
        database_layout.addWidget(self.database_path_line_edit)
        database_layout.addWidget(self.create_database_file_button)
        database_layout.addWidget(self.open_existing_database_file_button)
        database_layout.addWidget(self.database_checkbox)

        csv_layout = QHBoxLayout()
        csv_layout.addWidget(self.csv_path_button_line_edit)
        csv_layout.addWidget(self.create_csv_file_button)
        csv_layout.addWidget(self.open_existing_csv_file_button)
        csv_layout.addWidget(self.csv_checkbox)

        self.main_layout.addRow("SQL",database_layout)
        self.main_layout.addRow("CSV",csv_layout)


        self.setLayout(self.main_layout)

        self.open_existing_csv_file_button.clicked.connect(self.open_existing_csv_file)
        self.create_csv_file_button.clicked.connect(self.create_csv_file)

        self.create_database_file_button.clicked.connect(self.create_database_file)
        self.open_existing_database_file_button.clicked.connect(self.open_existing_database_file)

        self.csv_checkbox.stateChanged.connect(self.enable_csv_writing)
        self.database_checkbox.stateChanged.connect(self.enable_database_writing)

    def enable_csv_writing(self,value):
        print("---------",value)
        if(value ==  0):
            self.write_csv = False
        else:
            if self.csv_file_path:
                self.write_csv = True
            else:
                self.create_csv_file()

    def enable_database_writing(self,value):
        if(value == 0):
            self.write_database = False 
        else:
            if self.database_file_path:
                self.write_database = True 
            else:
                self.create_database_file()


if __name__ == "__main__":
    app  = QApplication(sys.argv)
    w = ExportDataWidget()
    w.show()
    sys.exit(app.exec_())