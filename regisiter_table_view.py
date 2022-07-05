import sys 

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from my_pushbutton import MyPushButton
from mystandarditem import MystandardItem

from mytableview import MyTableView


class RegisterTableWidget(QWidget):
    data_modified = pyqtSignal(dict)
    def __init__(self) -> None:
        super().__init__()

        self.main_layout = QHBoxLayout()
        self.main_widget = QTabWidget()
        self.coils_register_widget = MyTableView(["Label","IP","PORT","Value"])
        self.discrete_input_widget = MyTableView(["Label","IP","PORT","Value"])
        self.input_register_widget = MyTableView(["Label","IP","PORT","Value"])
        self.holding_register_widget = MyTableView(["Label","IP","PORT","Value"])
        
        self.init_UI()


    def add_coil(self,data):
        self.coils_register_widget.append_row([MystandardItem(str(data[i])) for i in data.keys() if i != "type"])

    def add_discrete_input(self,data):
        self.discrete_input_widget.append_row([MystandardItem(str(data[i])) for i in data.keys() if i != "type"])

    def add_input_register(self,data):
        self.input_register_widget.append_row([MystandardItem(str(data[i])) for i in data.keys() if i != "type"])

    def add_holding_register(self,data):
        self.holding_register_widget.append_row([MystandardItem(str(data[i])) for i in data.keys() if i != "type"])


    def init_UI(self):
        self.main_widget.addTab(self.coils_register_widget,"Coil register")
        self.main_widget.addTab(self.discrete_input_widget,"Discrete Input")
        self.main_widget.addTab(self.input_register_widget,"Input Register")
        self.main_widget.addTab(self.holding_register_widget,"Holding Register")

        self.main_layout.addWidget(self.main_widget)

        self.setLayout(self.main_layout)

        self.coils_register_widget.table_view_rowmodified.connect(self.data_modified)
        self.input_register_widget.table_view_rowmodified.connect(self.data_modified)
        self.discrete_input_widget.table_view_rowmodified.connect(self.data_modified)
        self.holding_register_widget.table_view_rowmodified.connect(self.data_modified)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = RegisterTableWidget()
    w.show()
    sys.exit(app.exec_())