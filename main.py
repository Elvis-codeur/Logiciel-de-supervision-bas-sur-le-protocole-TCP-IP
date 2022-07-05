from client_widget import ClientWidget
from main_widget import MainWidget
from server_widget import ServerWidget

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

from supervision_widget import DrawingWiget, SupervisionWidget 

class MainObject(QApplication):
    def __init__(self,argv) -> None:
        super().__init__(argv)
        self.client_widget = ClientWidget()
        self.server_widget = MainWidget()
        self.supervition_widget = SupervisionWidget()
     

    def init_UI(self):
        self.client_widget.send_client_info.connect(self.server_widget.server_widget.add_client_from_dict)
        self.supervition_widget.send_info.connect(self.server_widget.server_widget.add_client_from_dict)
        self.supervition_widget.show()
        self.server_widget.show()
        #self.client_widget.show()
       
        


if __name__ == "__main__":
    a = MainObject(sys.argv)
    a.init_UI()
    sys.exit(a.exec_())