from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from danmu import DanMuClient
import sys
import time
import socket
import os
import urllib
import urllib.request
from multiprocessing import Process, Queue
import threading 
import random

class Danmu(QLabel):
    font = QFont('SimHei',20,100)
    pe = QPalette()  
    pe.setColor(QPalette.WindowText,Qt.white)

    def __init__(self,parent,text,y=0,color=QColor(255,255,255)):
        super().__init__(text,parent)
        self.text = text
        self.parent = parent
        self.setFont(self.font)
        self.setposY(y)
        self.setcolor(color)
        self.setPalette(self.pe)
        self.anim2 = QPropertyAnimation(self,b'pos')
        self.anim2.setDuration(10000)
        self.anim2.setStartValue(QPoint(0,self.posY))
        self.anim2.setEndValue(QPoint(1380,self.posY))
        self.anim2.setEasingCurve(QEasingCurve.Linear)
        self.anim2.start()
    """
        def paintEvent(self,QPaintEvent):
        painter = QPainter(self)
        painter.save()
        metrics = QFontMetrics(self.font())
        path = QPainterPath()
        pen = QPen(QColor(0, 0, 0, 230))
        painter.setRenderHint(QPainter.Antialiasing)
        pen.setWidth(4)
        len = metrics.width(self.text)
        w = self.width()
        px = (len-w)/2
        if px <0 :
            px = -px

        
        py = (self.height()-metrics.height())/2 + metrics.ascent()
        if py <0 :
            py = -py

        path.addText(px+2,py+2,self.font(),self.text)
        painter.strokePath(path,pen)
        painter.drawPath(path)
        painter.fillPath(path,QBrush(self.color))
        painter.restore()    
    """

    def setposY(self,y):
        self.posY = y

    def setcolor(self,color):
        self.color = color


class DanmuWindow(QWidget):
    _signal = pyqtSignal(str) 
    def __init__(self,q):
        super().__init__()
        self._signal.connect(self.mySignal)  
        self.q = q
        self.setGeometry(0,0,QDesktopWidget().screenGeometry().width(),QDesktopWidget().screenGeometry().height()/3)
        self.th=threading.Thread(target=self.douyudanmu)
        self.th.setDaemon(True)#守护线程  
        self.th.start()
    
    def mySignal(self,text):
        danmu = Danmu(self,text,random.randint(0, 190),QColor(255,255,255))
        danmu.show()

    def alldanmu(self):
        while True:
            if not self.q.empty():
                self._signal.emit(self.q.get())
            time.sleep(0.5)

    def douyudanmu(self):
        dmc = DanMuClient('https://www.douyu.com/522423')
        @dmc.danmu
        def danmu_fn(msg):
            pp('{}'.format(msg['Content']))
      
        def pp(msg):
            self._signal.emit(msg)
        dmc.start(blockThread=True)


def invoke_sock(q):
    time.sleep(1)
    url = "http://localhost:5000/danmu_get"
    while True:
        data = urllib.request.urlopen(url).read()
        if data != b'no':
            print(data.decode('utf-8'))
            q.put(data.decode('utf-8'))
        time.sleep(0.5)

def invoke_gui(q):
    app = QApplication(sys.argv)
    win = DanmuWindow(q)
    
    win.setAttribute(Qt.WA_TranslucentBackground)
    win.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    q = Queue()
    #pw = Process(target=invoke_sock, args=(q,))
    pr = Process(target=invoke_gui, args=(q,))
    #pw.start()
    pr.start()
