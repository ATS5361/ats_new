import sys
import os
import cv2
import cv2.aruco as aruco
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon
import business_logic.fotograf_cekme_algoritmasi as foto
from time import time
from business_logic.mainThread_2 import *

global marker_dict, current_marker

class CameraThread(QThread):
    new_frame = pyqtSignal(object, object, object)  # Frame, Marker IDs, Corners

    def __init__(self, camera_path, aruco_dict, parameters):
        super().__init__()
        self.camera_path = camera_path
        self.capture = cv2.VideoCapture(self.camera_path, cv2.CAP_GSTREAMER)
        self.aruco_dict = aruco_dict
        self.parameters = parameters

    def run(self):
        while True:
            ret, frame = self.capture.read()
            if not ret:
                continue

            # Gri seviyeye çevirme
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # ArUco marker tespiti
            corners, ids, _ = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)

            self.new_frame.emit(frame, ids, corners)  # Yeni frame'i sinyal olarak gönder

class ArUcoTesting(QWidget):
    
    marker_dict = {0: "Cekmece1-1",
                   1: "Cekmece1-2",
                   2: "Cekmece1-3",
                   3: "Cekmece2-3",
                   4: "Cekmece2-2",
                   5: "Cekmece2-1",
                   6: "Cekmece3-3",
                   7: "Cekmece3-2",
                   8: "Cekmece3-1",
                   9: "Cekmece4-3",
                   10: "Cekmece4-2",
                   11: "Cekmece4-1",
                   12: "Cekmece5-3",
                   13: "Cekmece5-2",
                   14: "Cekmece5-1",
                   15: "Cekmece6-1",
                   16: "Cekmece6-2",
                   17: "Cekmece6-3",
                   } ## Optimizasyon Önerisi: Value'lar list olarak kaydedilebilir

    drawer_num_dict = {0:1,
                       1:1,
                       2:1,
                       3:2,
                       4:2,
                       5:2,
                       6:3,
                       7:3,
                       8:3,
                       9:4,
                       10:4,
                       11:4,
                       12:5,
                       13:5,
                       14:5,
                       15:6,
                       16:6,
                       17:6,
                       }

    def __init__(self, width=800, height=600):
        super().__init__()
        self.setWindowTitle("ArUco Testing")
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowIcon(QIcon("images/tai-logo-color.png"))
        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.reset_active_drawer)
        self.timer.start(1000)  # Her saniyede bir kontrol et
        
        # ArUco tanımları
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        self.parameters = aruco.DetectorParameters_create()

        # Kamera işleme iş parçacığı başlatma
        self.camera_thread1 = CameraThread("v4l2src device=/dev/video0 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! nvvideoconvert ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", self.aruco_dict, self.parameters)
        self.camera_thread2 = CameraThread("v4l2src device=/dev/video2 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! nvvideoconvert ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", self.aruco_dict, self.parameters)

        self.detected_ids = set() 
        self.current_marker = None 

        self.camera_thread1.new_frame.connect(lambda frame, ids, corners: self.process_frame(frame, ids, corners, 1))
        self.camera_thread2.new_frame.connect(lambda frame, ids, corners: self.process_frame(frame, ids, corners, 2))

        self.camera_thread1.start()
        self.camera_thread2.start()

        self.active_drawer = None
        self.last_marker = None  # hangi ArUco tespit edildi
        self.last_capture_time = 0  # son fotoğraf ne zaman çekildi
        self.last_detection_time = time()  # son detection zamanı

        self.camera_control = foto.CameraControl()
        self.setFixedSize(width, height)

    def initUI(self):
        main_layout = QVBoxLayout()
        self.screenlabel1 = QLabel("Kamera 1")
        self.screenlabel2 = QLabel("Kamera 2")
        self.screenlabel1.setFixedSize(1028, 320)
        self.screenlabel2.setFixedSize(1028, 320)
        
        main_layout.addWidget(self.screenlabel1)
        main_layout.addWidget(self.screenlabel2)
        self.setLayout(main_layout)

    def reset_active_drawer(self):
        if time() - self.last_detection_time > 30:  # 30 saniye boyunca yeni ArUco yoksa
            self.active_drawer = None
            print("30 saniye boyunca yeni ArUco tespit edilmedi, active_drawer sıfırlandı.")

    def process_frame(self, frame, ids, corners, camera_id):
        try:
            if ids is not None:
                aruco.drawDetectedMarkers(frame, corners, ids)
                for i in range(len(ids)):
                    marker_id = ids[i][0]

                    current_time = time()

                    # Eğer yeni bir ArUco tespit edildiyse veya 10 saniye geçtiyse fotoğraf çek
                    if (marker_id != self.last_marker) or (current_time - self.last_capture_time > 10):
                        self.last_marker = marker_id
                        self.last_capture_time = current_time
                        self.active_drawer = self.drawer_num_dict.get(marker_id, None)
                        print(f"{self.marker_dict[marker_id]} tespit edildi, fotoğraf çekiliyor...")
                        self.save_processed_photo() # set it to save_processed_photo_cropped() to use crop feature 

                    self.last_detection_time = current_time  # Detection zamanını güncelle

            self.display_image(self.screenlabel1 if camera_id == 1 else self.screenlabel2, frame)

        except KeyError:
            pass

    def display_image(self, label, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(qimg))

        count = 0
    def cropImage_1(self, frame, drawerNum):
        if frame is None or frame.size == 0:
            return None  # Geçersiz resim döndürme
        
        h_, w_ = frame.shape[:2]
        crop_regions = {
            1: (150, 100, w_ - 315, h_ - 175),
            2: (195, 223, w_ - 131, h_ - 255),
            3: (225, 332, w_ - 475, h_ - 285),
            4: (0, 0, w_, h_),
            5: (311, 290, w_ - 175, h_ - 165),
            6: (0, 0, w_, h_),
            'default': (140, 150, w_, h_ - 200)
        }
        x, y, w, h = crop_regions.get(drawerNum, crop_regions['default'])
        
        return frame[y:h, x:w]  # Doğrudan NumPy slicing ile kırpma

    def cropImage_2(self, frame, drawerNum):
        if frame is None or frame.size == 0:
            return None  
        
        h_, w_ = frame.shape[:2]
        crop_regions = {
            1: (120, 25, w_ - 177, h_ - 192),
            2: (180, 360, w_ - 325, h_ - 250),
            3: (226, 235, w_ - 375, h_ - 295),
            4: (258, 0, w_ - 450, h_ - 310),
            5: (268, 40, w_ - 480, h_ - 315),
            6: (281, 170, w_ - 508, h_ - 325),
            'default': (190, 0, w_ - 150, h_ - 200)
        }
        x, y, w, h = crop_regions.get(drawerNum, crop_regions['default'])
        
        return frame[y:h, x:w]  # Doğrudan NumPy slicing ile kırpma

## TAKE AND CROP THE PHOTO
    def save_processed_photo_cropped(self):
        drawer_num = self.active_drawer
        camera_nums = [1, 2]

        for camera_num in camera_nums:
            folder_path = f"fotolar_yeni/cekmece{drawer_num}"
            os.makedirs(folder_path, exist_ok=True)

            if camera_num == 1:
                ret, frame = self.camera_thread1.capture.read()
                if ret:
                    frame = self.cropImage_1(frame, drawer_num)
            else:
                ret, frame = self.camera_thread2.capture.read()
                if ret:
                    frame = self.cropImage_2(frame, drawer_num)

            if ret and frame is not None:
                # Kalibrasyon sonrası düzeltme
                map1, map2, map1_0014, map2_0014 = foto.setCameraParameter()
                calibrated_frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR)

                # Fotoğrafı kaydet
                photo_path = os.path.join(folder_path, f"cam{camera_num}_processed{self.count}.jpg")
                cv2.imwrite(photo_path, calibrated_frame)
                print(f"Kalibre fotoğraf kaydedildi: {photo_path}")
                self.count += 1

    count = 0
    def save_processed_photo(self):
        drawer_num = self.active_drawer
        camera_nums = [1, 2]
        for camera_num in camera_nums:
            folder_path = f"fotolar_yeni/cekmece{drawer_num}"
            os.makedirs(folder_path, exist_ok=True)
            
            ret, frame = self.camera_thread1.capture.read() if camera_num == 1 else self.camera_thread2.capture.read()
            if ret:
                # Kalibrasyon sonrası düzeltme işlemi
                map1, map2, map1_0014, map2_0014 = foto.setCameraParameter()
                frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR)
                photo_path = os.path.join(folder_path, f"cam{camera_num}_processed{self.count}.jpg")
                cv2.imwrite(photo_path, frame)
                print(f"Kalibre fotoğraf kaydedildi: {photo_path}")
                self.count = self.count + 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ArUcoTesting()
    win.show()
    sys.exit(app.exec_())