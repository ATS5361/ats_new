"""

        Bu uygulama TUSAŞ YTÜ Teknopark bünyesinde geliştirilen
        TUSAS Automated Tool Control System'in overexposure
        sorunu için potansiyel çözümler denerken iki kameranın da
        aynı anda görselleştirilebilmesi ve aradaki farkların
        bulunmasının kolaylaştırılması için geliştirilmiştir.
        
        GÜNCEL VERSİYON

"""

import os
import sys
import cv2
import fotograf_cekme_algoritmasi as foto
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QImage, QIcon, QSurfaceFormat
from PyQt5.QtCore import QTimer
import threading

# TODO - add threading for multiprocessing
# TODO - handle errors and exceptions
# TODO - add less dependencies and more variables for low coupling
# TODO - bir fotoğrafı çekince directory'deki diğer fotoğrafları silmeyecek şekilde guncellenecek
# TODO - kamera değiştir butonları arasında geçiş kolaylığı sağlanacak
# TODO - saygınlık

fmt = QSurfaceFormat()
fmt.setVersion(4, 6)
fmt.setProfile(QSurfaceFormat.CoreProfile)
fmt.setDepthBufferSize(24)
fmt.setStencilBufferSize(8)
QSurfaceFormat.setDefaultFormat(fmt)


class ToolControlUI(QWidget):
    def __init__(self, width=1048, height=800):
        super().__init__()
        self.setWindowTitle("ATCS Control UI")
        self.setGeometry(100, 100, 1000, 500)
        
        self.initUI()
        self.camera_is_on = False
        self.current_camera = 0
        self.capture1 = None
        self.capture2 = None
        self.active_drawer = None
        self.fullscreen = False
        self.cam1_path = "v4l2src device=/dev/video0 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! nvvideoconvert ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
        self.cam2_path = "v4l2src device=/dev/video2 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! nvvideoconvert ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
        self.count1, self.count2 = 0, 0

        self.setWindowIcon(QIcon("logo.jpg"))

        self.start_cameras()
        self.camera_control = foto.CameraControl()
        self.setFixedSize(width, height)
        
    def initUI(self):
        main_layout = QVBoxLayout()
        
        self.image_label1 = QLabel("Kamera 1")
        self.image_label2 = QLabel("Kamera 2")
        self.image_label1.setFixedSize(1028, 320)
        self.image_label2.setFixedSize(1028, 320)
        
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.image_label1)
        image_layout.addWidget(self.image_label2)
        main_layout.addLayout(image_layout)
        
        button_layout = QHBoxLayout()
        self.drawer_buttons = []
        for i in range(1, 7):
            btn = QPushButton(f"Çekmece {i}")
            btn.clicked.connect(lambda _, drawer_index=i: self.select_drawer(drawer_index))
            button_layout.addWidget(btn)
            self.drawer_buttons.append(btn)
        main_layout.addLayout(button_layout)
        
        photo_layout = QHBoxLayout()
        self.cam1_fullscreen = QPushButton("Kamera 1 Tam Ekran")
        self.cam1_fullscreen.clicked.connect(lambda: self.toggle_fullscreen(1))
        photo_layout.addWidget(self.cam1_fullscreen)
        
        self.cam2_fullscreen = QPushButton("Kamera 2 Tam Ekran")
        self.cam2_fullscreen.clicked.connect(lambda: self.toggle_fullscreen(2))
        photo_layout.addWidget(self.cam2_fullscreen)
        
        self.capture_button = QPushButton("Ham Fotoğrafı Kaydet")
        self.capture_button.clicked.connect(self.save_original_photo)
        photo_layout.addWidget(self.capture_button)

        self.capture_button = QPushButton("Kalibre Fotoğrafları Kaydet")
        self.capture_button.clicked.connect(self.save_processed_photo)
        photo_layout.addWidget(self.capture_button)
        
        self.exit_fullscreen_button = QPushButton("Tam Ekrandan Çık")
        self.exit_fullscreen_button.clicked.connect(self.exit_fullscreen)
        self.exit_fullscreen_button.hide()
        photo_layout.addWidget(self.exit_fullscreen_button)
        
        main_layout.addLayout(photo_layout)
        self.setLayout(main_layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

       # self.to_thread(self.select_drawer)

    
    def start_cameras(self):
        self.capture1 = cv2.VideoCapture(self.cam1_path, cv2.CAP_GSTREAMER)
        self.capture2 = cv2.VideoCapture(self.cam2_path, cv2.CAP_GSTREAMER)
        if not self.capture1.isOpened() or not self.capture2.isOpened():
            QMessageBox.critical(self, "Hata", "Kameralar açılamadı!")
            return
        self.camera_is_on = True
        self.timer.start(5)    
    
    
    def select_drawer(self, drawer_index):
        try:
            self.active_drawer = drawer_index
            self.camera_control.drawerNum = drawer_index
            self.camera_control.set_camera_parameters()
    #        print(f"{drawer_index}. Çekmece işleniyor...")
        except ValueError as e:
            print(f"Çekmece {drawer_index} parametreleri ayarlandı")

    def save_original_photo(self):
        if self.active_drawer is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir çekmece seçin!")
            return
        drawer_num = self.active_drawer
        camera_nums = [1, 2]
        for camera_num in camera_nums:
            folder_path = f"photos/cekmece{drawer_num}/camera{camera_num}"
            os.makedirs(folder_path, exist_ok=True)
            
            ret, frame = self.capture1.read() if camera_num == 1 else self.capture2.read()
            if ret:
                photo_path = os.path.join(folder_path, f"cam{camera_num}_photo{self.count1}.jpg")
                cv2.imwrite(photo_path, frame)
                print(f"Orijinal fotoğraf kaydedildi: {photo_path}")
    
    def save_processed_photo(self):
        if self.active_drawer is None:
            QMessageBox.warning(self, "Uyarı", "Lütfen önce bir çekmece seçin!")
            return
        drawer_num = self.active_drawer
        camera_nums = [1, 2]
        for camera_num in camera_nums:
            folder_path = f"photos/cekmece{drawer_num}/camera{camera_num}"
            os.makedirs(folder_path, exist_ok=True)
            
            ret, frame = self.capture1.read() if camera_num == 1 else self.capture2.read()
            if ret:
                # Kalibrasyon sonrası düzeltme işlemi
                map1, map2, map1_0014, map2_0014 = foto.setCameraParameter()
                frame = cv2.remap(frame, map1, map2, interpolation=cv2.INTER_LINEAR)
                photo_path = os.path.join(folder_path, f"cam{camera_num}_processed{self.count2}.jpg")
                cv2.imwrite(photo_path, frame)
                print(f"Kalibre fotoğraf kaydedildi: {photo_path}")
    
    def toggle_fullscreen_cam1(self):
        if not self.fullscreen:
            self.fullscreen = True
            self.image_label2.hide()
            self.image_label1.setFixedSize(1028, 720)
            self.image_label1.show()
            self.cam2_fullscreen.show()
            self.cam1_fullscreen.hide()
            self.exit_fullscreen_button.show()
            #self.cam2_fullscreen.clicked(lambda: self.toggle_fullscreen(2))

    def toggle_fullscreen_cam2(self):
        if not self.fullscreen:
            self.fullscreen = True
            self.image_label1.hide()
            self.image_label2.setFixedSize(1028, 720)
            self.image_label2.show()
            self.cam1_fullscreen.show()
            self.cam2_fullscreen.hide()
            self.exit_fullscreen_button.show()
            #self.cam2_fullscreen.clicked(lambda: self.toggle_fullscreen(2))

    def switch_fullscreen(self, camera_id):
        if self.cam1_fullscreen.clicked():
            self.toggle_fullscreen(1)
        elif self.cam2_fullscreen.clicked():
            self.toggle_fullscreen(2)
        else:
            print("Geçersiz kamera paramtresi, lütfen dosya yolunu kontrol edin.")
            
    def toggle_fullscreen(self, camera_id):
        if not self.fullscreen:
            self.fullscreen = True
            if camera_id == 1:
                self.image_label2.hide()
                self.cam2_fullscreen.hide()
                self.image_label1.setFixedSize(1028, 720)
                self.image_label1.show()
            elif camera_id == 2:
                self.image_label1.hide()
                self.cam1_fullscreen.hide()
                self.image_label2.setFixedSize(1028, 720)
                self.image_label2.show()
            else:
                print("Geçersiz kamera parametresi.")
            self.exit_fullscreen_button.show()

    # Unit test - 1
    def test(self):
        if self.cam2_fullscreen.clicked():
            print("VALID")

    def exit_fullscreen(self):
        self.fullscreen = False
        self.cam1_fullscreen.show()
        self.cam2_fullscreen.show()
        self.image_label1.show()
        self.image_label2.show()
        self.image_label1.setFixedSize(1028, 320)
        self.image_label2.setFixedSize(1028, 320)
        self.exit_fullscreen_button.hide()
        
    def update_frame(self):
        for cam_id, capture, label in [(0, self.capture1, self.image_label1), (2, self.capture2, self.image_label2)]:
            ret, frame = capture.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)
                label.setPixmap(pixmap)

    def closeEvent(self, event):
        print("Çıkış yapılıyor...")
        QTimer.singleShot(500, QApplication.instance().quit)
        event.ignore()

    # Unit test - 2
    def to_thread(self, funct):
        self._thread = threading.Thread(target=funct)
        self._thread.start()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ToolControlUI()
    win.show()
    sys.exit(app.exec_())