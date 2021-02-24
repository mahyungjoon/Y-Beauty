import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join
from pathlib import Path

import numpy as np
import dlib
import cv2
import pafy
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow.compat.v1 as tf
import os.path
import time
import datetime as dt
import pymysql

# images = [cv2.imread(file) for file in glob.glob("C:/korAI/beautyGAN/result/*.png")]
# path = glob.glob("C:/korAI/beautyGAN/result/*.png")
# cv_img = []



py_path = os.path.dirname(os.path.abspath("C:/korAI/beautyGAN/result/"))
os.chdir(py_path)

img_list = []
name_list = []

i = 1

def clickable(widget): # Label을 클릭할수있게 만들어주는 함수
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit() #emit(obj)를 선택하여 슬롯 내에서 객체를 가져올수있음
                        return True
            return False
    
    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked




class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    bSaveFlag = False

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from Youtube
        # url = "https://www.youtube.com/watch?v=7tf3lKh1pxU"
        # video = pafy.new(url)
        # best = video.getbest()
        # cap = cv2.VideoCapture(best.url)


        # capture from web cam
        cap = cv2.VideoCapture(0)
        
        frameRate = int(cap.get(cv2.CAP_PROP_FPS))
        
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            if self.bSaveFlag:
                cv2.imwrite("./cusFace.jpg", cv_img)
                self.bSaveFlag = False
            key = cv2.waitKey(frameRate)  # frameRate msec동안 한 프레임을 보여준다

        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

class MakeupDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.styleFile = None
    
    def setupUI(self):
        self.setGeometry(70, 70, 400, 150)
        self.setWindowTitle("Model")
        self.setWindowIcon(QIcon("C:/korAI/beautyGAN/beauty.png"))

        self.label1 = QLabel()
        self.label2 = QLabel()
        self.label3 = QLabel()
        self.label4 = QLabel()
        self.label5 = QLabel()
        self.label6 = QLabel()
        self.label7 = QLabel()
        self.label8 = QLabel()
        self.label9 = QLabel()
        self.label10 = QLabel()
        self.label11 = QLabel()
        self.label12 = QLabel()

        clickable(self.label1).connect(self.pushLabel1)
        clickable(self.label2).connect(self.pushLabel2)
        clickable(self.label3).connect(self.pushLabel3)
        clickable(self.label4).connect(self.pushLabel4)
        clickable(self.label5).connect(self.pushLabel5)
        clickable(self.label6).connect(self.pushLabel6)
        clickable(self.label7).connect(self.pushLabel7)
        clickable(self.label8).connect(self.pushLabel8)
        clickable(self.label9).connect(self.pushLabel9)
        clickable(self.label10).connect(self.pushLabel10)
        clickable(self.label11).connect(self.pushLabel11)
        clickable(self.label12).connect(self.pushLabel12)

        qStSrc1 = QPixmap()
        qStSrc1.load("C:/korAI/beautyGAN/makeup/vFG56.png")
        self.label1.setPixmap(qStSrc1)
        qStSrc2 = QPixmap()
        qStSrc2.load("C:/korAI/beautyGAN/makeup/vFG112.png")
        self.label2.setPixmap(qStSrc2)
        qStSrc3 = QPixmap()
        qStSrc3.load("C:/korAI/beautyGAN/makeup/vFG137.png")
        self.label3.setPixmap(qStSrc3)
        qStSrc4 = QPixmap()
        qStSrc4.load("C:/korAI/beautyGAN/makeup/vRX916.png")
        self.label4.setPixmap(qStSrc4)
        qStSrc5 = QPixmap()
        qStSrc5.load("C:/korAI/beautyGAN/makeup/XMY-014.png")
        self.label5.setPixmap(qStSrc5)
        qStSrc6 = QPixmap()
        qStSrc6.load("C:/korAI/beautyGAN/makeup/XMY-074.png")
        self.label6.setPixmap(qStSrc6)
        qStSrc7 = QPixmap()
        qStSrc7.load("C:/korAI/beautyGAN/makeup/XMY-136.png")
        self.label7.setPixmap(qStSrc7)
        qStSrc8 = QPixmap()
        qStSrc8.load("C:/korAI/beautyGAN/makeup/XMY-266.png")
        self.label8.setPixmap(qStSrc8)
        qStSrc9 = QPixmap()
        qStSrc9.load("C:/korAI/beautyGAN/makeup/XMY-112.png")
        self.label9.setPixmap(qStSrc9)
        qStSrc10 = QPixmap()
        qStSrc10.load("C:/korAI/beautyGAN/makeup/XMY-036.png")
        self.label10.setPixmap(qStSrc10)
        qStSrc11 = QPixmap()
        qStSrc11.load("C:/korAI/beautyGAN/makeup/vFG22.png")
        self.label11.setPixmap(qStSrc11)
        qStSrc12 = QPixmap()
        qStSrc12.load("C:/korAI/beautyGAN/makeup/vFG368.png")
        self.label12.setPixmap(qStSrc12)

        layout = QGridLayout()
        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.label2, 0, 1)
        layout.addWidget(self.label3, 0, 2)
        layout.addWidget(self.label4, 0, 3)
        layout.addWidget(self.label5, 1, 0)
        layout.addWidget(self.label6, 1, 1)
        layout.addWidget(self.label7, 1, 2)
        layout.addWidget(self.label8, 1, 3)
        layout.addWidget(self.label9, 2, 0)
        layout.addWidget(self.label10, 2, 1)
        layout.addWidget(self.label11, 2, 2)
        layout.addWidget(self.label12, 2, 3)
        self.setLayout(layout)

    def pushLabel1(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/vFG56.png"
        self.close()
    def pushLabel2(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/vFG112.png"
        self.close()
    def pushLabel3(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/vFG137.png"
        self.close()
    def pushLabel4(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/vRX916.png"
        self.close()
    def pushLabel5(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/XMY-014.png"
        self.close()
    def pushLabel6(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/XMY-074.png"
        self.close()
    def pushLabel7(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/XMY-136.png"
        self.close()
    def pushLabel8(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/XMY-266.png"
        self.close()
    def pushLabel9(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/XMY-112.png"
        self.close()
    def pushLabel10(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/XMY-036.png"
        self.close()
    def pushLabel11(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/vFG22.png"
        self.close()
    def pushLabel12(self):
        self.styleFile = "C:/korAI/beautyGAN/makeup/vFG368.png"
        self.close()

class ResultDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.ResultFile = None
    
    def setupUI(self):
        self.setGeometry(70, 70, 400, 150)
        self.setWindowTitle("Result Model")
        self.setWindowIcon(QIcon("C:/korAI/beautyGAN/beauty.png"))

        self.Rlabel0 = QLabel()
        self.Rlabel1 = QLabel()
        self.Rlabel2 = QLabel()


        clickable(self.Rlabel0).connect(self.pushRlabel0)
        clickable(self.Rlabel1).connect(self.pushRlabel1)
        clickable(self.Rlabel2).connect(self.pushRlabel2)


        Resrc0 = QPixmap()
        Resrc0.load(name_list[0])
        self.Rlabel0.setPixmap(Resrc0)

        Resrc1 = QPixmap()
        Resrc1.load(name_list[1])
        self.Rlabel1.setPixmap(Resrc1)

        Resrc2 = QPixmap()
        Resrc2.load(name_list[2])
        self.Rlabel2.setPixmap(Resrc2)

        layout = QGridLayout()
        layout.addWidget(self.Rlabel0, 0, 0)
        layout.addWidget(self.Rlabel1, 0, 1)
        layout.addWidget(self.Rlabel2, 0, 2)

        self.setLayout(layout)

    def pushRlabel0(self):
        self.ResultFile = name_list[0]
        self.close()
    def pushRlabel1(self):
        self.ResultFile = name_list[1]
        self.close()
    def pushRlabel2(self):
        self.ResultFile = name_list[2]
        self.close()



class MyWindow(QWidget):
    ResultFilePath = ""
    styleFilePath = ""
    FaceDector = dlib.get_frontal_face_detector()
    ShapePredictor = dlib.shape_predictor("C:/korAI/beautyGAN/models/shape_predictor_68_face_landmarks.dat")

    def __init__(self):
        super().__init__()
        self.setupUI()

        self.setStyleSheet("background-color: White;")

    def setupUI(self):
        self.setGeometry(50, 50, 900, 500)
        self.setWindowTitle("Y-Beauty v0.1")
        self.setWindowIcon(QIcon("C:/korAI/beautyGAN/beauty.png"))
 #---------------------------------------------------------------------------------------------------------------
        LeftLayout = QVBoxLayout()

        self.btnSelect = QPushButton("Style")
        self.btnSelect.setGeometry(100, 100, 50, 20)
        self.btnSelect.setStyleSheet("background-color: Yellow;font-Size : 18px;font-family:Times New Roman;")

        self.lblStyle = QLabel()
        self.lblStyle.resize(320, 240)
        self.lblStyle.setStyleSheet("color: green;""background-color: White;")        

        LeftLayout.addWidget(self.btnSelect)
        LeftLayout.addWidget(self.lblStyle)
 #---------------------------------------------------------------------------------------------------------------
        CenterLayout = QVBoxLayout()

        self.btnMakeup = QPushButton("Click-Photo")
        self.btnMakeup.setGeometry(100, 100, 50, 20)
        self.btnMakeup.setFont(QFont("Times", 15))
        self.btnMakeup.setStyleSheet("background-color: Yellow;font-Size : 18px;font-family:Times New Roman;")

        self.btnResult = QPushButton("Result-image")
        self.btnResult.setGeometry(100, 100, 50, 20)
        self.btnResult.setFont(QFont("Times", 15))
        self.btnResult.setStyleSheet("background-color: Yellow;font-Size : 18px;font-family:Times New Roman;")

        self.lblImage = QLabel()
        self.lblImage.resize(320, 240)
        self.lblImage.setStyleSheet("color: blue;""background-color: White;")

        CenterLayout.addWidget(self.btnMakeup)
        CenterLayout.addWidget(self.lblImage)
        CenterLayout.addWidget(self.btnResult)
 #---------------------------------------------------------------------------------------------------------------
        RightLayOut = QVBoxLayout()

        self.lblBeauty = QLabel("You-MakeUp")
        self.lblBeauty.setStyleSheet("background-color: Yellow;font-Size : 18px;font-family:Times New Roman;")
        self.lblBeauty.resize(400,300)
        self.lblBeauty.setAlignment(Qt.AlignCenter)

        self.lblName = QLabel("성명:")
        self.N_text = QLineEdit(self)

        Right2LayOut = QHBoxLayout()

        Right2LayOut.addWidget(self.lblName)
        Right2LayOut.addWidget(self.N_text)


        myFont=QFont()
        myFont.setBold(True)
        self.lblBeauty.setFont(myFont)

        self.matfig = plt.Figure()
        self.canvas = FigureCanvas(self.matfig)

        RightLayOut.addWidget(self.lblBeauty)
        RightLayOut.addLayout(Right2LayOut)
        RightLayOut.addWidget(self.canvas)

 #---------------------------------------------------------------------------------------------------------------
        qPmSource = QPixmap()
        qPmSource.load("C:/korAI/beautyGAN/makeup/Choice.png")
        self.lblStyle.setPixmap(qPmSource)
        self.lblStyle.resize(320, 240)

        AllLayout = QHBoxLayout()
        AllLayout.addLayout(LeftLayout)
        AllLayout.addLayout(CenterLayout)
        AllLayout.addLayout(RightLayOut)
        # AllLayout.setStretchFactor(bottomLayout, 1)
        self.setLayout(AllLayout)

        self.btnSelect.clicked.connect(self.SelectFile)
        self.btnMakeup.clicked.connect(self.onMakeupButtonClicked)
        self.btnResult.clicked.connect(self.ResultSelect)

        # create the video capture thread
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()

  
    def ResultSelect(self):
        dlg2 = ResultDialog()
        dlg2.exec_()
        fname2 = dlg2.ResultFile

        #fname, _ = QFileDialog.getOpenFileName(self, "Load Image", "")
        if fname2:
            self.ResultFilePath = fname2
            self.qPmSource2 = QPixmap()
            self.qPmSource2.load(fname2)
            self.lblBeauty.setPixmap(self.qPmSource2)
            self.lblBeauty.resize(320, 240)

    def SelectFile(self): # 모델 선택 함수
        dlg = MakeupDialog()
        dlg.exec_()
        fname = dlg.styleFile

        #fname, _ = QFileDialog.getOpenFileName(self, "Load Image", "")
        if fname: 
            self.styleFilePath = fname
            self.qPmSource = QPixmap()
            self.qPmSource.load(fname)
            self.lblStyle.setPixmap(self.qPmSource)
            self.lblStyle.resize(320, 240)

    def onMakeupButtonClicked(self):

        #==========비디오를 이미지로 캡쳐한다. VideoThread의 bSaveFlag를 True로 만든다.
        self.thread.bSaveFlag = True
        #===============고객의 사진이 찍힐때까지 2초 기다린다.====================
        for i in range(1, 21): 
            time.sleep(0.1) #
            if os.path.exists("./cusFace.jpg"):
                break

        if not os.path.exists("./cusFace.jpg"):
            QMessageBox.information(self, "Message", "고객 사진이 촬영되지 않았습니다.")
            return
        if not os.path.exists(self.styleFilePath):
            QMessageBox.information(self, "Message", "스타일 사진을 선택하세요.")
            return
        if  self.N_text.text() == "":
            QMessageBox.information(self, "Message", "이름을 입력해주세요.")
            return
        #====================고객의 사진을 Makeup 한다.==========================
        # 원본 이미지를 읽는다. img1 은 원본 이미지, img2 는 스타일 이미지
        img1 = dlib.load_rgb_image("./cusFace.jpg") # -> 캠에서 캡쳐된 이미지
        # 스타일 이미지를 읽는다.
        img2 = dlib.load_rgb_image(self.styleFilePath) # -> 모델 선택이미지
        # 원본 이미지, 스타일 이미지에서 얼굴을 검출한다.
        faces1 = self.align_faces(img1)
        if not faces1:
            return
        faces2 = self.align_faces(img2)
        #검출된 얼굴에서 첫번째 얼굴을 사용한다.
        src_img = faces1[0]
        ref_img = faces2[0]
        # 얼굴에 대해 전처리 작업을 한다
        X_img = self.preprocess(src_img)
        X_img = np.expand_dims(X_img, axis=0)
        Y_img = self.preprocess(ref_img)
        Y_img = np.expand_dims(Y_img, axis=0)

        # 텐서플로우로 GAN 을 돌려 예측 이미지를 얻는다.
        with tf.compat.v1.Session() as sess: #텐서플로를 통해 세션생성
            sess.run(tf.global_variables_initializer())
            saver = tf.train.import_meta_graph("C:/korAI/beautyGAN/models/model.meta") #tf.train.import_meta_graph -> 모델의 그래프를 불러온다
            saver.restore(sess, tf.train.latest_checkpoint("C:/korAI/beautyGAN/models")) #모델의 weights를 로드한다 #CHeckpoint 모델의 변수 값을 저장
            graph = tf.get_default_graph()
            X = graph.get_tensor_by_name("X:0") # X:0 으로 미리 지정해두고 X변수명을 쓸떄 불러옴
            Y = graph.get_tensor_by_name("Y:0")
            Xs = graph.get_tensor_by_name("generator/xs:0")
            output = sess.run(Xs, feed_dict={X: X_img, Y: Y_img}) #X0값에 X_img를 넣어서 아웃풋해줌
            output_img = self.deprocess(output[0]) # 아웃풋 이미지를 위해 위에거 해주고 
        # 예측 결과를 matplotlib 에 출력한다.
        ax = self.matfig.add_subplot(111)
        ax.axis("off")
        ax.grid(False)
        ax.imshow(output_img)
        self.canvas.draw()

        if not os.path.exists('./result/' + self.N_text.text() + '1.png'):
            name_list.clear
            style_V = './result/' + self.N_text.text() + '1.png'
        elif not os.path.exists('./result/' + self.N_text.text() + '2.png'):
            style_V = './result/' + self.N_text.text() + '2.png'
        elif not os.path.exists('./result/' + self.N_text.text() + '3.png'):
            style_V = './result/' + self.N_text.text() + '3.png'
        else:
            style_V = './result/' + self.N_text.text() + '1.png'
        
        name_list.append(style_V)

        self.matfig.savefig(style_V)
        self.insert_db(style_V)

        #====================고객의 사진을 지운다.===============================
        if os.path.exists("./cusFace.jpg"):
            os.remove('./cusFace.jpg')

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.lblImage.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(320, 240, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def align_faces(self, img):
        # 얼굴을 검출한다.
        dets = self.FaceDector(img, 1)
        if len(dets) == 0:
            QMessageBox.information(self, "Message", "사진에서 얼굴을 찾을 수 없습니다!")
            return
        # 객체 검출 모델
        objs = dlib.full_object_detections()

        #검출한 얼굴을 모두 객체 검출 모델로
        for detection in dets:
            s = self.ShapePredictor(img, detection) #ShapePredictor - > 랜드마크 68개의 점
            objs.append(s)

        #얼굴을 각도 조절
        faces = dlib.get_face_chips(img, objs, size=256, padding=0.35) # 얼굴을 수평으로 회전하여 얼굴 부분만 자른 이미지를 변환 
        return faces
    
    def preprocess(self, img):
        return (img / 255.0 - 0.5) * 2

    def deprocess(self, img):
        return (img + 1) / 2

    def insert_db(self, fname2):
        conn = pymysql.connect(host="localhost",user="root",password="1234",db="mydb1",charset="utf8")

        try:
            mydb = conn.cursor()
            sql = "insert into mydb1(style) values(%s)"
            mydb.execute(sql, (fname2))
            conn.commit()

        finally:
            conn.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    wWindow = MyWindow()
    wWindow.show()
    app.exec_()