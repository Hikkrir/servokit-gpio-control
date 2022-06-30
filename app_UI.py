# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

class VideoStreamThread(QtCore.QThread):
    changePixmap = QtCore.pyqtSignal(QtGui.QImage)
    
    def __init__(self, *args, **kwargs):
        super().__init__()

    def run(self):
        self.cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap1.set(3,480)
        self.cap1.set(4,640)
        self.cap1.set(5,30)
        while True:
            ret1, image1 = self.cap1.read()
            if ret1:
                im1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
                height1, width1, channel1 = im1.shape
                step1 = channel1 * width1
                qImg1 = QtGui.QImage(im1.data, width1, height1, step1, QtGui.QImage.Format_RGB888)
                self.changePixmap.emit(qImg1)

class RecordVideoThread(QtCore.QThread):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.active = True

    def run(self):
        if self.active:            
            self.fourcc = cv2.VideoWriter_fourcc(*'XVID') 
            self.out1 = cv2.VideoWriter('output_video.avi', self.fourcc, 15, (640, 480))
            self.cap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.cap1.set(3, 480)
            self.cap1.set(4, 640)
            self.cap1.set(5, 30)
            i = 0
            while self.active:                      
                ret1, image1 = self.cap1.read()
                if ret1:
                    self.out1.write(image1) 
                    cv2.imwrite("D:\servokit-gpio-control\dataframe\\frame_" + str(i) + ".jpg", image1)
                    i+=1    
                self.msleep(10)                    

    def stop(self):
        self.out1.release()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.servo_angle_slider = QtWidgets.QSlider(self.centralwidget)
        self.servo_angle_slider.setGeometry(QtCore.QRect(20, 460, 500, 22))
        self.servo_angle_slider.setOrientation(QtCore.Qt.Horizontal)
        self.servo_angle_slider.setInvertedControls(False)
        self.servo_angle_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.servo_angle_slider.setObjectName("servo_angle_slider")

        self.camera_box_label = QtWidgets.QLabel(self.centralwidget)
        self.camera_box_label.setGeometry(QtCore.QRect(10, 10, 511, 400))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.camera_box_label.setFont(font)
        self.camera_box_label.setTabletTracking(False)
        self.camera_box_label.setStyleSheet("border-style: solid;\n"
                                            "border-width: 1px;\n"
                                            "border-color: black")
        self.camera_box_label.setTextFormat(QtCore.Qt.AutoText)
        self.camera_box_label.setScaledContents(False)
        self.camera_box_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_box_label.setObjectName("camera_box_label")

        self.speed_slider = QtWidgets.QSlider(self.centralwidget)
        self.speed_slider.setGeometry(QtCore.QRect(570, 60, 22, 320))
        self.speed_slider.setOrientation(QtCore.Qt.Vertical)
        self.speed_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.speed_slider.setObjectName("speed_slider")

        self.servo_angle_spin_box = QtWidgets.QSpinBox(self.centralwidget)
        self.servo_angle_spin_box.setGeometry(QtCore.QRect(250, 500, 42, 22))
        self.servo_angle_spin_box.setObjectName("servo_angle_spin_box")
        self.speed_spin_box = QtWidgets.QSpinBox(self.centralwidget)
        self.speed_spin_box.setGeometry(QtCore.QRect(610, 210, 42, 22))
        self.speed_spin_box.setProperty("value", 0)
        self.speed_spin_box.setObjectName("speed_spin_box")

        self.servo_box_info = QtWidgets.QLabel(self.centralwidget)
        self.servo_box_info.setGeometry(QtCore.QRect(190, 430, 171, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.servo_box_info.setFont(font)
        self.servo_box_info.setAutoFillBackground(False)
        self.servo_box_info.setScaledContents(False)
        self.servo_box_info.setObjectName("servo_box_info")
        self.backgound_servo = QtWidgets.QTextBrowser(self.centralwidget)
        self.backgound_servo.setGeometry(QtCore.QRect(10, 420, 521, 181))
        font = QtGui.QFont()
        font.setKerning(True)
        self.backgound_servo.setFont(font)
        self.backgound_servo.setObjectName("backgound_servo")
        self.background_speed = QtWidgets.QTextBrowser(self.centralwidget)
        self.background_speed.setGeometry(QtCore.QRect(530, 10, 256, 571))
        self.background_speed.setObjectName("background_speed")
        self.speed_box_info = QtWidgets.QLabel(self.centralwidget)
        self.speed_box_info.setGeometry(QtCore.QRect(540, 20, 230, 25))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.speed_box_info.setFont(font)
        self.speed_box_info.setObjectName("speed_box_info")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(550, 400, 160, 100))
        self.label.setText("Угол сервопривода -- 110°")
        self.label.setFont(QtGui.QFont("Arial", 9))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(550, 420, 160, 100))
        self.label_2.setText("Скорость двигателя -- 0")
        self.label_2.setFixedSize(160, 100)
        self.label_2.setFont(QtGui.QFont("Arial", 9))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.control_bt = QtWidgets.QPushButton(self.centralwidget)
        self.control_bt.setText("Начать запись")
        self.control_bt.setGeometry(QtCore.QRect(550, 500, 160, 20))
        self.control_bt.clicked.connect(self.controlTimer)
        self.saveTimer = QtCore.QTimer()

        self.th = VideoStreamThread()
        self.th.changePixmap.connect(self.setImage)
        self.th.start()

        self.backgound_servo.raise_()
        self.background_speed.raise_()
        self.servo_angle_slider.raise_()
        self.camera_box_label.raise_()
        self.speed_slider.raise_()
        self.servo_angle_spin_box.raise_()
        self.speed_spin_box.raise_()
        self.servo_box_info.raise_()
        self.speed_box_info.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.control_bt.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setImage(self, qImg1):
        self.camera_box_label.setPixmap(QtGui.QPixmap.fromImage(qImg1))

    def controlTimer(self):
        if not self.saveTimer.isActive():
            self.saveTimer.start()
            self.th2 = RecordVideoThread(self)
            self.th2.active = True                                
            self.th2.start()
            self.control_bt.setText("Остановить запись")
        else:
            self.saveTimer.stop()
            self.th2.active = False                   
            self.th2.stop()                         
            self.th2.terminate()                    
            self.control_bt.setText("Начать запись")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Control"))
        self.camera_box_label.setText(_translate("MainWindow", "No camera enable"))
        self.servo_box_info.setText(_translate("MainWindow", "управление углом поворота"))
        self.speed_box_info.setText(_translate("MainWindow", "Управление скоростью и направлением"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
