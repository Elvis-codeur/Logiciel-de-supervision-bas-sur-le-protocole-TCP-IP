import datetime
from ipaddress import ip_address
import threading
from apprendre_a_programmer_en_python.socket_server import SocketServer, ThreadClient
from constants import M_CATEGORIES, M_HEADERS
import sys 


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from my_pushbutton import MyPushButton
from my_timer import Timer

from mytableview import MyTableView
from regisiter_table_view import RegisterTableWidget
from export_data_widget import ExportDataWidget
import socket 


class ServerWidget(QMainWindow):
    server_started =pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        self.ip_adress = ""
        
        self.main_widget = QWidget()
        self.main_layout = QHBoxLayout()
        self.client_table = MyTableView(M_HEADERS)
        self.register_widget = RegisterTableWidget()

        self.export_widget = ExportDataWidget()

        self.client_dict = {}

        self.port_entry = QSpinBox()
        self.ip_entry = QLineEdit()
        self.connect_button = MyPushButton("Lancer",QColor.fromRgb(105,225,235))
        self.disconnect_button = MyPushButton("Arrêter",QColor.fromRgb(240,0,6))


        self.timer = Timer(0.5)
        
        self.init_UI()
        

    def init_UI(self):

        self.export_widget.setFixedSize(350,350)
        self.setMinimumSize(500,500)
        
        self.layout_1 = QVBoxLayout()
        self.layout_2 = QHBoxLayout()


        self.ip_entry.setPlaceholderText("IP Adress")
    
        self.port_entry.setToolTip("PORT number")
        self.port_entry.setValue(12800)
        self.port_entry.setRange(0,65000)
        self.port_entry.setValue(12800)
        self.port_entry.setMinimumWidth(75)
        
        # Connecton buttons and thier layouts
        self.connection_button_layout = QHBoxLayout()
        self.connection_button_layout.addWidget(self.connect_button)
        self.connection_button_layout.addWidget(self.disconnect_button)

        self.connect_button.setFixedSize(QSize(100,100))
        self.disconnect_button.setFixedSize(QSize(100,100))

        # Button and text edit 
        self.text_edit_and_button_layout = QVBoxLayout()

        self.connection_parmeter_widget_layout = QHBoxLayout()
        self.connection_parmeter_widget_layout.addWidget(self.ip_entry)
        self.connection_parmeter_widget_layout.addWidget(self.port_entry)

        self.text_edit_and_button_layout.addWidget(self.export_widget)
        self.text_edit_and_button_layout.addLayout(self.connection_parmeter_widget_layout)
        
        
        self.layout_1.addLayout(self.text_edit_and_button_layout)
        self.layout_1.addLayout(self.connection_button_layout)


        self.main_layout.addLayout(self.layout_1)
        
        self.main_layout.addWidget(self.register_widget)
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

        self.connect_button.clicked.connect(self.create_server)
        self.register_widget.data_modified.connect(self.handle_client_modification)

        self.timer.signal.connect(self.save_client_data)
        self.timer.start()


    def handle_client_modification(self,data):
        # Envoie de nouvelle donnée vers le client spécifié 
        self.server.send_data(str(data),(data["ip_address"],int(data["port_number"])))


    def add_client(self,data):
        self.client_table.append_row(data)

    def add_client_from_dict(self,data):
        self.client_dict[data["label"]] = data

        if data["type"] == "Coils":
            self.register_widget.add_coil(data)
        elif data["type"] == "Discrete Inputs":
            self.register_widget.add_discrete_input(data)
        elif data["type"] == "Input Registers":
            self.register_widget.add_input_register(data)
        elif data["type"] == "Holding Registers":
            self.register_widget.add_holding_register(data)


    def save_client_data(self):
        #print("we are to save")
        """Récolte les données et l'envoie à l'export """
        time_str =str( datetime.datetime.now())
        l = []
        for label in self.client_dict.keys():
            data = self.client_dict.get(label)
            l.append(time_str)
            l.append(data.get("label"))
            l.append(data.get("ip_address"))
            l.append(data.get("port_number"))
            l.append(data.get("type"))
            l.append(str(self.get_client_value(label)))
            self.export_widget.write_data(l)
            l = []



    # Méthode proposé pour la programmation
    def get_client_value(self,label):
        if label in self.client_dict.keys():
            data = self.client_dict[label]
            return self.server.get_client_value(
                (data["ip_address"],int(data["port_number"]))
                )
        else:
            return "label_error"

    def set_client_value(self,label,value):
        #print("attemps set")
        if label in self.client_dict.keys():
            data = self.client_dict[label]
            return self.server.set_client_value(
                (data["ip_address"],int(data["port_number"])),
                str(value)
                )
        else:
            return "label_error"

    def get_client_ip_address(self,label):
        if label in self.client_dict.keys():
            return self.client_dict.get(label).get("ip_adress")
        else:
            return "error"

    def get_client_port_number(self,label):
        if label in self.client_dict.keys():
            return self.client_dict.get(label).get("port_number")
        else:
            return -1

    def get_client_type(self,label):
        if label in self.client_dict.keys():
            return self.client_dict.get(label).get("type")
        else:
            return -1

    # Fin des méthodes

    def exec_code(self,source_code):
        if(source_code == ""):
            return 

        method = {"ip_address":"self.get_client_ip_address",
                    "port_number":"self.get_client_port_number",
                    "_type":"self.get_client_type",
                    "get_value":"self.get_client_value",
                    "set_value":"self.set_client_value"}
        
        # On change les méthodes macro fournie par d'autres
        for i in method.keys():
            source_code = source_code.replace(i,method.get(i))

        is_compiled = False
        try:
            compiled = compile(source_code,"debug.txt","exec")
            is_compiled = True 
        except Exception as e:
            print("Exeception ----- compilation ----",e)

            
        if is_compiled:
            try:
                exec(compiled)
            except Exception as e:
                print("Exeception ----- execution ----",e)


    def closeEvent(self, event) -> None:
        self.server.close()


    def create_server(self):
        self.ip_address = self.ip_entry.text()
        self.port_number = self.port_entry.value()

        # Si le serveur est absent 
        if "server" not in self.__dict__.keys():
            self.server = SocketServer(self.ip_address,self.port_number)
            self.server.start()


        #print(self.__dict__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ServerWidget()
    w.show()
    sys.exit(app.exec_())