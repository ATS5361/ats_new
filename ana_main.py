"""
Bismillahirrahmanirrahim
"""
import sys

from PyQt5.QtCore import Qt, QSize, QSettings, QThread, pyqtSignal, QTime, QTimer, QDateTime, QDate
from PyQt5 import QtWidgets, QtGui, QtCore
from datetime import date, datetime

from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import *

from detectThread import *
import resources
from toolWindows import ToolWindow
from UserWindow import UserWindow
import time
import os
import sqlite3
import psycopg2
from mainThread import *
import json

import threading


# photo = TakePhoto()
# class MainThread(QThread):
#     threadSignal = pyqtSignal()
#     def run(self):
#     	photo.mainThreadFunction()

photo = TakePhoto()
class MainThread(QThread):
    threadSignal = pyqtSignal()
    def run(self):
        while(not photo.terminate):
            photo.endlessLoop()
            
        
class CustomDialog(QDialog):
    def __init__(self, parent = None):
        super(CustomDialog, self).__init__(parent)
        self.setWindowTitle("Toolbox Login Panel")

        self.setWindowFlag(Qt.FramelessWindowHint)
        

        self.toolWindow = ToolWindow()
        self.userWindow = UserWindow()	
        self.buttonSize = QSize(160, 160)
        self.setFont((QFont('Roboto', 15)))

        self.toolNotExistBackground = "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e63900, stop: 0.3  #ff531a,stop: 0.8  #ff531a, stop: 1.0  #e63900); font: bold;font-size: 58px;border-style: outset; border-width: 3px;border-color: #e63900; border-radius: 35px; "
        self.toolExistsBackground = "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #85e085, stop: 0.3  #47d147,stop: 0.8  #47d147, stop: 1.0  #70db70); font: bold;font-size: 58px;border-style: outset; border-width: 3px;border-color: #33cc33; border-radius: 35px;"

        photo.drawerTrigger.connect(self.toolWindow.updateOpenedDrawer)
        photo.openedDrawersTrigger.connect(self.toolWindow.updateDrawers)
        self.toolWindow.detectSignal.connect(self.setOpenedDrawers)
        self.statusLabel = QLabel(self)
        self.toolStatus = False
        self.missingTools = 0
        self.setMinimumSize(QtCore.QSize(1365, 745))
        self.setMaximumSize(QtCore.QSize(1365, 745))
        #self.setFixedSize(1280,960) 
        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setStyleSheet('font-size: 10pt; background-color: #101010')
        self.layout = QGridLayout()
        self.layout.setSpacing(13)
        #Set components of QDialog
        self.setButtons()
        self.setLastStatus()
        self.setStatusLabel()
        self.addLogo()
        self.databaseButton.clicked.connect(self.dataMigrate)
        self.loginButton.clicked.connect(self.readCardForLogin)
        self.rebootButton.clicked.connect(self.rebootSystem)
        self.shutDownButton.clicked.connect(self.shutDownSystem)
        self.userButton.clicked.connect(self.addUser)
        self.toolWindow.disconnectSignal.connect(self.disconnectSensor)
        self.toolWindow.updateStatusSignal.connect(self.updateStatus)
        self.toolWindowFlag = 1
        self.userWindowFlag = 0
        self.debugLastDistance = 0
        self.completeFlag = False
        
        self.timeLabel = QLabel()
        self.timeLabel.setStyleSheet("font-size: 18pt; background-color: blue")
        self.lastStatusOfTools = [self.toolWindow.lastStatusOfTools_1, 
                                  self.toolWindow.lastStatusOfTools_2,
                                  self.toolWindow.lastStatusOfTools_3,
                                  self.toolWindow.lastStatusOfTools_4,
                                  self.toolWindow.lastStatusOfTools_5,
                                  self.toolWindow.lastStatusOfTools_6]

        self.layout.addWidget(self.taiLogo, 0, 0, 1, 0)
        self.layout.addWidget(self.timeLabel, 0, 3)
        self.layout.addWidget(self.statusLabel,1, 0, 2, 5)
        # self.layout.addWidget(self.settingsButton, 3, 0)
        self.layout.addWidget(self.databaseButton, 3, 0)
        self.layout.addWidget(self.loginButton, 3, 2)
        self.layout.addWidget(self.userButton, 3, 1)
        self.layout.addWidget(self.rebootButton, 3, 3)
        self.layout.addWidget(self.shutDownButton, 3, 4)
        
        self.timeLabel.setStyleSheet("font-size: 15pt; color: white")
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()

        self.debugTimer = QtCore.QTimer(self)
        self.debugTimer.setInterval(100)
        self.debugTimer.timeout.connect(self.debugCam)
        self.debugTimer.start()
        #self.layout.setRowStretch(2, 0)
        self.passwordEntry = QLineEdit(self)
        self.passwordEntry.setFixedWidth(0)
        self.passwordEntry.move(100, 100)
        self.passwordEntry.textChanged.connect(self.passCheck)
        self.passwordEntry.hide()

        self.isForLogin = False

        self.setLayout(self.layout)
        self.readCard()
        runMain()

        
    def setLastStatus(self):
        with open("toolList.txt", "r") as dosya:
            i = 0
            total_dif = 0

            for satir in dosya:
                if i != 6:
                    self.toolWindow.lastStatusOfDrawers[i] = json.loads(satir)
                    missing_counter = 0
                    for index in self.toolWindow.lastStatusOfDrawers[i]:
                        if index == 0:
                            total_dif += 1
                            missing_counter += 1
                    self.toolWindow.toolLabels[i].setText(str(missing_counter))
                    
                    i += 1


            self.missingTools = total_dif
            if total_dif > 0:
                self.toolStatus = False
            else:
                self.toolStatus = True
        
        self.toolWindow.drawLastStatus()
            
            

            

    def setOpenedDrawers(self):
        changeDrawerList(photo.openedDrawerList)

    def passCheck(self):
        password = self.passwordEntry.text()
        if len(password) == 8:
            try:
                sqlConnectionAdm = sqlite3.connect('databaseFiles/for_add.db')
                cursorAdm = sqlConnectionAdm.cursor()
                cursorAdm.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM LOGIN WHERE PASSWORD =:password", {"password":password.upper()})
                recordroot = cursorAdm.fetchall()
                sqlConnectionUsr = sqlite3.connect('databaseFiles/LOGIN.db')
                cursorUsr = sqlConnectionUsr.cursor()
                cursorUsr.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM LOGIN WHERE PASSWORD =:password", {"password":password.upper()})
                recorduser = cursorUsr.fetchall()
                sqlConnectionAdm.close()
                sqlConnectionUsr.close()
                if len(recordroot) == 1 and self.isForLogin == False:
                    self.showButtons()
                elif len(recorduser) == 1:
                    if self.toolWindowFlag:
                        sqlConnection = sqlite3.connect('databaseFiles/LOGIN.db')
                        cursor = sqlConnection.cursor()
                    elif self.userWindowFlag:
                        sqlConnection = sqlite3.connect('databaseFiles/for_add.db')
                        cursor = sqlConnection.cursor()
                    else:
                        print("HATA!!! db bağlantısı için gerekli ayarlamalar(flagler) eksik yapılmış.")
                    cursor.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM LOGIN WHERE PASSWORD =:password", {"password":password.upper()})
                    record = cursor.fetchall()
                    sqlConnection.close()
                    if len(record) == 0:
                        print("HATA!!! Veri Tabanında böyle bir kullanıcı bulunamadı...")
                        self.statusLabel.setText("KULLANICI BULUNAMADI.\nLÜTFEN TEKRAR OKUTUNUZ")
                        self.statusLabel.repaint()
                    elif len(record) == 1:
                        if self.toolWindowFlag == 1:
                            self.statusLabel.setText("LÜTFEN BEKLEYİNİZ...")
                            self.statusLabel.repaint()
                            app.processEvents()
                            self.openToolWindow()
                            self.toolWindow.activePassword = record[0][3].upper()
                            # self.toolWindowFlag = 0
                        elif self.userWindowFlag == 1:
                            self.userWindow.show()
                            self.userWindowFlag = 0
                            self.toolWindowFlag = 1
                        self.passwordEntry.hide()
                        self.passwordEntry.setFocus(False)
                        self.toolWindow.nameLabel_entry.setText(record[0][0])
                        self.toolWindow.surnameLabel_entry.setText(record[0][1])
                        self.toolWindow.departmanLabel_entry.setText(record[0][2])
                        self.isForLogin = False
                        
                    else:
                        print("Hata: Veri tabanında duplike kayıt bulunmakta!!!")
                elif(len(recorduser) == 0 and len(recordroot) == 0):
                    print("HATA!!! Veri Tabanında böyle bir kullanıcı bulunamadı...")
                    self.statusLabel.setText("KULLANICI BULUNAMADI.\nLÜTFEN TEKRAR OKUTUNUZ")
                    self.statusLabel.repaint()
            except sqlite3.Error as err:
                print("Veri tabanı bağlantısı hatası:", err)
                sqlConnection.close()
            finally:
                self.passwordEntry.clear()

        
        
            # if password == "3DA8ECB9":
            #     photo.sensor.setToolboxOn()
            #     self.openToolWindow()


    def addUser(self):
        self.statusLabel.setText("YETKİLİ KİŞİ GİRİŞİ")
        self.statusLabel.repaint()
        self.userWindowFlag = 1
        self.toolWindowFlag = 0
        self.isForLogin = True
        self.passwordEntry.show()
        self.passwordEntry.setFocus(True)
        self.hideButtons()
        
    
    def dataMigrate(self):
        self.insertSQLiteToPostgre()
        if self.completeFlag:
            self.clearLocalDB()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Veri tabanı aktarımı tamamlandı.")
            msg.setWindowTitle("İşlem Tamamlandı")
            msg.exec_()


    def insertSQLiteToPostgre(self):
        try:
            sqlConnection = sqlite3.connect('databaseFiles/TOOL_TIME.db')
            cursorSqlite = sqlConnection.cursor()
            cursorSqlite.execute("""SELECT * FROM TOOL_TIME""")
            sqLiteData = cursorSqlite.fetchall()
            #print(sqLiteData)
            conn = psycopg2.connect(database="toolboxtakip", user="toctoolbox", password="T*00l@Bax!06", host="pgcons.dmnint.intra", port="54001")
            cursor = conn.cursor()
            cursor.executemany(""" INSERT INTO TOOLTRACK VALUES(nextval('record_sequence'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",sqLiteData)
            
            conn.commit()
            conn.close()
            sqlConnection.commit()
            sqlConnection.close()
            self.completeFlag = True
        except Exception as e:
            self.completeFlag = False
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("OET-TUSAS ağına bağlanamadığı için \nişlem gerçekleştirilemedi lütfen tekrar deneyiniz.")
            msg.setWindowTitle("Bağlantı Hatası")
            msg.exec_()
    

    def clearLocalDB(self):
        try:
            sqlConnection = sqlite3.connect('databaseFiles/TOOL_TIME.db')
            cursor = sqlConnection.cursor()
            cursor.execute("""DELETE FROM TOOL_TIME WHERE 1=1""")
            sqlConnection.commit()
            sqlConnection.close()
            self.completeFlag = False
        except Exception as e:
            print(e)


    def readCard(self):
        self.passwordEntry.setFocus(True)

    
    def readCardForLogin(self):
        self.statusLabel.setText("LÜTFEN KARTINIZI OKUTUN")
        self.statusLabel.repaint()
        self.toolWindowFlag = 1
        self.userWindowFlag = 0
        self.passwordEntry.show()
        self.passwordEntry.setFocus(True)
        self.isForLogin = True
        self.hideButtons()

    
    def showButtons(self):
        self.databaseButton.show()
        self.userButton.show()
        self.loginButton.show()
        self.rebootButton.show()
        self.shutDownButton.show()

    
    def hideButtons(self):
        self.databaseButton.hide()
        self.userButton.hide()
        self.loginButton.hide()
        self.rebootButton.hide()
        self.shutDownButton.hide()


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


    def updateStatus(self):
        pass

    
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

        #os.system("python3 _main.py &")

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

    def rebootSystem(self):
        #self.workerThread.quit()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Sistemi yeniden başlatmak istediğinize emin misiniz?")
        msg.setWindowTitle("Sistemi Yeniden Başlat")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msg.exec_()
        if ret == QMessageBox.Ok:
            os.system("reboot")
        #os.system("sudo pkill -f _main.py")
        #self.close()


    def shutDownSystem(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Sistemi kapatmak istediğinize emin misiniz?")
        msg.setWindowTitle("Sistemi Kapat")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msg.exec_()
        if ret == QMessageBox.Ok:
            os.system("shutdown -h now")


    def addLogo(self):
        self.taiLogo = QLabel()
        self.taiLogo.setPixmap(QtGui.QPixmap("images/tai-logo.png"))
        #self.taiLogo.setGeometry(QtCore.QRect(0, 0, 20, 20))
        self.taiLogo.setScaledContents(True)
        self.taiLogo.setMaximumSize(160,84)
        self.taiLogo.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    
    def displayTime(self):
        current_time = QTime.currentTime()
        label_time = current_time.toString('hh:mm:ss')
        now = QDate.currentDate()
        self.timeLabel.setText(now.toString(Qt.ISODate) + "\n" + label_time)
        self.timeLabel.setAlignment(Qt.AlignRight)
        self.readCard()

    def setButtons(self):
        self.loginButton = QPushButton(self)
        self.loginButton.setIcon(QIcon("images/login-icon.png"))
        self.loginButton.setIconSize(self.buttonSize)
        self.loginButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px")
        self.loginButton.hide()

        # self.settingsButton = QPushButton(self)
        # self.settingsButton.setIcon(QIcon("images/settings-icon.png"))
        # self.settingsButton.setIconSize(self.buttonSize)
        # self.settingsButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px")

        self.rebootButton = QPushButton(self)
        self.rebootButton.setIcon(QIcon("images/close-icon.png"))
        self.rebootButton.setIconSize(self.buttonSize)
        self.rebootButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px;")
        self.rebootButton.hide()

        self.shutDownButton = QPushButton(self)
        self.shutDownButton.setIcon(QIcon("images/shutDown.png"))
        self.shutDownButton.setIconSize(self.buttonSize)
        self.shutDownButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px;")
        self.shutDownButton.hide()
        
        self.userButton = QPushButton(self)
        self.userButton.setIcon(QIcon("images/user-icon.png"))
        self.userButton.setIconSize(self.buttonSize)
        self.userButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px;")
        self.userButton.hide()

        self.databaseButton = QPushButton(self)
        self.databaseButton.setIcon(QIcon("images/database-icon.png"))
        self.databaseButton.setIconSize(self.buttonSize)
        self.databaseButton.setStyleSheet("background-color: rgba(0, 153, 255, 30);border-width: 3px;border-color: #33cc33; border-radius: 25px;")
        self.databaseButton.hide()


    def setStatusLabel(self):
        
        if (self.toolStatus == False):
            self.statusLabel.setText("EKSİK ALET BULUNMAKTADIR. (" + str(self.missingTools) + ")" + "\n GÖRMEK İÇİN GİRİŞ YAPINIZ.")
            self.statusLabel.repaint()
            self.statusLabel.setStyleSheet(self.toolNotExistBackground)
        else:
            self.statusLabel.setText("TÜM ALETLER YERİNDEDİR.")
            self.statusLabel.repaint()
            self.statusLabel.setStyleSheet(self.toolExistsBackground)
        
        
            
        font = self.statusLabel.font()
        
        font.setLetterSpacing(QFont.AbsoluteSpacing, 8)
        #self.statusLabel.setStyleSheet("background-color: rgba(0, 255, 0, 100);")
        self.statusLabel.setAlignment(Qt.AlignCenter)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CustomDialog()
    win.show()
    sys.exit(app.exec_())
