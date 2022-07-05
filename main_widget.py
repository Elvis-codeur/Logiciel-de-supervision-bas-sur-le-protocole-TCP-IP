from client_widget import ClientWidget
from my_timer import Timer
from server_widget import ServerWidget

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

from text_editor import MyTextEditor, TextEditingWidget 


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.main_widget  = QWidget()
        self.main_layout = QHBoxLayout()

        self.tab_widget = QTabWidget()
        self.server_widget = ServerWidget()
        self.text_editor = TextEditingWidget(self)

        self.init_UI()                                                                                                                                   

    def exec_code(self):
        #print("exec")
        code_source = self.text_editor.toPlainText()
        self.server_widget.exec_code(code_source)

    def init_UI(self):
        
        self.tab_widget.addTab(self.server_widget,"Régistre")
        self.tab_widget.addTab(self.text_editor,"Editor")

        self.main_layout.addWidget(self.tab_widget)

        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)


       
    def closeEvent(self, a0) -> None:
        self.text_editor.closeEvent(a0)
        return super().closeEvent(a0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec_())