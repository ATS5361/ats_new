import sys
import cv2
import cv2.aruco as aruco
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QIcon

""" ÇALIŞAN VERSİYON """

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

    def __init__(self, width=800, height=600):
        super().__init__()
        self.setWindowTitle("ArUco Testing")
        self.setGeometry(100, 100, 1000, 500)
        self.setWindowIcon(QIcon("images/tai-logo-color.png"))
        self.initUI()
        
        # ArUco tanımları
        self.aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_100)
        self.parameters = aruco.DetectorParameters_create()

        # Kamera işleme iş parçacığı başlatma
        self.camera_thread1 = CameraThread("v4l2src device=/dev/video0 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! nvvideoconvert ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", self.aruco_dict, self.parameters)
        self.camera_thread2 = CameraThread("v4l2src device=/dev/video2 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! nvvideoconvert ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1", self.aruco_dict, self.parameters)

        # Marker'ları kaydetmek için set
        self.detected_ids = set()  # Set kullanarak her ID'yi bir kez kaydedelim
        self.current_marker = None  # Şu anki marker

        self.camera_thread1.new_frame.connect(self.process_frame1)
        self.camera_thread2.new_frame.connect(self.process_frame2)

        # Kameraları başlat
        self.camera_thread1.start()
        self.camera_thread2.start()

    def initUI(self):
        main_layout = QVBoxLayout()
        self.screenlabel1 = QLabel("Kamera 1")
        self.screenlabel2 = QLabel("Kamera 2")
        self.screenlabel1.setFixedSize(1028, 320)
        self.screenlabel2.setFixedSize(1028, 320)
        
        main_layout.addWidget(self.screenlabel1)
        main_layout.addWidget(self.screenlabel2)
        self.setLayout(main_layout)
    
    def keyPressEvent(self, event):
        print(f"Key pressed: {event.key()}")
        if event.key() == Qt.Key_Escape:
            print("ESC tıklandı. Uygulama kapanıyor...")
            QApplication.instance().quit()

    def process_frame1(self, frame, ids, corners):
        try:
            if ids is not None:
                aruco.drawDetectedMarkers(frame, corners, ids)
                for i in range(len(ids)):
                    marker_id = ids[i][0]
                    if marker_id not in self.detected_ids and marker_id <= 17:  # Eğer marker daha önce tanımlanmadıysa
                        self.detected_ids.add(marker_id)  # Marker ID'yi kaydet
                        print(f"{self.marker_dict[marker_id]}") # Yeni marker ID'sini yazdır
                    elif marker_id != self.current_marker:  # Eğer marker zaten tanındı fakat farklı bir marker göründü
                        self.current_marker = marker_id  # Yeni marker'ı current_marker olarak kaydet
                        print(f"{self.marker_dict[marker_id]}")  # Yeni current marker ID'sini yazdır
            self.display_image(self.screenlabel1, frame)
        except KeyError as err:
            pass

    def process_frame2(self, frame, ids, corners):
        try:
            if ids is not None:
                aruco.drawDetectedMarkers(frame, corners, ids)
                for i in range(len(ids)):
                    marker_id = ids[i][0]
                    if marker_id not in self.detected_ids and marker_id <= 17:  # Eğer marker daha önce tanımlanmadıysa
                        self.detected_ids.add(marker_id)  # Marker ID'yi kaydet
                        print(f"{self.marker_dict[marker_id]}") # Yeni marker ID'sini yazdır
                    elif marker_id != self.current_marker:  # Eğer marker zaten tanındı fakat farklı bir marker göründü
                        self.current_marker = marker_id  # Yeni marker'ı current_marker olarak kaydet
                        print(f"{self.marker_dict[marker_id]}")  # Yeni current marker ID'sini yazdır
            self.display_image(self.screenlabel2, frame)
        except KeyError as err:
            pass

    def display_image(self, label, frame):
        """ OpenCV görüntüsünü QLabel'e çevirip gösterir. """
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        label.setPixmap(QPixmap.fromImage(qimg))

    def keyPressEvent(self, event):
        """
            Enables users to pass between the Login UI And Tool Window.
            Click esc to shut down the system.
        """
        print(f"Key pressed: {event.key()}")
        if event.key() == Qt.Key_Escape:
            print("ESC tıklandı. Uygulama kapanıyor...")
            QApplication.instance().quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ArUcoTesting()
    win.show()
    sys.exit(app.exec_())