"""
    fotogra_cekme_algoritma_lb revize - özlem
"""

import os
import time
import cv2
import numpy as np

checkerboard_image_path = "/home/tai-orin/Desktop/ats_new/images/1.jpg"

def load_coefficients(file_path):
    """ Loads camera matrix and distortion coefficients. """
    cv_file = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()
    cv_file.release()
    return [camera_matrix, dist_matrix]


def inside_parameter():
    K, D = load_coefficients("/home/tai-orin/Desktop/ats_new/matris_dosyalari/0367")
    K_0014, D_0014 = load_coefficients("/home/tai-orin/Desktop/ats_new/matris_dosyalari/0014")
    DIM = (1280, 720)
    K = np.array(K)
    D = np.array(D)
    K_0014 = np.array(K_0014)
    D_0014 = np.array(D_0014)

    balance = 0.0
    img = cv2.imread(checkerboard_image_path)
    dim1 = img.shape[:2][::-1]
    dim2 = None
    dim3 = None
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]
    scaled_K[2][2] = 1.5
    scaled_K_0014 = K_0014 * dim1[0] / DIM[0]
    scaled_K_0014[2][2] = 1.5

    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, dim3, cv2.CV_32F)

    new_K_0014 = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K_0014, D_0014, dim2, np.eye(3),
                                                                        balance=balance)
    map1_0014, map2_0014 = cv2.fisheye.initUndistortRectifyMap(K_0014, D_0014, np.eye(3), new_K_0014, dim3, cv2.CV_32F)

    return map1, map2, map1_0014, map2_0014


def same_settings():
    # For Camera - 1
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=sharpness=127")  #
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=saturation=28")  #
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=brightness=-1")  #
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=tilt_absolute=0")  #
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=pan_absolute=0")  #

    # For Camera - 2
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=tilt_absolute=0")  #
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=pan_absolute=0")  #


def setCameraParameter():
    map1, map2, map1_0014, map2_0014 = inside_parameter()
    same_settings()
    # Set Camera-1 Parameters
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=exposure_auto=1")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=exposure_absolute=14")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=gain=9")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=zoom_absolute=100")

    # Set Camera-2 Parameters
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=exposure_auto=1")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=exposure_absolute=15")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=gain=9")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=sharpness=127")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=saturation=28")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=brightness=-1")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=zoom_absolute=100")

    return map1, map2, map1_0014, map2_0014


def setCameraParameter120():
    map1, map2, map1_0014, map2_0014 = inside_parameter()
    same_settings()

    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=zoom_absolute=120")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=zoom_absolute=120")

    return map1, map2, map1_0014, map2_0014


def setCameraParameter150():
    map1, map2, map1_0014, map2_0014 = inside_parameter()
    same_settings()

    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=zoom_absolute=150")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=zoom_absolute=150")

    return map1, map2, map1_0014, map2_0014


def setCameraParameterAuto():
    map1, map2, map1_0014, map2_0014 = inside_parameter()

    # Set Camera-1 Parameters
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=brightness=0")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=contrast=10")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=saturation=16")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=white_balance_temperature_auto=1")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=gamma=220")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=gain=1")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=sharpness=16")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=exposure_auto=0")
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl=zoom_absolute=140")

    # Set Camera-2 Parameters
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=brightness=0")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=contrast=10")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=saturation=16")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=white_balance_temperature_auto=1")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=gamma=220")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=gain=1")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=sharpness=16")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=exposure_auto=0")
    os.system("v4l2-ctl -d /dev/video2 --set-ctrl=zoom_absolute=140")

    return map1, map2, map1_0014, map2_0014


# kamera kontrol classı
class CameraControl:
    def __init__(self):
        self.camera_set = False
        self.drawerOpened = False
        self.drawerNum = 1
        self.FRAME_COUNT = 10
        self.frameAvailability = [0] * self.FRAME_COUNT
        self.currentFrames = [None] * self.FRAME_COUNT
        self.current_frame = None
        self.video_capture = cv2.VideoCapture(0)  # Kamera açma (yerel kamera)

    def set_camera_parameters(self):

        if self.drawerNum == 1:
            self.map1, self.map2 = setCameraParameter()
        elif self.drawerNum == 2:
            self.map1, self.map2 = setCameraParameter120()
        elif self.drawerNum == 3:
            self.map1, self.map2 = setCameraParameter120()
        elif self.drawerNum == 4:
            self.map1, self.map2 = setCameraParameter120()
        elif self.drawerNum == 5:
            self.map1, self.map2 = setCameraParameter120()
        elif self.drawerNum == 6:
            self.map1, self.map2 = setCameraParameter150()
        else:
            self.map1, self.map2 = setCameraParameter()

    def capture_image(self):
        # Kamera görüntüsünü çekme ve kaydetme
        _, self.current_frame = self.video_capture.read()
        if self.current_frame is not None:
            folder_path = f"photos/cekmece{self.drawerNum}/camera1/1"
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, f"foto_1.jpg")
            cv2.imwrite(file_path, self.current_frame)
            print(f"Fotoğraf kaydedildi: {file_path}")

    def on_drawer_button_pressed(self, drawer_num):
        self.drawerNum = drawer_num
        self.set_camera_parameters()
        self.capture_image()
        print(f"Çekmece {drawer_num} başarıyla açıldı.")

"""    def endless_loop(self):
        while True:
            if self.drawerOpened:
                self.on_drawer_button_pressed(self.drawerNum)
            time.sleep(0.1)  #aşırı yüklemeyi onlemek için      """

#-----------------------------------------------

zoomValue = str(os.popen("v4l2-ctl --get-ctrl=zoom_absolute").read())

K, D = load_coefficients("matris_dosyalari/0367")
K_0014, D_0014 = load_coefficients("matris_dosyalari/0014")
DIM = (1280, 720)
K = np.array(K)
D = np.array(D)
K_0014 = np.array(K_0014)
D_0014 = np.array(D_0014)

balance = 0.0
img = cv2.imread(checkerboard_image_path)
dim1 = img.shape[:2][::-1]
dim2 = None
dim3 = None
if not dim2:
    dim2 = dim1
if not dim3:
    dim3 = dim1
scaled_K = K * dim1[0] / DIM[0]
scaled_K[2][2] = 1.5
scaled_K_0014 = K_0014 * dim1[0] / DIM[0]
scaled_K_0014[2][2] = 1.5

counter = 0
new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), new_K, dim3, cv2.CV_32F)
h_, w_ = (720, 1280)

new_K_0014 = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K_0014, D_0014, dim2, np.eye(3),
                                                                    balance=balance)
map1_0014, map2_0014 = cv2.fisheye.initUndistortRectifyMap(K_0014, D_0014, np.eye(3), new_K_0014, dim3, cv2.CV_32F)
