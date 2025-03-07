# Necessary Libraries
import os
import cv2
from PyQt5.QtCore import QObject, pyqtSignal
import business_logic.fotograf_cekme_algoritmasi as fotograf
import aruco_deneme2

# Class Structure for Taking Photos
class TakePhoto(QObject):
	drawerTrigger = pyqtSignal(int)
	openedDrawersTrigger = pyqtSignal(list)

	drawerMap = {0: 1,
			  	 1: 1,
				 2: 1,
				 3: 2,
			  	 4: 2,
				 5: 2,
				 6: 3,
			  	 7: 3,
				 8: 3,
				 9: 4,
			  	 10: 4,
				 11: 4,
				 12: 5,
			  	 13: 5,
				 14: 5,
				 15: 6,
			  	 16: 6,
				 17: 6
				 }

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
		# Initial Setup
		self.video_capture = cv2.VideoCapture(self.cam1_path, cv2.CAP_GSTREAMER)
		self.video_capture_2 = cv2.VideoCapture(self.cam2_path, cv2.CAP_GSTREAMER)
		
		self.currentFrames = 		[0]*(self.FRAME_COUNT)
		self.currentFrames_2 = 		[0]*(self.FRAME_COUNT)
		self.frameAvailability_2 = 	[0]*(self.FRAME_COUNT)
		self.lastDrawerStatus = 0
		self.camera_set = True
		self.incomingData = 0		
		self.motion_detected = False

		self.camera_set_1 = False
		self.closed_flag = 1

		self.counter_cekmece4 = 0
		self.prev_frame_time = 0
		self.new_frame_time = 0

	def endlessLoop(self):
		try:
			if self.camera_set == True or self.drawerChanged == 1:
					
				self.currentFrames = [0]*self.FRAME_COUNT
				self.frameAvailability = [0]*self.FRAME_COUNT
				self.drawerNum = self.drawerMap[aruco_deneme2.current_marker] # Map the values into self.drawerMap
				
				if self.txtWriteArr[self.drawerNum - 1] == 0 and self.drawerNum > 0 and self.drawerNum != 99:
					self.txtWriteArr[self.drawerNum - 1] = 1
					self.openedDrawerList.append(self.drawerNum)
					self.openedDrawersTrigger.emit(self.openedDrawerList)

				if self.drawerNum == 1:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = fotograf.setCameraParameter()
				elif self.drawerNum == 2:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = fotograf.setCameraParameter120()
				elif self.drawerNum == 3:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = fotograf.setCameraParameter120()
				elif self.drawerNum == 4:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = fotograf.setCameraParameter120()
				elif self.drawerNum == 5:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = fotograf.setCameraParameter120()
				elif self.drawerNum == 6:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = fotograf.setCameraParameter150()
				else:
					self.map1 , self.map2 , self.map1_0014 ,self.map2_0014 = fotograf.setCameraParameter()
			
			self.camera_set = False			
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

				if  self.incomingData == 1:
					if self.drawerNum == 1:
						if aruco_deneme2.current_marker == 0:
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014)  
							self.currentFrames[0] = self.current_frame
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability[0] = 1
							self.frameAvailability_2[0] = 1
						
						elif aruco_deneme2.current_marker == 1:
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014)
							self.currentFrames[1] = self.current_frame
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability[1] = 1
							self.frameAvailability_2[1] = 1
						
						elif aruco_deneme2.current_marker == 2:
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames[2] = self.current_frame
							self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability[2] = 1
							self.frameAvailability_2[2] = 1

					elif self.drawerNum == 2:
						if aruco_deneme2.current_marker == 5:
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames[0] = self.current_frame
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability[0] = 1
							self.frameAvailability_2[0] = 1

						elif aruco_deneme2.current_marker == 4:
							self.readVideo_1(self.drawerNum, self.map1, self.map2)
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames[1] = self.current_frame 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability[1] = 1
							self.frameAvailability_2[1] = 1

						elif aruco_deneme2.current_marker == 3:

							self.readVideo_1(self.drawerNum, self.map1, self.map2)
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames[3] = self.current_frame
							self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability[3] = 1
							self.frameAvailability_2[2] = 1

					elif self.drawerNum == 3:
						if aruco_deneme2.current_marker == 8:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability_2[0] = 1
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.currentFrames[0] = self.current_frame
							self.frameAvailability[0] = 1

						elif aruco_deneme2.current_marker == 7:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1
							
						elif aruco_deneme2.current_marker == 6:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability_2[2] = 1
							self.readVideo_1(self.drawerNum, self.map1, self.map2) 
							self.currentFrames[1] = self.current_frame
							self.frameAvailability[1] = 1

					elif self.drawerNum == 4:
						if aruco_deneme2.current_marker == 11:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability_2[0] = 1

						elif aruco_deneme2.current_marker == 10:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1

						elif aruco_deneme2.current_marker == 9:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[2] = self.current_frame_2

							self.frameAvailability_2[2] = 1

					elif self.drawerNum == 5:
						if aruco_deneme2.current_marker == 14:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability_2[0] = 1

						elif aruco_deneme2.current_marker == 13:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1
						
						elif aruco_deneme2.current_marker == 12:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1

					elif self.drawerNum == 6:
						if aruco_deneme2.current_marker == 15:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[0] = self.current_frame_2
							self.frameAvailability_2[0] = 1

						elif aruco_deneme2.current_marker == 16:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[1] = self.current_frame_2
							self.frameAvailability_2[1] = 1

						elif aruco_deneme2.current_marker == 17:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[2] = self.current_frame_2
							self.frameAvailability_2[2] = 1

						elif aruco_deneme2.current_marker == 17:
							self.readVideo_2(self.drawerNum, self.map1_0014, self.map2_0014) 
							self.currentFrames_2[3] = self.current_frame_2
							self.frameAvailability_2[3] = 1
			
					self.incomingData = 0
					self.closed_flag = 0
		except Exception as e:
			print("Patladık: ", e)