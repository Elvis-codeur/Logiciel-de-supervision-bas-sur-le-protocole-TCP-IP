from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


import socket, sys, threading,time 

class Timer(threading.Thread,QObject):
    signal = pyqtSignal()
    def __init__(self,sleep_time) -> None:
        self.sleep_time = sleep_time

    def run(self):
        while 1:
            time.sleep(self.sleep_time)
            self.signal.emit()

