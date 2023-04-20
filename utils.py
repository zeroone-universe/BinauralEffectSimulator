import librosa as lbr
import numpy as np

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

#polar coordinates
class PolarCoordinate(QWidget):

    qp = QPainter()
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Where Audio Comes From?')
        self.move(300, 300)
        self.resize(600, 350)
        self.show()

    def paintEvent(self, e):
        self.qp.begin(self)
        self.draw_ellipse(self.qp)
        self.qp.end()

    def draw_ellipse(self, qp):
        qp.setPen(QPen(Qt.black, 2, Qt.DashLine))
        for i in {50,100,150,200,250} :
            qp.drawArc(i,i, 600-2*i, 600-2*i,0,180*16)
            # qp.drawEllipse(i, i, 600-2*i, 600-2*i)


    def mousePressEvent(self, event):
        xTmp, yTmp = event.x() - 300, -event.y() + 300
        if yTmp>=0 and xTmp**2+yTmp**2<62500 :
            xPos=xTmp*10/250
            yPos=yTmp*10/250
            self.xPos, self.yPos = xPos, yPos
            self.close()
            
#Audio
def load_audio(file):
    wav_file= file
    wav_mono, wav_sr =lbr.load(wav_file, sr=None)
    wav_mono, wav_sr =lbr.load(wav_file, sr=None)
    wav_left=np.concatenate((wav_mono, np.zeros(441000)),axis=0)
    wav_right=np.concatenate((wav_mono, np.zeros(441000)), axis=0)
    return  wav_mono, wav_left, wav_right ,wav_sr

def binaural(x,y):
    
    #to polar coordinates
    r= np.sqrt(x**2+y**2)
    theta=np.arctan(y/x)
    
    #phase 
    left_dis=np.sqrt((x+0.15)**2+(y)**2) #좌이까지 거리
    left_timedelay=left_dis/340
    right_dis=np.sqrt((x-0.15)**2+(y)**2)#우이까지 거리
    right_timedelay=right_dis/340
    
    #volume parameter
    
    if theta>=0:
        left_vol=(np.abs(theta)/(np.pi))*(1/r)
        right_vol=(1-(np.abs(theta)/(np.pi)))*(1/r)
    else:
        left_vol=(1-(np.abs(theta)/(np.pi)))*(1/r)
        right_vol=(np.abs(theta)/(np.pi))*(1/r)
    
    return left_vol, left_timedelay, right_vol, right_timedelay
