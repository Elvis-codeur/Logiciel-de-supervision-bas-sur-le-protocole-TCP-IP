
from ipaddress import ip_address
from apprendre_a_programmer_en_python.socket_client import SocketClient

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

from constants import M_CATEGORIES

class DialogWidget(QObject):
    finished_signal = pyqtSignal()
    def __init__(self) -> None:
        super().__init__()
        
        self.ip_address = ""
        self.port_number = 0

        self.dialog_widget = QDialog()

        self.init_UI()



    def init_UI(self):
        self.form_layout = QFormLayout()
        self.ip_adress_entry = QLineEdit()
        self.ip_adress_entry.setText("localhost")
        
        self.port_number_entry = QSpinBox()
        self.port_number_entry.setRange(1500,65000)
        self.port_number_entry.setValue(12800)

        self.label_line_edit = QLineEdit()
        self.type_combobox = QComboBox()
        self.type_combobox.addItems(M_CATEGORIES)
        self.ok_button = QPushButton("Ok")


        self.form_layout.addRow("Adresse IP",self.ip_adress_entry)
        self.form_layout.addRow("Numéro de port",self.port_number_entry)
        self.form_layout.addRow("Label",self.label_line_edit)
        self.form_layout.addRow("Type",self.type_combobox)
        self.form_layout.addRow("Terminer",self.ok_button)

        self.ok_button.clicked.connect(self.dialog_widget.done)
        self.dialog_widget.finished.connect(self.set_information)
        self.dialog_widget.finished.connect(self.finished_signal)

        self.dialog_widget.setLayout(self.form_layout)

        


    def show_dialog_widget(self):
        """Affiche un Qdialog pour recevoir les infos nécessaire 
            ip_address
            port_number
        """
        self.dialog_widget.show()

    def set_information(self,value):
        self.ip_address = self.ip_adress_entry.text()
        self.port_number = self.port_number_entry.value()
        self.label = self.label_line_edit.text()
        self._type = self.type_combobox.currentText()

    def get_information(self):
        return self.ip_address, self.port_number,self.label,self._type


class MotorImage(QImage):
    def __init__(self,file_path):
        super().__init__(file_path)
        self.type = "motor"

        self.signal_emmiter = SignalEmitter()

        self.dialog_widget = DialogWidget()
        self.dialog_widget.finished_signal.connect(self.connect)


    def show_dialog_widget(self):
        self.dialog_widget.show_dialog_widget()

    def get_value(self):
        return self.socket_client.get_value()

    def connect(self):
        _ip_address,port_number,label,_type = self.dialog_widget.get_information()

        self.socket_client = SocketClient(ip_adress=_ip_address,
                                        port_number=port_number,
                                        type_=_type,
                                        value="0",
                                        label=label)

        self.socket_client.start()
    
        socket_info = self.socket_client.get_socket_info()
                
        self.signal_emmiter.send_info({"label":label,
                                        "ip_address":socket_info[0],
                                        "port_number":str(socket_info[1]),
                                        "value":"0",
                                        "type":_type,
                                        })
     
class InterrupteurImage(QImage):
    
    def __init__(self,low_file_path,height_file_path,etat):
        super().__init__(height_file_path)

        self.signal_emmiter = SignalEmitter()

        self.type = "interrupteur"

        self.low_file_path = low_file_path
        self.heigt_file_path = height_file_path
        self.etat = etat
        
        

        self.dialog_widget = DialogWidget()

        self.dialog_widget.finished_signal.connect(self.connect)
    def show_dialog_widget(self):
        self.dialog_widget.show_dialog_widget()

    def connect(self):
        _ip_address,port_number,label,_type = self.dialog_widget.get_information()

        self.socket_client = SocketClient(ip_adress=_ip_address,
                                        port_number=port_number,
                                        type_=_type,
                                        value="0",
                                        label=label)

        self.socket_client.start()
    
        socket_info = self.socket_client.get_socket_info()
                
        self.signal_emmiter.send_info({"label":label,
                                        "ip_address":socket_info[0],
                                        "port_number":str(socket_info[1]),
                                        "value":"0",
                                        "type":_type,
                                        })

    def update(self):
        self.etat = self.socket_client.get_value()
        if self.etat == "0":
            self.load(self.heigt_file_path)
        else:
            self.load(self.low_file_path)

    def change_etat(self,state):
        self.etat = state
        self.socket_client.set_value(str(state))
        if state == "0":
            self.load(self.heigt_file_path)
        else:
            self.load(self.low_file_path)

class Slider():
    def __init__(self,x,y,width,height) -> None:
        
        self.move_step = 5
        self.x = x 
        self.y = y 
        self.width = width
        self.height = height

        self.signal_emmiter = SignalEmitter()

        self.type = "slider"
        
        
    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y 

    def setWidth(self,width):
        self.width = width 

    def setHeight(self,height):
        self.height = height

    def move(self,move_step):
        self.move_step = move_step
        self.x += self.move_step

    


class SignalEmitter(QObject):
    signal_emis = pyqtSignal(dict)
    def __init__(self):
        super().__init__()



    def send_info(self,info):
        self.signal_emis.emit(info)
if __name__ == "__main__":
    """"""