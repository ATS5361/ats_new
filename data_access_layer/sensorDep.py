# This file is created for handling SENSOR dependencies to prevent "sphagetti code"

photo = MT.TakePhoto()


def debugCam(self):
    if self.toolWindow.isVisible():
        if self.toolWindow.drawerIsOpen and self.debugLastDistance == photo.sensor.avgDistance and photo.sensor.avgDistance > 160:
            self.debugCnt +=1
        else:
            self.debugCnt = 0
        
        if self.debugCnt >= 5:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Beklenmedik bir hata ile karşılaşıldı. Tüm çekmecelerin kapalı olduğundan emin olun ve 'OK' butonuna tıklayarak\ntekrar giriş yapın.")
            msg.setWindowTitle("HATA")
            retunVal = msg.exec_()
            if (retunVal == QMessageBox.Ok):
                self.toolWindow.closeWindow()
            self.debugCnt = 0
        self.debugLastDistance = photo.sensor.avgDistance
        #os.system("python3 _main.py &")

def disconnectSensor(self):
    photo.sensor.setToolboxOff()
    self.toolWindow.triggerDetectSignal()
    photo.terminate = True
    time.sleep(0.1)
    del photo.sensor
    time.sleep(0.1)
    photo.txtWriteArr = [0]*6
    photo.openedDrawerList = []
    self.toolWindow.updateDrawers(photo.openedDrawerList)
    self.workerThread.quit()
    self.workerThread.exit()
    del self.workerThread
    time.sleep(0.1)
    photo.video_capture_2.release()
    photo.video_capture.release()
    self.setLastStatus()
    self.setStatusLabel()

def openToolWindow(self):
    photo.mainThreadFunction()
    photo.terminate = False
    self.workerThread = MainThread()
    self.workerThread.start()
        
    self.toolWindow.show()
    time.sleep(2)
    photo.sensor.setToolboxOn()
    self.toolWindow.passwordEntry.show()
    self.toolWindow.passwordEntry.setFocus(True)
    self.toolWindow.autoCloseTimer.start()