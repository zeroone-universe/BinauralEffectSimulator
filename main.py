import librosa as lbr
import numpy as np
import IPython.display as ipd
import soundfile as sf
import sys
import time
import pydub

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt

from utils import *


xPos = 0 
yPos = 0


class MyApp(QWidget):

    qp = QPainter()
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Where does the signal come from?')
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

    
if __name__ == '__main__':
    
    # 큰따옴표 안에 .wav를 제외한 파일 이름을 입력하세요.
    #file="song"
    file="letsgo"
    # file="Britney Spears - (You Drive Me) Crazy (Original Mix)"
    
    filename="./mono_wav/"+file+".wav"
    wav_mono, wav_left, wav_right, sr = acoustics.load_audio(filename)
    
    app = QApplication(sys.argv)
    pos = MyApp()
    app.exec_()
    
    xPos, yPos=pos.xPos, pos.yPos
    if xPos>=0:
        print("음원은 사용자 {0}m 앞에, {1}m 오른쪽에 존재합니다.".format(yPos,xPos))
    else:
        print("음원은 사용자 {0}m 앞에, {1}m 왼쪽에 존재합니다.".format(yPos,-xPos))
        
    left_vol, left_timedelay, right_vol, right_timedelay=acoustics.binaural(xPos,yPos)
    
    left_arraydelay=int(left_timedelay * sr)
    right_arraydelay=int(right_timedelay * sr)
    out_left=np.concatenate((np.zeros(left_arraydelay),(wav_left*left_vol)),axis=0)
    out_left=out_left[0:len(wav_mono)+44100*2]
    out_right=  np.concatenate((np.zeros(right_arraydelay),(wav_right*right_vol)),axis=0)  
    out_right=out_right[0:len(wav_mono)+44100*2]
    
    output=np.concatenate([out_left, out_right],axis=0)
    output=output.reshape((-1,2), order='F')
    
    stereo_filename="./stereo_wav/{0}_stereo_({1},{2}).wav".format(file,xPos,yPos)
    sf.write(stereo_filename,output,44100,'PCM_24')
    
    #mp3 출력
    stereo_mp3=pydub.AudioSegment.from_wav(stereo_filename)
    mp3_name="./stereo_mp3/{0}_stereo_({1},{2}).mp3".format(file,xPos,yPos)
    stereo_mp3.export(mp3_name, format="mp3")
    