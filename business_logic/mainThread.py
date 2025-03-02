# PyQt Libs
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject, pyqtSignal

# built-in libs
import multiprocessing
import time
import shutil

# User Packages
from business_logic.fotograf_cekme_algoritmasi import *
from business_logic.SensorReading import VL53

class TakePhoto(QObject):

	drawerTrigger = pyqtSignal(int)
	openedDrawersTrigger = pyqtSignal(list)

	def __init__(self):		
		super().__init__()
		
		self.FRAME_COUNT = 6
		self.openedDrawerList = []
		
		self.frameAvailability = [0]*self.FRAME_COUNT
		self.txtWriteArr = [0]*6

		self.terminate = False
		self.debugCnt = 0

		self.cam1_path = " v4l2src device=/dev/video0 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
		self.cam2_path = " v4l2src device=/dev/video2 ! image/jpeg, format=MJPG, framerate=60/1, width=1280, height=720 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
		
	def readVideo_1(self, drawerNum, map1, map2):
		#_, self.current_frame = video_capture.read()
		self.remapPhoto_1(map1, map2)
		self.cropImage_1(drawerNum)

	def readVideo_2(self, drawerNum, map1, map2):
		#_2, self.current_frame_2 = video_capture_2.read()
		self.remapPhoto_2(map1, map2)
		self.cropImage_2(drawerNum)
		
	def remapPhoto_1(self, map1, map2):
		current_frame = cv2.cuda_GpuMat(self.current_frame)
		map1_cuda = cv2.cuda_GpuMat(map1)
		map2_cuda = cv2.cuda_GpuMat(map2)
		self.current_frame = cv2.cuda.remap(current_frame, map1_cuda, map2_cuda, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)

	def remapPhoto_2(self, map1_0014, map2_0014):
		current_frame_2 = cv2.cuda_GpuMat(self.current_frame_2)
		map1_0014_cuda = cv2.cuda_GpuMat(map1_0014)
		map2_0014_cuda = cv2.cuda_GpuMat(map2_0014)
		self.current_frame_2 = cv2.cuda.remap(current_frame_2, map1_0014_cuda, map2_0014_cuda, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
		
	def cropImage_1(self, drawerNum):
		if drawerNum == 1:	
			self.current_frame = cv2.cuda_GpuMat(self.current_frame, [150, 0 + h_ - 175], [100, 0 + w_ - 315])
		elif drawerNum == 2:
			self.current_frame = cv2.cuda_GpuMat(self.current_frame, [195, 0 + h_ - 255], [223, 0 + w_ - 131])
		elif drawerNum == 3:
			self.current_frame = cv2.cuda_GpuMat(self.current_frame, [225, 0 + h_ - 285],[332, 0 + w_ - 475])
		elif drawerNum == 4:
			self.current_frame = cv2.cuda_GpuMat(self.current_frame, [0, 0 + h_ - 0], [0, 0 + w_ - 0])
		elif drawerNum == 5:
			self.current_frame = cv2.cuda_GpuMat(self.current_frame, [311, 0 + h_ - 165], [290, 0 + w_ - 175])
		elif drawerNum == 6:
			self.current_frame = cv2.cuda_GpuMat(self.current_frame, [0, 0 + h_ - 0], [0, 0 + w_ - 0])
		else:
			self.current_frame = cv2.cuda_GpuMat(self.current_frame, [140, 0 + h_ - 200], [150, 0 + w_ - 0])

	def cropImage_2(self, drawerNum):
		if drawerNum == 1:	
			self.current_frame_2 = cv2.cuda_GpuMat(self.current_frame_2, [120, 0 + h_ - 192], [25, 0 + w_ - 177])  
		elif drawerNum == 2:
			self.current_frame_2 = cv2.cuda_GpuMat(self.current_frame_2, [180, 0 + h_ - 250], [360, 0 + w_ - 325])  
		elif drawerNum == 3:
			self.current_frame_2 = cv2.cuda_GpuMat(self.current_frame_2, [226, 0 + h_ - 295], [235, 0 + w_ - 375]) 
		elif drawerNum == 4:
			self.current_frame_2 = cv2.cuda_GpuMat(self.current_frame_2,[258, 0 + h_ - 310], [0, 0 + w_ - 450])
		elif drawerNum == 5:
			self.current_frame_2 = cv2.cuda_GpuMat(self.current_frame_2, [268, 0 + h_ - 315], [40, 0 + w_ - 480]) 
		elif drawerNum == 6:
			self.current_frame_2 = cv2.cuda_GpuMat(self.current_frame_2, [281, 0 + h_ - 325], [170, 0 + w_ - 508]) 
		else:
			self.current_frame_2 = cv2.cuda_GpuMat(self.current_frame_2, [190, 0 + h_ - 200], [0, 0 + w_ - 150])

	def mainThreadFunction(self):
		
		self.video_capture = cv2.VideoCapture(cam1_path, cv2.CAP_GSTREAMER)
		self.video_capture_2 = cv2.VideoCapture(cam2_path, cv2.CAP_GSTREAMER)

		self.sensor = VL53()
		
		self.currentFrames = [0]*self.FRAME_COUNT
		self.currentFrames_2 = [0]*self.FRAME_COUNT
		self.frameAvailability_2 = [0]*self.FRAME_COUNT
		self.lastDrawerStatus = 0
		self.camera_set = True
		
		self.motion_detected = False
		self.camera_set_1 = False
		self.closed_flag = 1

		self.counter_cekmece4 = 0
		self.prev_frame_time = 0
		self.new_frame_time = 0

	def endless_loop(self): # ArUco Reading instead of sensor bytes reading

		pass

	def endlessLoop(self):
	#time.sleep(0.0001)
		try:
			self.sensor.readBytes() # VL53 mesafe sensörü dependency
			self.drawerChanged = self.sensor.isDrawerChanged()
			self.drawerOpened = self.sensor.isDrawerOpened()
			# if self.drawerOpened != self.lastDrawerStatus:
			# 	self.counter_cekmece4 += 1
			self.lastDrawerStatus = self.drawerOpened
			currentDistance = self.sensor.getFilteredDistance()
			self.sensor.distance = currentDistance
			if self.camera_set == True or self.drawerChanged == 1:
				self.sensor.drawerChanged = 0	
					
				self.currentFrames = [0]*self.FRAME_COUNT
				self.frameAvailability = [0]*self.FRAME_COUNT
				self.drawerNum = self.sensor.getCurrentDrawer()
				
				if self.txtWriteArr[self.drawerNum - 1] == 0 and self.drawerNum > 0 and self.drawerNum != 99:
					self.txtWriteArr[self.drawerNum - 1] = 1
					self.openedDrawerList.append(self.drawerNum)
					self.openedDrawersTrigger.emit(self.openedDrawerList)
				
				# print(str(self.drawerNum))

				if self.drawerNum == 1:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = setCameraParameter()
				elif self.drawerNum == 2:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = setCameraParameter120()
				elif self.drawerNum == 3:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = setCameraParameter120()
				elif self.drawerNum == 4:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = setCameraParameter120()
				elif self.drawerNum == 5:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = setCameraParameter120()
				elif self.drawerNum == 6:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = setCameraParameter150()
				else:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = setCameraParameter()
			
			self.camera_set = False			
			print("Distance: " + str(currentDistance))
			if self.closed_flag == 0 and self.drawerOpened == 0:
				self.drawerTrigger.emit(0)
				for i in range(self.FRAME_COUNT):
					if self.frameAvailability[i] != 0:
							self.currentFrames[i] = self.currentFrames[i].download()
							cv2.imwrite("photos/cekmece"  + str(self.drawerNum) + "/camera1/1/al_camera0367_foto_" + str(i) + "_1.jpg",self.currentFrames[i])
					if self.frameAvailability_2[i] != 0:
							self.currentFrames_2[i] = self.currentFrames_2[i].download()
							cv2.imwrite("photos/cekmece"  + str(self.drawerNum) + "/camera2/1/al_camera0367_foto_" + str(i) + "_2.jpg",self.currentFrames_2[i])

				self.currentFrames = [0]*self.FRAME_COUNT
				self.currentFrames_2 = [0]*self.FRAME_COUNT
				self.frameAvailability = [0]*self.FRAME_COUNT
				self.frameAvailability_2 = [0]*self.FRAME_COUNT
							
				self.closed_flag = 1

			if self.drawerOpened == 1:
				_2, self.current_frame_2 = self.video_capture_2.read()					
				_, self.current_frame = self.video_capture.read()
				self.drawerTrigger.emit(self.drawerNum)
				value_changed = 0
				if self.camera_set_1 == False or self.drawerChanged == 1:
					# self.drawerTrigger.emit(self.drawerNum)
					drawer_variable = 1
					counterFirstDrawer = 1
					try:
					
						os.mkdir("photos/cekmece" + str(self.drawerNum) + "/camera1/1")
						os.mkdir("photos/cekmece" + str(self.drawerNum) + "/camera2/1")
					except:
						pass
					
					self.camera_set_1 = True

				if  self.sensor.incomingData == 1:
						
					if self.drawerNum == 4:
						if currentDistance > 307 and currentDistance < 323:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability_2[0] = 1

						elif currentDistance > 380 and currentDistance < 392:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1

						elif currentDistance > 462 and currentDistance < 475:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[2] = self.current_frame_2

							self.frameAvailability_2[2] = 1

					elif self.drawerNum == 1:
						if currentDistance > 216 and currentDistance < 227:
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014)  
							self.currentFrames[0] = self.current_frame
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability[0] = 1
							self.frameAvailability_2[0] = 1
						
						elif currentDistance > 340 and currentDistance < 352:
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014)
							self.currentFrames[1] = self.current_frame
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability[1] = 1
							self.frameAvailability_2[1] = 1
						
						elif currentDistance > 435 and currentDistance < 450:
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames[2] = self.current_frame
							self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability[2] = 1
							self.frameAvailability_2[2] = 1
						
					elif self.drawerNum == 2:
						if currentDistance > 213 and currentDistance < 226:
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames[0] = self.current_frame
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability[0] = 1
							self.frameAvailability_2[0] = 1

						elif currentDistance > 309 and currentDistance < 320:
							self.readVideo_1(self.drawerNum, self.map1, self.map2)
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames[1] = self.current_frame 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability[1] = 1
							self.frameAvailability_2[1] = 1

						elif currentDistance > 374 and currentDistance < 386:
							self.readVideo_1(self.drawerNum, self.map1, self.map2)
							#self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014)  
							self.currentFrames[2] = self.current_frame
							#self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability[2] = 1
							#self.frameAvailability_2[2] = 1

						elif currentDistance > 435 and currentDistance < 448:

							self.readVideo_1(self.drawerNum, self.map1, self.map2)
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames[3] = self.current_frame
							self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability[3] = 1
							self.frameAvailability_2[2] = 1

					elif self.drawerNum == 5:
						if currentDistance > 194 and currentDistance < 210:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability_2[0] = 1

						elif currentDistance > 400 and currentDistance < 415:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1

					elif self.drawerNum == 3:
						if currentDistance > 216 and currentDistance < 233:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability_2[0] = 1
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.currentFrames[0] = self.current_frame
							self.frameAvailability[0] = 1

						elif currentDistance > 350 and currentDistance < 367:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1
							
						elif currentDistance > 462 and currentDistance < 475:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability_2[2] = 1
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.currentFrames[1] = self.current_frame
							self.frameAvailability[1] = 1

					elif self.drawerNum == 6:
						if currentDistance > 210 and currentDistance < 220:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability_2[0] = 1

						elif currentDistance > 318 and currentDistance < 328:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1

						elif currentDistance > 410 and currentDistance < 420:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability_2[2] = 1

						elif currentDistance > 465 and currentDistance < 475:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[3] = self.current_frame_2
							self.frameAvailability_2[3] = 1
			
					self.sensor.incomingData = 0
					self.closed_flag = 0
		except Exception as e:
			print("Patladık: ", e)