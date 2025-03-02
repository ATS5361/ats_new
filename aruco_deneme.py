import os
import sys
import cv2
import cv2.aruco as aruco
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer

class ArUcoTesting(QWidget):
    def __init__(self, width=1048, height=800):
        super().__init__()
        self.setWindowTitle("ArUco Testing")
        self.setGeometry(100, 100, 1000, 500)
        
        self.initUI()
        
        # Kamera yolları
        self.cam1_path = "v4l2src device=/dev/video0 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! nvvideoconvert ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
        self.cam2_path = "v4l2src device=/dev/video2 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! nvvideoconvert ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"

        # Kameralar başlatılıyor
        self.capture1 = cv2.VideoCapture(self.cam1_path, cv2.CAP_GSTREAMER)
        self.capture2 = cv2.VideoCapture(self.cam2_path, cv2.CAP_GSTREAMER)

        if not self.capture1.isOpened() or not self.capture2.isOpened():
            QMessageBox.critical(self, "Hata", "Kameralar açılamadı!")
            sys.exit(1)  # Programı durdur

#        self.camera_control = foto.CameraControl()
        self.setFixedSize(width, height)

        # Timer başlat
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.run)
        self.timer.start(30)

        # ArUco tanımları
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        self.parameters = aruco.DetectorParameters_create()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.screenlabel1 = QLabel("Kamera 1")
        self.screenlabel2 = QLabel("Kamera 2")
        
        main_layout.addWidget(self.screenlabel1)
        main_layout.addWidget(self.screenlabel2)
        self.setLayout(main_layout)

    def run(self):
        ret1, frame1 = self.capture1.read()
        ret2, frame2 = self.capture2.read()

        if not ret1 or not ret2:
            print("Kamera görüntüsü alınamadı!")
            return

        # Gri seviyeye çevirme
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # ArUco marker tespiti
        corners1, ids1, _ = aruco.detectMarkers(gray1, self.aruco_dict, parameters=self.parameters)
        corners2, ids2, _ = aruco.detectMarkers(gray2, self.aruco_dict, parameters=self.parameters)

        if ids1 is not None:
            aruco.drawDetectedMarkers(frame1, corners1, ids1)
            for i in range(len(ids1)):
                x, y = int(corners1[i][0][0][0]), int(corners1[i][0][0][1])
                print(f"Kamera 1 - Marker ID: {ids1[i][0]}, Konum: ({x}, {y})")

        if ids2 is not None:
            aruco.drawDetectedMarkers(frame2, corners2, ids2)
            for i in range(len(ids2)):
                x, y = int(corners2[i][0][0][0]), int(corners2[i][0][0][1])
                print(f"Kamera 2 - Marker ID: {ids2[i][0]}, Konum: ({x}, {y})")

        # PyQt QLabel'e görüntüleri aktar
        self.display_image(self.screenlabel1, frame1)
        self.display_image(self.screenlabel2, frame2)

    def display_image(self, label, frame):
        """ OpenCV görüntüsünü QLabel'e çevirip gösterir. """
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        print("Çıkış yapılıyor...")
        QTimer.singleShot(500, QApplication.instance().quit)
        event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ArUcoTesting()
    win.show()
    sys.exit(app.exec_())