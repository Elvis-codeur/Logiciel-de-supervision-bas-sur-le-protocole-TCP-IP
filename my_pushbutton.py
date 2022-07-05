import imp
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys 


class MyPushButton(QPushButton):
    def __init__(self,text = "",color = ""):
        super().__init__(text)
        self.color = color
        self._text = text
        


    def paintEvent(self,event) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(QColor(self.color))
        painter.setFont(QFont("Consolas",12))
        size = self.size()
        painter.drawRect(0,0,size.width(),size.height())
        painter.drawText(QRectF(10,size.height()/2-10,size.width(),size.height()),self._text)
        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyPushButton(text="Connect",color="Green")
    w.show()
    sys.exit(app.exec())
        