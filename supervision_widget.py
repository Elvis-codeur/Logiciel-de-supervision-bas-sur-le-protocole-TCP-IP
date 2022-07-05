from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


import sys

from numpy import object_

from drawing_object import InterrupteurImage, MotorImage, Slider
from my_timer import Timer



class DrawingWiget(QWidget):
    send_info = pyqtSignal(dict)
    def __init__(self):
        super().__init__()

        self.painter = QPainter()

        self.drawed_objects = []

        self.timer = Timer(0.5)
        self.timer.signal.connect(self.animate)
        self.timer.start()

        self.can_animate = False
        self.move_slider = False

        self.previous_mouse_move_x = 0
        self.previous_mouse_move_y = 0
        self.mouse_move_first_time = True 

        #self.main_layout = QHBoxLayout()
        #self.main_layout.addWidget(self.drawing_scene)

        #self.setLayout(self.main_layout)



        self.drawed_objects =[
            {
                "position" : QRect(50,50,100,100),
                "object": MotorImage("images/motor.jpg")
            },
            {
                "position" : QRect(160+50,160+50,100,100),
                "object": InterrupteurImage("images/interrupteur_bas.jpg",
                "images/interrupteur_haut.jpg",0)
            },
            {
                "position" : QRect(200,200,100,100),
                "object": InterrupteurImage("images/interrupteur_bas.jpg",
                "images/interrupteur_haut.jpg",0)
            },
            {
                "position" : QRect(100,100,100,50),
                "object": Slider(100,100,100,50)
            }
        ]

        for i in self.drawed_objects:
            i.get("object").signal_emmiter.signal_emis.connect(self.send_info)

    def set_animation_state(self):
        """Décide si l'animation doit continuer ou pas."""
        self.can_animate = not self.can_animate


    def update_interrupteur(self,position):
        for i in self.drawed_objects:
            _object = i.get("object")
            if _object.type == "interrupteur":
                interrupeur_pos = i.get("position")
                if position[0] >= interrupeur_pos.x() and position[0] <= interrupeur_pos.x()+interrupeur_pos.width():
                    _object.change_etat("1")
                else:
                    _object.change_etat("0")

    def animate(self):
        #print("We are to animate")
        if self.can_animate:
            for i in self.drawed_objects:
                _object = i.get("object")
                if _object.type == "slider":
                    position = (_object.x,_object.y,_object.width,_object.height)
                    self.update_interrupteur(position)

                    if(self.move_slider):
                        _object.move(15)


                    self.update()
                    self.repaint()
                elif _object.type == "interrupteur":
                    _object.update()

                elif _object.type == "motor":
                    #print("motor value ",_object.get_value())
                    if _object.get_value() == "1":
                        self.move_slider = True 
                    else:
                        self.move_slider = False 



                
    
    def paintEvent(self, event) -> None:

        self.brush = QBrush(QColor.fromRgb(0,0,200),Qt.VerPattern)
        self.pen = QPen(QColor.fromRgb(100,100,0),20,Qt.SolidLine)
        
        self.painter.begin(self)
        self.painter.setBrush(self.brush)
        self.painter.setPen(self.pen)
        

        for i in self.drawed_objects:
            if i.get("object").type == "slider":
                ob = i.get("object")
                self.painter.drawPolygon(QPolygon([
                    QPoint(ob.x,ob.y),
                    QPoint(ob.x+ ob.width,ob.y),
                    QPoint(ob.x+ ob.width,ob.y+ob.height),
                    QPoint(ob.x,ob.y+ob.height),
                ]))
            else:
                self.painter.drawImage(i.get("position"),i.get("object"))

        self.painter.end()
        return super().paintEvent(event)
        

    def mouseDoubleClickEvent(self, event) -> None:
        position = (event.x(),event.y())

        object_double_clicked = 0
        for i in self.drawed_objects:
            if self.is_in_rect(position,i.get("position")):
                object_double_clicked = i
                break

        if object_double_clicked:
            """
            if(object_double_clicked.get("object").type =="interrupteur"):
                object_double_clicked.get("object").change_etat(1)
                self.update()
                self.repaint()
            """
            if object_double_clicked.get("object").type != "slider":
                object_double_clicked.get("object").show_dialog_widget()



        return super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event) -> None:
        position = (event.x(),event.y())

        object_to_move = 0
        for i in self.drawed_objects:
            if self.is_in_rect(position,i.get("position")):
                object_to_move = i
                break

        if object_to_move:
            if(object_to_move.get("object").type == "slider"):
                object =  object_to_move.get("object")
                width = object.width
                heigt = object.height

                object_position =  object_to_move.get("position")
                object_position.setX(position[0]-20)
                object_position.setY(position[1]-20)
                object_position.setWidth(width)
                object_position.setHeight(heigt)


                object.setX(position[0]-20)
                object.setY(position[1]-20)
                object.setWidth(width)
                object.setHeight(heigt)

               

            else:

                object_position =  object_to_move.get("position")
                width = object_position.width()
                heigt = object_position.height()

                object_position.setX(position[0]-30)
                object_position.setY(position[1]-30)
                object_position.setWidth(width)
                object_position.setHeight(heigt)

            self.update()
            self.repaint()
        else:
            print("failed")       


        return super().mouseMoveEvent(event)


    def is_in_rect(self,position,rect):

        if position[0] >= rect.x() and position[0] <= rect.x()+rect.width() and \
            position[1] >= rect.y() and position[1] <= rect.y()+ rect.height():
            return True 

        else:
            return False 




class SupervisionWidget(QWidget):
    send_info = pyqtSignal(dict)
    def __init__(self):
        super().__init__()

        self.drawing_widget = DrawingWiget()
        self.main_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()

        self.start_button = QPushButton("Commencer")
        self.stop_button = QPushButton("Arrêter")

        self.drawing_widget.send_info.connect(self.send_info)
        self.start_button.clicked.connect(self.drawing_widget.set_animation_state)
        self.init_UI()


    def init_UI(self):
        self.setGeometry(50,50,1200,600)
        self.main_layout.addWidget(self.drawing_widget)

        self.button_layout.addWidget(self.start_button)
        self.button_layout.addWidget(self.stop_button)

        self.main_layout.addLayout(self.button_layout)

        self.setLayout(self.main_layout)

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SupervisionWidget()
    
    w.show()
    sys.exit(app.exec_())
