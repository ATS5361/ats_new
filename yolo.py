from PyQt5 import QtCore, QtGui, QtWidgets , QtSerialPort
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from fillprofile_30mayis import Ui_Dialog3
import sys
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.Qt import Qt
import images_rc
import imutils
import cv2
import numpy as np
import time
import serial
import serial.tools.list_ports
#import threading
import os
from random import randint
import sqlite3
from datetime import datetime


start = time.time()
image2 = cv2.imread('fotograflar_2/sonuclar/cekmece1/camera1/1/result_camera1.jpg')
image1 = cv2.imread('fotograflar_2/sonuclar/cekmece1/camera2/1/result_camera2.jpg')

image1 = cv2.resize(image1,(300,300))
image2 = cv2.resize(image2,(300,300))

print(cv2.getBuildInformation())
tool = {   "0" : "Nut Driver", "1" : "Socket Deep", "17" : "Big_Socket", "2" : "Small_Socket","3" : "1/4 Drive Hex Bit Socket", "5" : "Big_Socket, 1/4 Dr M Series", "4" : "Small_Socket, 1/4 Dr M Series", "9" : "1/4 Drive Deep Socket ", "8" : "1/4 Drive Socket", "7" : "1/4 Drive Magnetic Bit Holder 1/4 Hex","6" : "Proto Drive Adapter", "10":  "Proto 1/4 Drive Flexible Extension 6-1/4","11" : "Proto 1/4 Drive Extension 3", "12" : "Proto 1/4 Drive Extension 2", "13" : "Proto 1/4 Drive Extension 6", "14" : "Proto 1/4 Drive Extension 14-3/32", "15" : "1/4 Drive Dual 80 Technology Standart Handle Ratchet" , "16" : "Proto 1/4 Drive Socket Drive", "18" : "Precision Screwdrivers Set 6 pcs", "19" : "Wire Cutters", "20" : "Plier Diagonal Midget W/G", "21" : "Electronics Diagonal Cutter Piller", "22" : "Short Non-Serrated Jaws 4 5/8","23" : "45 Serrated Jaws 6" }

obj_index_1_1 = [5,4,3,2,1,0]
LABELS = open("detection_dosyalari/1.cekmece_helloA_versiyonu.names").read().strip().split("\n")
net = cv2.dnn.readNetFromDarknet("detection_dosyalari/1.cekmece_helloA_versiyonu.cfg", "detection_dosyalari/1.cekmece_helloA_versiyonu.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
obj_index_1_2 = [17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
LABELS_2 = open("detection_dosyalari/1.cekmece_helloB_versiyonu_gecici.names").read().strip().split("\n")
net2 = cv2.dnn.readNetFromDarknet("detection_dosyalari/1.cekmece_helloB_versiyonu_gecici.cfg", "detection_dosyalari/1.cekmece_helloB_versiyonu_gecici.weights")
net2.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net2.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

for y in range(2):

	print("3")
	if y == 0:
		image = image1
		ln = net.getLayerNames()
		ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (256, 256), swapRB=True, crop=False)
		net.setInput(blob)
		layerOutputs = net.forward(ln)

		a = 0

	elif y == 1:
		image = image2
		ln = net2.getLayerNames()
		ln = [ln[i[0] - 1] for i in net2.getUnconnectedOutLayers()]
		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (256, 256), swapRB=True, crop=False)
		net2.setInput(blob)
		layerOutputs = net2.forward(ln)

		a = 1


	(H, W) = image.shape[:2]

	
	boxes = []
	confidences = []
	classIDs = []

	for output in layerOutputs:

		for detection in output:

			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			if confidence > 0.5:
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				boxes.append([x, y, int(width), int(height)])


				confidences.append(float(confidence))
				classIDs.append(classID)


	classIDs = list(classIDs)
	classes = []

	classes1 = []
	classes2 = []
	classes3 = []
	classes4 = []

	idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

	if len(idxs) > 0:

		if a == 0 :
			for i in idxs.flatten():
				classes1.append(classIDs[i])
				classes1 = list(classes1)
				(x,y) = (boxes[i][0], boxes[i][1])
				(w,h) = (boxes[i][2], boxes[i][3])
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				text = "{}".format(classIDs[i])
				cv2.putText(image,text,(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,0),2)
				cv2.imwrite("detectedA1_yeni.jpg",image)
			

		elif a == 1 :
			for i in idxs.flatten():
				classes2.append(classIDs[i])
				classes2 = list(classes2)
				(x,y) = (boxes[i][0], boxes[i][1])
				(w,h) = (boxes[i][2], boxes[i][3])
				cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
				text = "{}".format(classIDs[i])
				cv2.putText(image,text,(x,y-5),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,0),2)
				cv2.imwrite("detectedB1_yeni.jpg",image)
end = time.time()
print("[BİLGİ] YOLO took {:.6f} seconds".format(end - start))
