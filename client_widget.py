
from email import message
from multiprocessing.connection import Client
from constants import M_CATEGORIES, M_HEADERS, TRANSACTION_ID
import sys 


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from my_pushbutton import MyPushButton
from mystandarditem import MystandardItem
from my_timer import Timer
from mytableview import MyTableView

from  apprendre_a_programmer_en_python.socket_client import ThreedReception, TheadEmission,SocketClient

import socket


class ClientWidget(QMainWindow):
    send_client_info =pyqtSignal(dict)
    def __init__(self) -> None:
        super().__init__()

        self.timer = Timer(0.5)

        self.compteur_client = 0
        self.compteur_iteration = 0
        self.client_info = {}

        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.client_table = MyTableView(M_HEADERS)

        self.previous_value = []

        self.port_entry = QSpinBox()
        self.ip_entry = QLineEdit()
        self.label_entry = QLineEdit()
        self.type_combobox = QComboBox()
        self.add_client_button = QPushButton("Ajouter")
        self.connect_button = MyPushButton("Connect",QColor.fromRgb(105,225,235))
        self.disconnect_button = MyPushButton("Disconnect",QColor.fromRgb(240,0,6))

        self.init_UI()
  
        

    def init_UI(self):
        self.setMinimumSize(500,500)
        
        self.layout_1 = QVBoxLayout()
        self.layout_1.addWidget(self.client_table)

        self.layout_2 = QHBoxLayout()


        self.ip_entry.setPlaceholderText("IP")
        self.ip_entry.setText("localhost")
        self.port_entry.setRange(1024,65000)
        self.port_entry.setValue(12800)
        self.port_entry.setMinimumWidth(100)
        self.label_entry.setPlaceholderText("Label(unique)")
        
        # Connecton buttons and thier layouts
        self.connection_button_layout = QHBoxLayout()
        self.connection_button_layout.addWidget(self.connect_button)
        self.connection_button_layout.addWidget(self.disconnect_button)

        self.connect_button.setFixedSize(QSize(100,100))
        self.disconnect_button.setFixedSize(QSize(100,100))
        

        self.connection_parmeter_widget_layout = QHBoxLayout()
        self.connection_parmeter_widget_layout.addWidget(self.ip_entry)
        self.connection_parmeter_widget_layout.addWidget(self.port_entry)

        
        
        self.type_combobox.addItems(M_CATEGORIES)

        self.layout_2.addWidget(self.label_entry)
        
        self.layout_2.addWidget(self.type_combobox)
        self.layout_2.addWidget(self.add_client_button)
    
        
        self.layout_1.addLayout(self.layout_2)
        self.layout_1.addLayout(self.connection_parmeter_widget_layout)
       


        self.main_layout.addLayout(self.layout_1)
        
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.add_client_button.clicked.connect(self.add_client)
        self.connect_button.clicked.connect(self.connect)
  

        self.client_table.table_view_rowmodified.connect(self.handle_client_modification)
        #self.timer.signal.connect(self.handle_client_modification)
        #self.timer.start()

    def add_client(self):

        
        ip_address = self.ip_entry.text()
        port_number = self.port_entry.value()
        label = self.label_entry.text()
        type_ = self.type_combobox.currentText()
        value = "1"

        if(label in self.client_info.keys()):
            return 

        try:
            
            a = SocketClient(ip_adress= ip_address,
                            port_number= port_number,
                            label=label,
                            value=value,
                            type_= type_)
            
            a.start()

            socket_info = a.get_socket_info()
            
            self.client_info[label] = \
            {
                "ip":ip_address,
                "port":port_number,
                "client":a
                
            }
            self.compteur_client += 1
            self.send_client_info.emit({"label":label,
                                        "ip_address":socket_info[0],
                                        "port_number":str(socket_info[1]),
                                        "value":value,
                                        "type":type_,
                                        })


            data = []
            data.append(MystandardItem(label))
            data.append(MystandardItem(socket_info[0]))
            data.append(MystandardItem(str(socket_info[1])))
            data.append(MystandardItem(type_))
            data.append(MystandardItem(value))

            self.client_table.append_row(data)


        except Exception as e:
            print(e)


    def handle_client_modification(self,data):
        """ 
        Modifie le client correspondant à la ligne
        On récupère du dictionnaire le dictionnaire associé au label et on impose 
            la nouvelle valeur au client 
        """
        self.client_info[data.get("label")].get("client").set_value(data.get("value"))
        """
        compteur = 0

        for i in self.client_info.keys():
            client = self.client_info[i].get("client")
            value =  client.get_value()
            label = client.get_label()

            if self.compteur_iteration == 0:
                self.previous_value.append(value)
                self.client_table.set_item(str(value),compteur,len(M_HEADERS)-1)
                self.compteur_iteration += 1
            else:
                for i in self.previous_value:
                    if i != value:
                        print("modification")
                        self.previous_value.index(value)
                        self.client_table.set_item(str(value),compteur,len(M_HEADERS)-1)

            compteur += 1
        """




                      
        

    def connect(self):
        self.client_table.get_data()

    def closeEvent(self, event) -> None:
       
        return super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ClientWidget()
    w.show()
    sys.exit(app.exec_())