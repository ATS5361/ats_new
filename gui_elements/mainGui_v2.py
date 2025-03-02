"""
Bismillahirrahmanirrahim
"""
# PyQt Lib
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QTime, QDate
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont, QKeySequence
from PyQt5.QtWidgets import *

# built-ins
import time
import os
import sqlite3
import psycopg2
import json
import sys

# Necessary User Packages
import business_logic.detectThread_2 as detectThread
from gui_elements.toolsGui import ToolWindow
from gui_elements.userGui import UserWindow
import business_logic.mainThread as MT
from data_access_layer import dbConnection as dbcon

tool_list_path = "sources/toolList.txt"
photo = MT.TakePhoto() # mainThread dependency

class MainThread(QThread):
    threadSignal = pyqtSignal()
    def run(self):
        while(not photo.terminate):
            photo.endlessLoop()

class CustomDialog(QDialog):
    def __init__(self, parent = None):
        super(CustomDialog, self).__init__(parent)

        # Initial Setup
        self.setWindowTitle("Toolbox Login Panel")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.buttonSize = QSize(160, 160)
        self.setFont((QFont('Roboto', 15)))

        self.toolNotExistBackground = "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e63900, stop: 0.3  #ff531a,stop: 0.8  #ff531a, stop: 1.0  #e63900); font: bold;font-size: 58px;border-style: outset; border-width: 3px;border-color: #e63900; border-radius: 35px; "
        self.toolExistsBackground = "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #85e085, stop: 0.3  #47d147,stop: 0.8  #47d147, stop: 1.0  #70db70); font: bold;font-size: 58px;border-style: outset; border-width: 3px;border-color: #33cc33; border-radius: 35px;"
    
        self.statusLabel = QLabel(self)
        self.toolStatus = False
        self.missingTools = 0
        self.setFixedSize(QtCore.QSize(1365, 745))
        self.setStyleSheet('font-size: 10pt; background-color: #101010')
        self.layout = QGridLayout()
        self.layout.setSpacing(13)
        self.isForLogin = False
        self.setFocusPolicy(Qt.StrongFocus)  # Widget'a fokus ver -özlem

        # Dependency initizalization start !!!!!!!!
        self.toolWindow = ToolWindow() # GUI modülleri birbirine bağlı olabilir, bu nedenle kapatılmadı.
        self.userWindow = UserWindow() # GUI modülleri birbirine bağlı olabilir, bu nedenle kapatılmadı.

#        photo.drawerTrigger.connect(self.toolWindow.updateOpenedDrawer)
#        photo.openedDrawersTrigger.connect(self.toolWindow.updateDrawers)
#        self.toolWindow.detectSignal.connect(self.setOpenedDrawers)
        
        # Components of QDialog
        self.setButtons()
        self.setLastStatus()
        self.setStatusLabel()
        self.addLogo()

        #self.databaseButton.clicked.connect(self.dataMigrate)
        #self.loginButton.clicked.connect(self.readCardForLogin)
        self.rebootButton.clicked.connect(self.rebootSystem)
        self.shutDownButton.clicked.connect(self.shutDownSystem)
        self.userButton.clicked.connect(self.addUser)
        #self.toolWindow.disconnectSignal.connect(self.disconnectSensor)
        #self.toolWindow.updateStatusSignal.connect(self.updateStatus)
        
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

        # Add Widgets
        self.layout.addWidget(self.taiLogo, 0, 0, 1, 0)
        self.layout.addWidget(self.timeLabel, 0, 3)
        self.layout.addWidget(self.statusLabel,1, 0, 2, 5)
        self.layout.addWidget(self.databaseButton, 3, 0)
        self.layout.addWidget(self.loginButton, 3, 2)
        self.layout.addWidget(self.userButton, 3, 1)
        self.layout.addWidget(self.rebootButton, 3, 3)
        self.layout.addWidget(self.shutDownButton, 3, 4)
        
        # Add Timer Attributes
        self.timeLabel.setStyleSheet("font-size: 15pt; color: white")
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.displayTime)
        self.timer.start()

        self.debugTimer = QtCore.QTimer(self)
        self.debugTimer.setInterval(100)
#        self.debugTimer.timeout.connect(self.debugCam)
        self.debugTimer.start()
        #self.layout.setRowStretch(2, 0)
        self.passwordEntry = QLineEdit(self)
        self.passwordEntry.setFixedWidth(0)
        self.passwordEntry.move(100, 100)
#        self.passwordEntry.textChanged.connect(self.passCheck)
        self.passwordEntry.hide()

        # ! Dependency of detectThread for running the loop function
        self.setLayout(self.layout)
        self.readCard()
#        detectThread.runMain()
        
#    def setOpenedDrawers(self):
#        detectThread.changeDrawerList(photo.openedDrawerList) ### DEP

    # key pressed event addition -özlem
    def keyPressEvent(self, event):
        """
            Enables users to pass between the Login UI And Tool Window.
            event.key() == Qt.Key_Escape: Click esc to shut down the system.
            event.key() == Qt.Key_Space: CLick space key to pass to the ToolWindow widget instance.
        """
        print(f"Key pressed: {event.key()}")
        if event.key() == Qt.Key_Escape:
            print("ESC tıklandı. Uygulama kapanıyor...")
            QApplication.instance().quit()

        elif event.key() == Qt.Key_Space:
            print("Space tuşuna basıldı!")
            self.hide()
            self.toolWindow.show()
            self.toolWindow.setFocus()  # ToolWindow'a odaklanır
            event.accept()

    def setLastStatus(self):
        with open(tool_list_path, "r") as dosya:
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

    def addUser(self):
        self.statusLabel.setText("YETKİLİ KİŞİ GİRİŞİ")
        self.statusLabel.repaint()
        self.userWindowFlag = 1
        self.toolWindowFlag = 0
        self.isForLogin = True
        self.passwordEntry.show()
        self.passwordEntry.setFocus(True)
        self.hideButtons() # readCardForLogin ile aynı işi yapıyor -özlem

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
        self.hideButtons() # addUser ile aynı işi yapıyor -özlem

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

    def updateStatus(self):
        pass

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
            self.statusLabel.setText(f"{str(self.missingTools)} EKSİK ALET BULUNMAKTADIR. \n GÖRMEK İÇİN GİRİŞ YAPINIZ.")
            self.statusLabel.repaint()
            self.statusLabel.setStyleSheet(self.toolNotExistBackground)
        else:
            self.statusLabel.setText("TÜM ALETLER YERİNDEDİR.")
            self.statusLabel.repaint()
            self.statusLabel.setStyleSheet(self.toolExistsBackground)
        
        font = self.statusLabel.font()
        
        font.setLetterSpacing(QFont.AbsoluteSpacing, 8)
        self.statusLabel.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CustomDialog()
    win.show()
    sys.exit(app.exec_())