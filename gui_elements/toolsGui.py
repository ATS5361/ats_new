# PyQt Libs
from PyQt5.QtCore import Qt, QSize, QDateTime, QSettings, QThread, pyqtSignal, QPropertyAnimation, QRect, QTimer
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter, QPixmap
from PyQt5.QtWidgets import *

# built-ins
from datetime import date, datetime
from functools import partial
import sqlite3
import time
import sys

# user packages
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sources.ToolCordinates import Coordinates

# Class for Picture Making
class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

# Main Tool Window 
class ToolWindow(QDialog):
    detectSignal = pyqtSignal()
    disconnectSignal = pyqtSignal()
    updateStatusSignal = pyqtSignal()
    """Main Window."""
    def __init__(self, parent=None):
        super(ToolWindow, self).__init__(parent)
        self.setFixedSize(QtCore.QSize(1365, 745))
        self.autoCloseTimer = QTimer()
        self.autoCloseTimer.setInterval(30000)
        self.autoCloseTimer.timeout.connect(self.closeWindow)

        self.setFont((QFont('Roboto', 15)))
        self.coord = Coordinates()
        self.arrSize = 34  #91
    
        self.COORD_1 = self.coord.COORD_1
        self.COORD_2 = self.coord.COORD_2
        self.COORD_3 = self.coord.COORD_3
        self.COORD_4 = self.coord.COORD_4
        self.COORD_5 = self.coord.COORD_5

        self.timerFlag = 0
        self.drawerImgFile = "drawer-image-"
        self.animationTimer=QTimer()
        self.animationTimer.timeout.connect(partial(self.changeColor))
        self.scale = 2.5
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.clickStatus = [0]*6
        self.toolButtons = []
        self.toolLabels = []

        self.frames_1 = []
        self.frames_2 = []
        self.frames_3 = []
        self.frames_4 = []
        self.frames_5 = []
        self.frames_6 = []

        self.openedDrawersList = []
        self.lastStatusOfTools_1 = [0] * len(self.coord.COORD_1_NumOfTools_LiveAll)
        self.lastStatusOfTools_2 = [0] * len(self.coord.COORD_2_NumOfTools_LiveAll)
        self.lastStatusOfTools_3 = [0] * len(self.coord.COORD_3_NumOfTools_LiveAll)
        self.lastStatusOfTools_4 = [0] * len(self.coord.COORD_4_NumOfTools_LiveAll)
        self.lastStatusOfTools_5 = [0] * len(self.coord.COORD_5_NumOfTools_Live)
        self.lastStatusOfTools_6 = [0] * len(self.coord.COORD_6_NumOfTools_LiveAll)
        self.lastStatusOfDrawers = [self.lastStatusOfTools_1, 
                                  self.lastStatusOfTools_2,
                                  self.lastStatusOfTools_3,
                                  self.lastStatusOfTools_4,
                                  self.lastStatusOfTools_5,
                                  self.lastStatusOfTools_6]

        self.openedDrawer = -1
        self.activePassword = 0
        self.isBusyFlag = False

        self.eksikCekmece = []

        self.toolsTaken = []
        self.toolsGiven = []

        self.setStyleSheet('font-size: 10pt; background-color: #101010')
        self.createLayout()
        self.setLayout(self.layout)
        #self.toolLabels[0].setText("1")
        self.animationTimer.start(500)
        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon("images/close-icon-old.png"))
        self.closeButton.setStyleSheet("background-color: transparent")
        self.closeButton.setIconSize(QSize(30, 30))
        self.closeButton.move(1290, 5)
        self.closeButton.clicked.connect(self.closeWindow)

        # self.detectButton = QPushButton(self)
        # self.detectButton.setMinimumSize(100, 100)
        # self.detectButton.setText("DETECT")
        # self.detectButton.move(1290, 25)
        # self.detectButton.clicked.connect(self.triggerDetectSignal)
        #self.userImg.clicked.connect(self.focusPassword)

        self.passwordEntry = QLineEdit(self)
        self.passwordEntry.setFixedWidth(0)
        self.passwordEntry.move(100, 100)
        self.passwordEntry.textChanged.connect(self.passCheck)
        self.passwordEntry.hide()

        self.drawerIsOpen = False

        newFile = ['0\n', '0\n', '0\n', '0\n', '0\n', '0\n']
        with open("detectionFinishCheck.txt", "w") as dosya:
             dosya.writelines(newFile)

        newFile = ['0\n', '0\n', '0\n', '0\n', '0\n', '0\n']
        with open("detectionFinishCheck.txt", "w") as dosya:
             dosya.writelines(newFile)

    def passCheck(self):
        password = self.passwordEntry.text()
        if len(password) == 8:
            if password.upper() == self.activePassword:
                self.passwordEntry.setFocus(False)
                self.triggerDetectSignal()
                self.passwordEntry.setFocus(True)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Kart ID yanlış.\nLütfen giriş yaptığınız kartı okutun.")
                msg.setWindowTitle("Eksik alet tespiti")
                msg.exec_()
                self.passwordEntry.show()
                self.passwordEntry.setFocus(True)

            self.passwordEntry.clear()

    def focusPassword(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Eksik aletleri tespit etmek için lütfen pencereyi kapatın ve kartınızı okutun")
        msg.setWindowTitle("Eksik alet tespiti")
        msg.exec_()
        self.passwordEntry.show()
        self.passwordEntry.setFocus(True)
    
    def drawLastStatus(self):
      
        for i in range(len(self.coord.COORD_1_NumOfTools_LiveAll)):
            if self.lastStatusOfDrawers[0][i] == 0:
                
                (x, y) = (self.COORD_1[i][0], self.COORD_1[i][1])
                (w, h) = (self.COORD_1[i][2], self.COORD_1[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_1.append(frame)

        for i in range(len(self.coord.COORD_2_NumOfTools_LiveAll)):
            if self.lastStatusOfDrawers[1][i] == 0:
                
                (x, y) = (self.COORD_2[i][0], self.COORD_2[i][1])
                (w, h) = (self.COORD_2[i][2], self.COORD_2[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_2.append(frame)

        for i in range(len(self.coord.COORD_3_NumOfTools_LiveAll)):
            if self.lastStatusOfDrawers[2][i] == 0:
                
                (x, y) = (self.COORD_3[i][0], self.COORD_3[i][1])
                (w, h) = (self.COORD_3[i][2], self.COORD_3[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_3.append(frame)
        
        for i in range(len(self.coord.COORD_4_NumOfTools_LiveAll)):
            if self.lastStatusOfDrawers[3][i] == 0:
                
                (x, y) = (self.COORD_4[i][0], self.COORD_4[i][1])
                (w, h) = (self.COORD_4[i][2], self.COORD_4[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_4.append(frame)
        
        for i in range(len(self.coord.COORD_5_NumOfTools_Live)):
            if self.lastStatusOfDrawers[4][i] == 0:
                
                (x, y) = (self.COORD_5[i][0], self.COORD_5[i][1])
                (w, h) = (self.COORD_5[i][2], self.COORD_5[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_5.append(frame)

        for i in range(len(self.coord.COORD_6_NumOfTools_LiveAll)):
            if self.lastStatusOfDrawers[5][i] == 0:
                
                (x, y) = (self.coord.COORD_6[i][0], self.coord.COORD_6[i][1])
                (w, h) = (self.coord.COORD_6[i][2], self.coord.COORD_6[i][3])

                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_6.append(frame)

    def writeToolsToDB(self):
        try:
            sqlConnection = sqlite3.connect('databaseFiles/TOOL_TIME.db')
            cursor = sqlConnection.cursor()
            tempDate = QDateTime.currentDateTime()
            if len(self.toolsTaken) > 0:
                insert_data_taken = (self.nameLabel_entry.text().upper(), self.surnameLabel_entry.text().upper(), self.departmanLabel_entry.text().upper(), str(self.toolsTaken), 0, 0, "", tempDate.toString(), 0, "Taken")
                cursor.execute('''INSERT INTO TOOL_TIME (USERNAME, LASTNAME, DEPARTMENT, ALET, I1, I2, S1, DATE, I3, ISTAKEN)
                 VALUES(?,?,?,?,?,?,?,?,?,?);''', insert_data_taken)
                sqlConnection.commit()
            if len(self.toolsGiven) > 0:
                insert_data_given = (self.nameLabel_entry.text().upper(), self.surnameLabel_entry.text().upper(), self.departmanLabel_entry.text().upper(), str(self.toolsGiven), 0, 0, "", tempDate.toString(), 0, "Given")
                cursor.execute('''INSERT INTO TOOL_TIME (USERNAME, LASTNAME, DEPARTMENT, ALET, I1, I2, S1, DATE, I3, ISTAKEN)
                VALUES(?,?,?,?,?,?,?,?,?,?);''', insert_data_given)
                sqlConnection.commit()
        except sqlite3.Error as err:
            print("Veri tabanı bağlantısı hatası:", err)
        finally:
            if sqlConnection:
                sqlConnection.close()

    def triggerDetectSignal(self):
        if not self.isBusyFlag:
            self.isBusyFlag = True
            self.autoCloseTimer.start()
            self.detectSignal.emit()
            time.sleep(0.1)
            while(1):
                time.sleep(0.02)
                with open("detectionFinishCheck.txt", "r") as dosya: 
                    newFile = dosya.readlines()
                    rFlag = True

                    print(self.openedDrawersList)
                    print(newFile)
                    for i in range(len(self.openedDrawersList)):
                        try:
                            if newFile[self.openedDrawersList[i] - 1] == '1\n':
                                rFlag = rFlag and True
                            else:
                                rFlag = rFlag and False
                        except IndexError as e:
                            rFlag = False
                            print(e)
                            pass
                    print(rFlag)
                
                if rFlag == True:
                    print("İşlem tamam")
                    break
                        
            newFile = ['0\n', '0\n', '0\n', '0\n', '0\n', '0\n']
            with open("detectionFinishCheck.txt", "w") as dosya:
                dosya.writelines(newFile)
                
            self.toolsTaken = []
            self.toolsGiven = []
            self.clearTextBox()
            for drawer in self.openedDrawersList:
                if drawer == 1:
                    self.readToolsFromFile_1()
                if drawer == 2:
                    self.readToolsFromFile_2()
                elif drawer == 3:
                    self.readToolsFromFile_3()
                elif drawer == 4:
                    self.readToolsFromFile_4()
                elif drawer == 5:
                    self.readToolsFromFile_5()
                elif drawer == 6:
                    self.readToolsFromFile_6()
            
            self.addNewLine(self.toolsTaken, 0)
            self.addNewLine(self.toolsGiven, 1)
            self.saveLastStatus()
            self.writeToolsToDB()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Tool Tespiti Tamamlandı")
            msg.setWindowTitle("Tool Tespiti")
            QTimer.singleShot(2000, lambda: msg.done(0))
            msg.exec_()
            self.isBusyFlag = False

    def closeWindow(self):
        if self.drawerIsOpen == False:
            self.autoCloseTimer.stop()
            self.disconnectSignal.emit()
            self.close()
            self.updateStatusSignal.emit()
        else:
            print("Cekmece Açık")
        
    def saveLastStatus(self):
        tempStr = ""
        for i in range(6):
            #tempLine= json.dumps(self.lastStatusOfDrawers[i])
            tempStr += str(self.lastStatusOfDrawers[i]) + "\n"

        with open("toolList.txt", "w") as dosya:
            dosya.write(tempStr)

    def createLayout(self):
        self.layout = QGridLayout()
        self.layout.setSpacing(5)
        self.createToolImages()
        self.createLabels()
        self.createWidget()
        self.createUserImage()
        
        self.layout.addWidget(self.toolButtons[0], 0, 0)
        self.layout.addWidget(self.toolButtons[1], 0, 1)
        self.layout.addWidget(self.toolButtons[2], 0, 2)
        self.layout.addWidget(self.toolButtons[3], 2, 0)
        self.layout.addWidget(self.toolButtons[4], 2, 1)
        self.layout.addWidget(self.toolButtons[5], 2, 2)

        self.layout.addWidget(self.toolLabels[0], 1, 0)
        self.layout.addWidget(self.toolLabels[1], 1, 1)
        self.layout.addWidget(self.toolLabels[2], 1, 2)
        self.layout.addWidget(self.toolLabels[3], 3, 0)
        self.layout.addWidget(self.toolLabels[4], 3, 1)
        self.layout.addWidget(self.toolLabels[5], 3, 2)
        
        self.layout.addWidget(self.emptyWidget, 0, 4, 4, 4)
        #self.layout.addWidget(self.toolButtons[0], 4,0)
        self.layout.setContentsMargins(12,15,12,15)
        #self.toolButtons[2].setVisible(False)
        self.createQVLayout()
        self.emptyWidget.setLayout(self.vLayout)

        self.connectButtons()
        self.colorAnimation(0)

    def createBackButton(self):
        self.backButton = QPushButton(self)
        self.backButton.setIcon(QIcon("images/back-icon.png"))
        self.backButton.setIconSize(QSize(30,30))
        self.backButton.setStyleSheet("background-color: rgba(255, 255, 255, 0)")

    def createUserImage(self):
        self.userImg = QPushButton(self)
        self.userImg.setIcon(QIcon("images/mechanic-icon.png"))
        self.userImg.setStyleSheet("background-color: transparent; border: 0px")
        self.userImg.setIconSize(QSize(130,130))
    
    def createQVLayout(self):
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.userImg)
        #self.userImg.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.vLayout.setContentsMargins(10,10,10,10)
        self.groupBox = QGroupBox()
        self.groupBox.setStyleSheet("color: #E8E8E8; font-weight: bold; padding: 4px; background-color:rgba(0, 153, 255, 15);")
        
        # self.groupBox.setCheckable(True)
        self.vLayout.addWidget(self.groupBox)

        gridBox = QGridLayout()

        self.nameLabel = QLabel("İsim:")
        self.surnameLabel = QLabel("Soyisim: ")
        self.departmanLabel = QLabel("Departman: ")
        #self.sicilLabel = QLabel("Sicil: ")

        self.nameLabel_entry = QLabel("Alperen")
        self.surnameLabel_entry = QLabel("Kopuz")
        self.departmanLabel_entry = QLabel("Yazılım")
        #self.sicilLabel_entry = QLabel("228558")

        self.groupBox.setLayout(gridBox)

        gridBox.addWidget(self.nameLabel, 0, 0)
        gridBox.addWidget(self.surnameLabel, 1, 0)
        gridBox.addWidget(self.departmanLabel, 2, 0)
        #gridBox.addWidget(self.sicilLabel, 3, 0)

        gridBox.addWidget(self.nameLabel_entry, 0, 1)
        gridBox.addWidget(self.surnameLabel_entry, 1, 1)
        gridBox.addWidget(self.departmanLabel_entry, 2, 1)
        #gridBox.addWidget(self.sicilLabel_entry, 3, 1)

        self.nameLabel_entry.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.surnameLabel_entry.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.departmanLabel_entry.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        #self.sicilLabel_entry.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        
        self.nameLabel.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.surnameLabel.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.departmanLabel.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        #self.sicilLabel.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
                
        self.alinanToolLabel = QLabel("ALINAN ALETLER")
        self.alinanToolLabel.setStyleSheet("color: #E8E8E8; font-weight: bold; padding: 6px")
        self.vLayout.addWidget(self.alinanToolLabel)
        self.toolTable1 = QTextEdit()
        self.toolTable1.setReadOnly(True)
        self.toolTable1.setStyleSheet("background-color: rgba(0, 153, 255, 15); color: #E8E8E8; font-weight: bold; padding: 6px")

        self.vLayout.addWidget(self.toolTable1)

        self.verilenToolLabel = QLabel("İADE EDİLEN ALETLER")
        self.verilenToolLabel.setStyleSheet("color: #E8E8E8; font-weight: bold; padding: 6px")
        self.vLayout.addWidget(self.verilenToolLabel)

        self.toolTable = QTextEdit()
        self.toolTable.setReadOnly(True)
        self.toolTable.setStyleSheet("background-color: rgba(0, 153, 255, 15); color: #E8E8E8; font-weight: bold; padding: 6px")
        self.vLayout.addWidget(self.toolTable)
        #self.setMouseTracking(True)

    def addNewLine(self, strList, index):
        if index == 0:
            for str in strList:
                self.toolTable1.append("• " + str)
        elif index == 1:
            for str in strList:
                self.toolTable.append("• " + str)

    """
    def mouseMoveEvent(self, event):
        print('Mouse coords: ( %d : %d )' % (event.x(), event.y()))
    """

    def clearTextBox(self):
        self.toolTable.clear()
        self.toolTable1.clear()

    def createToolImages(self):
        for i in range(6):
            
            tempFileName = "images/" + self.drawerImgFile + str(i + 1) + ".jpeg"
            tempButton = PicButton(QPixmap(tempFileName), self)
            #tempButton = QPushButton(self)
            
            #tempButton.setIcon(QIcon(tempFileName))
            ##tempButton.setIconSize(QSize(30,30))
            
            tempButton.setMinimumWidth(356)
            tempButton.setMinimumHeight(292)
            self.buttonWidth = tempButton.width() 
            self.buttonHeight = tempButton.height()

            tempButton.setIconSize(QSize(self.buttonWidth,self.buttonHeight))
            tempButton.setStyleSheet("background-color: rgba(255, 255, 255, 0); ")

            self.toolButtons.append(tempButton)

    def showFrames(self, index):
        frames = []
        if index == 2:
            frames = self.frames_3
        elif index == 4:
            frames = self.frames_5
        elif index == 3:
            frames = self.frames_4
        elif index == 1:
            frames = self.frames_2
        elif index == 0:
            frames = self.frames_1
        elif index == 5:
            frames = self.frames_6

        for i in range(len(frames)):
            frames[i].show()
    
    def hideFrames(self, index):
        frames = []
        if index == 2:
            frames = self.frames_3
        elif index == 4:
            frames = self.frames_5
        elif index == 3:
            frames = self.frames_4
        elif index == 1:
            frames = self.frames_2
        elif index == 0:
            frames = self.frames_1
        elif index == 5:
            frames = self.frames_6

        for i in range(len(frames)):
            frames[i].hide()

    def connectButtons(self):
        for i in range(6):
            self.toolButtons[i].clicked.connect(partial(self.resizeToolImage, i))            
            
    def createLabels(self):
        for i in range(6):
            self.tempLabel = QLabel(self)
            self.tempLabel.setText("0")
            self.tempLabel.setStyleSheet("font-size: 25pt; color: white; font-weight: bold; background-color: rgba(0, 153, 255, 80);border-width: 3px;")
            self.tempLabel.setAlignment(Qt.AlignCenter)
            self.toolLabels.append(self.tempLabel)

    def createWidget(self):
        self.emptyWidget = QWidget(self)
        self.emptyWidget.setFixedWidth(260)
        self.emptyWidget.setStyleSheet("background-color: #101010")
        
    def resizeToolImage(self, index):
            
            tempButton = self.toolButtons[index]

            if self.clickStatus[index] == 0:
                self.setVisibleLayout(False, index)
                w = self.buttonWidth * self.scale
                h = self.buttonHeight * self.scale
                self.showFrames(index)
                tempButton.setMinimumWidth(1000)
                self.clickStatus[index] = 1

            else:
                self.setVisibleLayout(True, index)
                w = self.buttonWidth
                h = self.buttonHeight
                tempButton.setMinimumWidth(343)
                self.hideFrames(index)
                self.clickStatus[index] = 0
            
            
            tempButton.setIconSize(QSize(w,h))
            #tempButton.setIconSize(QSize(w,h))
            self.passwordEntry.show()
            self.passwordEntry.setFocus(True)
            
    def setVisibleLayout(self, bool, index):
        for i in range(6):
            if i != index:
                self.toolButtons[i].setVisible(bool)
                self.toolLabels[i].setVisible(bool)

    def updateOpenedDrawer(self, drawerNum):
        self.autoCloseTimer.start()
        self.openedDrawer = drawerNum - 1
        for i in range(6):
            self.toolLabels[i].setStyleSheet("font-size: 25pt; color: white; font-weight: bold; background-color: rgba(0, 153, 255, 80);border-width: 3px;")
          # print("Opened Drawer: ",self.openedDrawer)
        if (not self.openedDrawer == -1) and self.openedDrawer != 99:
            self.drawerIsOpen = True
            self.toolLabels[self.openedDrawer].setStyleSheet("font-size: 25pt; color: white; font-weight: bold; background-color: rgba(0, 255, 247, 90);border-width: 3px;")
        else:
            self.drawerIsOpen = False
            
    def updateDrawers(self, list):
        self.openedDrawersList = list

    def changeColor(self):
        pass
        # if not self.openedDrawer == -1:
        # for tool in self.eksikCekmece:
        #     if self.timerFlag == 0:
        #         tool.setStyleSheet("font-size: 25pt; color: white; font-weight: bold; background-color: #FF6666; border-width: 3px;")
        #         #self.toolButtons[i].setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        #         self.timerFlag = 1
        #     else:
        #         tool.setStyleSheet("font-size: 25pt; color: white; font-weight: bold; background-color: rgba(0, 153, 255, 80);border-width: 3px;")
        #         #self.toolButtons[i].setStyleSheet("background-color: rgba(255, 255, 255, 0);" )
        #         self.timerFlag = 0

    def readToolsFromFile_1(self):
        toolsArr = []
        self.hideFrames(0)
        for temp in self.frames_1:
            temp.deleteLater()
        self.frames_1 = []
        try:
            with open("runs/detect/exp/labels/al_camera0367_foto_0_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "5" or ilk_eleman == "6":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)
        
        try:
            with open("runs/detect/exp/labels/al_camera0367_foto_1_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "3" or ilk_eleman == "4":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp/labels/al_camera0367_foto_2_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0" or ilk_eleman == "1" or ilk_eleman == "2":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp2/labels/al_camera0367_foto_0_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "6" or ilk_eleman == "7":
                        temp = int(ilk_eleman) + 7
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp2/labels/al_camera0367_foto_1_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "3" or ilk_eleman == "4" or ilk_eleman == "5":
                        temp = int(ilk_eleman) + 7
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp2/labels/al_camera0367_foto_2_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0" or ilk_eleman == "1" or ilk_eleman == "2":
                        temp = int(ilk_eleman) + 7
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)

        for i in range(3):
            try:
                path = "runs/detect/exp/labels/al_camera0367_foto_" + str(i) + "_1.txt"
                with open(path, "w") as dosya:
                    dosya.write("")
            except FileNotFoundError as err:
                print(err)
            
        for i in range(3):
            try:
                path = "runs/detect/exp2/labels/al_camera0367_foto_" + str(i) + "_2.txt"
                with open(path, "w") as dosya:
                    dosya.write("")
            except FileNotFoundError as err:
                print(err)

        self.coord.COORD_1_NumOfTools_Live = [0]*len(self.coord.COORD_1_NumOfTools)
        self.coord.COORD_1_NumOfTools_LiveAll = [0]*len(self.coord.COORD_1_NumOfTools_LiveAll)
        
        for i in range(len(toolsArr)):
             self.coord.COORD_1_NumOfTools_Live[int(toolsArr[i])] += 1
                    
        total_dif = 0
        counter = 0
        for i in range(len(self.coord.COORD_1_NumOfTools)):
            if int(self.coord.COORD_1_NumOfTools_Live[i]) > int(self.coord.COORD_1_NumOfTools[i]):
                self.coord.COORD_1_NumOfTools_Live[i] = self.coord.COORD_1_NumOfTools[i]
            temp = int(self.coord.COORD_1_NumOfTools[i]) - int(self.coord.COORD_1_NumOfTools_Live[i])
            total_dif += temp
            temp = int(self.coord.COORD_1_NumOfTools_Live[i])
            if temp < 0:
                temp = 0
            for j in range(temp):
                self.coord.COORD_1_NumOfTools_LiveAll[counter + j] = 1
            counter += self.coord.COORD_1_NumOfTools[i]

        for i in range(len(self.coord.COORD_1_NumOfTools_LiveAll)):
            if self.coord.COORD_1_NumOfTools_LiveAll[i] == 0:
                
                (x, y) = (self.COORD_1[i][0], self.COORD_1[i][1])
                (w, h) = (self.COORD_1[i][2], self.COORD_1[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_1.append(frame) 

        for i in range(len(self.coord.COORD_1_NumOfTools_LiveAll)):
            if (int(self.lastStatusOfDrawers[0][i]) < int(self.coord.COORD_1_NumOfTools_LiveAll[i])): 
                self.toolsGiven.append(self.coord.COORD_1_ToolNames[i])

            elif (int(self.lastStatusOfDrawers[0][i]) > int(self.coord.COORD_1_NumOfTools_LiveAll[i])):
                self.toolsTaken.append(self.coord.COORD_1_ToolNames[i])

        self.lastStatusOfDrawers[0] = self.coord.COORD_1_NumOfTools_LiveAll

        # for i in range(len(self.coord.COORD_1_NumOfTools)):
        #     temp = int(self.coord.COORD_1_NumOfTools[i]) - int(self.coord.COORD_1_NumOfTools_Live[i])
        #     total_dif += temp
        #     if(not temp == 0):
        #         counter = temp
        #         for j in range(temp):
        #             self.toolsTaken.append("Tool " + str(i) + "- Drawer 1")
        #             for z in range(len(self.coord.COORD_1_Groups)):
        #                 if self.coord.COORD_1_Groups[z] == i and counter > 0:
        #                     (x, y) = (self.COORD_1[z][0], self.COORD_1[z][1])
        #                     (w, h) = (self.COORD_1[z][2], self.COORD_1[z][3])
        #                     frame = QFrame(self)
        #                     frame.setGeometry(QtCore.QRect(x, y, w, h))
        #                     frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
        #                     frame.hide()
        #                     self.frames_1.append(frame)  
        #                     counter -= 1   

        self.toolLabels[0].setText(str(total_dif))
        if self.clickStatus[0] == 1:
            self.showFrames(0)

    def readToolsFromFile_4(self):
        toolsArr = []
        self.hideFrames(3)
        for temp in self.frames_4:
            temp.deleteLater()
        self.frames_4 = []
        try:
            with open("runs/detect/exp7/labels/al_camera0367_foto_0_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "4" or ilk_eleman == "5" or ilk_eleman == "6" or ilk_eleman == "7" or ilk_eleman == "8" or ilk_eleman == "9":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp7/labels/al_camera0367_foto_1_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "3":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp7/labels/al_camera0367_foto_2_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0" or ilk_eleman == "1" or ilk_eleman == "2":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        for i in range(3):
            try:
                path = "runs/detect/exp7/labels/al_camera0367_foto_" + str(i) + "_2.txt"
                with open(path, "w") as dosya:
                    dosya.write("")
            except FileNotFoundError as err:
                print(err)

        self.coord.COORD_4_NumOfTools_Live = [0]*len(self.coord.COORD_4_NumOfTools)
        self.coord.COORD_4_NumOfTools_LiveAll = [0]*12

        for i in range(len(toolsArr)):
             self.coord.COORD_4_NumOfTools_Live[int(toolsArr[i])] += 1
                    
        total_dif = 0
        counter = 0
        for i in range(len(self.coord.COORD_4_NumOfTools)):
            if int(self.coord.COORD_4_NumOfTools_Live[i]) > int(self.coord.COORD_4_NumOfTools[i]):
                self.coord.COORD_4_NumOfTools_Live[i] = self.coord.COORD_4_NumOfTools[i]
            temp = int(self.coord.COORD_4_NumOfTools[i]) - int(self.coord.COORD_4_NumOfTools_Live[i])
            print(temp)
            total_dif += temp
            temp = int(self.coord.COORD_4_NumOfTools_Live[i])
            if temp < 0:
                temp = 0
            for j in range(temp):
                self.coord.COORD_4_NumOfTools_LiveAll[counter + j] = 1
            counter += self.coord.COORD_4_NumOfTools[i]

        print(self.coord.COORD_4_NumOfTools_LiveAll)

        for i in range(len(self.coord.COORD_4_NumOfTools_LiveAll)):
            if self.coord.COORD_4_NumOfTools_LiveAll[i] == 0:
                
                (x, y) = (self.COORD_4[i][0], self.COORD_4[i][1])
                (w, h) = (self.COORD_4[i][2], self.COORD_4[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_4.append(frame) 

        for i in range(len(self.coord.COORD_4_NumOfTools_LiveAll)):
            if (int(self.lastStatusOfDrawers[3][i]) < int(self.coord.COORD_4_NumOfTools_LiveAll[i])): 
                self.toolsGiven.append(self.coord.COORD_4_ToolNames[i])

            elif (int(self.lastStatusOfDrawers[3][i]) > int(self.coord.COORD_4_NumOfTools_LiveAll[i])):
                self.toolsTaken.append(self.coord.COORD_4_ToolNames[i])

        self.lastStatusOfDrawers[3] = self.coord.COORD_4_NumOfTools_LiveAll

        self.toolLabels[3].setText(str(total_dif))
        if self.clickStatus[3] == 1:
            self.showFrames(3)

    def readToolsFromFile_3(self):

        toolsArr = []
        for temp in self.frames_3:
            temp.deleteLater()
        self.hideFrames(2)
        self.frames_3 = []
    
        try:
            with open("runs/detect/exp5/labels/al_camera0367_foto_0_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "1" or ilk_eleman == "2":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp5/labels/al_camera0367_foto_1_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp6/labels/al_camera0367_foto_0_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "5" or ilk_eleman == "6":
                        temp = int(ilk_eleman) + 3
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp6/labels/al_camera0367_foto_1_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "3" or ilk_eleman == "4":
                        temp = int(ilk_eleman) + 3
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp6/labels/al_camera0367_foto_2_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0" or ilk_eleman == "1" or ilk_eleman == "2":
                        temp = int(ilk_eleman) + 3
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)

        self.coord.COORD_3_NumOfTools_Live = [0]*len(self.coord.COORD_3_NumOfTools)
        self.coord.COORD_3_NumOfTools_LiveAll = [0]*len(self.coord.COORD_3_NumOfTools_LiveAll)
        
        total_dif = 0
        counter = 0
        for i in range(len(toolsArr)):
            self.coord.COORD_3_NumOfTools_Live[int(toolsArr[i])] += 1
            
        for i in range(len(self.coord.COORD_3_NumOfTools)):
            if int(self.coord.COORD_3_NumOfTools_Live[i]) > int(self.coord.COORD_3_NumOfTools[i]):
                self.coord.COORD_3_NumOfTools_Live[i] = self.coord.COORD_3_NumOfTools[i]

            temp = int(self.coord.COORD_3_NumOfTools[i]) - int(self.coord.COORD_3_NumOfTools_Live[i])
            total_dif += temp

            temp = int(self.coord.COORD_3_NumOfTools_Live[i])
            for j in range(temp):
                self.coord.COORD_3_NumOfTools_LiveAll[counter + j] = 1
            counter += self.coord.COORD_3_NumOfTools[i]

        cnt = 0
        width = 473
        try:
            with open("runs/detect/exp5/labels/al_camera0367_foto_1_1.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_3_Predefined_1:

                    for line in lines:
                        result = self.coord.splitLine(line, tool_id, width)
                        if result == True:
                            break
                        
                    self.coord.COORD_3_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_3_Predefined_1)
            print(err)

        width = 665
        cnt += 2
        try:
            with open("runs/detect/exp6/labels/al_camera0367_foto_2_2.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_3_Predefined_2:

                    for line in lines:
                        result = self.coord.splitLine(line, tool_id, width)
                        if result == True:
                            break

                    self.coord.COORD_3_NumOfTools_LiveAll[cnt] = result  
                    cnt += 1
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_3_Predefined_2)
            print(err)

        for i in range(len(self.coord.COORD_3_NumOfTools_LiveAll)):
            if self.coord.COORD_3_NumOfTools_LiveAll[i] == 0:
                (x, y) = (self.COORD_3[i][0], self.COORD_3[i][1])
                (w, h) = (self.COORD_3[i][2], self.COORD_3[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_3.append(frame) 

        for i in range(len(self.coord.COORD_3_NumOfTools_LiveAll)):
            if (int(self.lastStatusOfDrawers[2][i]) < int(self.coord.COORD_3_NumOfTools_LiveAll[i])): 
                self.toolsGiven.append(self.coord.COORD_3_ToolNames[i])

            elif (int(self.lastStatusOfDrawers[2][i]) > int(self.coord.COORD_3_NumOfTools_LiveAll[i])):
                self.toolsTaken.append(self.coord.COORD_3_ToolNames[i])

        self.lastStatusOfDrawers[2] = self.coord.COORD_3_NumOfTools_LiveAll

        self.toolLabels[2].setText(str(total_dif))

        for i in range(2):
            try:
                path = "runs/detect/exp5/labels/al_camera0367_foto_" + str(i) + "_1.txt"
                with open(path, "w") as dosya:
                    dosya.write("")
            except FileNotFoundError as err:
                print(err)

        for i in range(3):
            try:
                path = "runs/detect/exp6/labels/al_camera0367_foto_" + str(i) + "_2.txt"
                with open(path, "w") as dosya:
                    dosya.write("")
            except FileNotFoundError as err:
                print(err)

        if self.clickStatus[2] == 1:
            self.showFrames(2)

    def readToolsFromFile_5(self):
        self.hideFrames(4)
        self.frames_5 = []
        width = 760
        cnt = 0
        total_dif = 0
        
        self.coord.COORD_5_NumOfTools_Live = [0]*len(self.coord.COORD_5_NumOfTools)

        try:
            with open("runs/detect/exp8/labels/al_camera0367_foto_1_2.txt", 'r') as dosya:
                lines = dosya.readlines()
                
                for tool_id in self.coord.COORD_5_Predefined_2:

                    for line in lines:
                        result = self.coord.splitLine(line, tool_id, width)
                        if result == True:
                            break

                    if result:
                        self.coord.COORD_5_NumOfTools_Live[cnt] = 1
                    else:
                        self.coord.COORD_5_NumOfTools_Live[cnt] = 0
                        total_dif += 1

                    cnt += 1

        except FileNotFoundError as err:
            total_dif += len(self.coord.COORD_5_Predefined_2)
            cnt += len(self.coord.COORD_5_Predefined_2)
            print(err)

        try:
            with open("runs/detect/exp8/labels/al_camera0367_foto_0_2.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_5_Predefined_1:

                    for line in lines:
                        result = self.coord.splitLine(line, tool_id, width)
                        if result == True:
                            break

                    if result:
                        self.coord.COORD_5_NumOfTools_Live[cnt] = 1
                    else:
                        self.coord.COORD_5_NumOfTools_Live[cnt] = 0
                        total_dif += 1

                    cnt += 1

        except FileNotFoundError as err:
            total_dif += len(self.coord.COORD_5_Predefined_1)
            cnt += len(self.coord.COORD_5_Predefined_1)
            print(err)
        
        
        try:
            with open("runs/detect/exp8/labels/al_camera0367_foto_0_2.txt", "w") as dosya:
                dosya.write("")
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp8/labels/al_camera0367_foto_1_2.txt", "w") as dosya:
                dosya.write("")
        except FileNotFoundError as err:
            print(err)


        for i in range(len(self.coord.COORD_5_NumOfTools_Live)):
            if (int(self.lastStatusOfDrawers[4][i]) < int(self.coord.COORD_5_NumOfTools_Live[i])): 
                self.toolsGiven.append(self.coord.COORD_5_ToolNames[i])

            elif (int(self.lastStatusOfDrawers[4][i]) > int(self.coord.COORD_5_NumOfTools_Live[i])):
                self.toolsTaken.append(self.coord.COORD_5_ToolNames[i])


        for i in range(len(self.coord.COORD_5_NumOfTools_Live)):
            if self.coord.COORD_5_NumOfTools_Live[i] == 0:
                
                (x, y) = (self.COORD_5[i][0], self.COORD_5[i][1])
                (w, h) = (self.COORD_5[i][2], self.COORD_5[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_5.append(frame) 
        
        self.lastStatusOfDrawers[4] = self.coord.COORD_5_NumOfTools_Live

        self.toolLabels[4].setText(str(total_dif))
        if self.clickStatus[4] == 1:
            self.showFrames(4)
        
    def readToolsFromFile_2(self):
        toolsArr = []
        self.hideFrames(1)

        for temp in self.frames_2:
            temp.deleteLater()

        self.frames_2 = []

        self.coord.COORD_2_NumOfTools_LiveAll = [0]*91
        self.coord.COORD_2_NumOfTools_Live = [0]*len(self.coord.COORD_2_NumOfTools)
        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_0_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "10" or ilk_eleman == "11" or ilk_eleman == "12" or ilk_eleman == "13" or ilk_eleman == "14" or ilk_eleman == "15" or ilk_eleman == "16":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_1_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "4" or ilk_eleman == "5" or ilk_eleman == "6" or ilk_eleman == "7" or ilk_eleman == "8" or ilk_eleman == "9":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)
        
        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_2_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "2" or ilk_eleman == "3":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)
            ## İkinci model
        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_3_1.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0" or ilk_eleman == "1":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)
        
        try:
            with open("runs/detect/exp4/labels/al_camera0367_foto_0_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "4" or ilk_eleman == "5":
                        temp = int(ilk_eleman) + 17
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp4/labels/al_camera0367_foto_1_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "2" or ilk_eleman == "3":
                        temp = int(ilk_eleman) + 17
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)
        try:
            with open("runs/detect/exp4/labels/al_camera0367_foto_2_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0" or ilk_eleman == "1":
                        temp = int(ilk_eleman) + 17
                        toolsArr.append(str(temp))
        except FileNotFoundError as err:
            print(err)

        for i in range(len(toolsArr)):
            self.coord.COORD_2_NumOfTools_Live[int(toolsArr[i])] += 1
                     
        total_dif = 0
        counter = 0
        
        for i in range(len(self.coord.COORD_2_NumOfTools)):
            if int(self.coord.COORD_2_NumOfTools_Live[i]) > int(self.coord.COORD_2_NumOfTools[i]):
                self.coord.COORD_2_NumOfTools_Live[i] = self.coord.COORD_2_NumOfTools[i]
            temp = int(self.coord.COORD_2_NumOfTools[i]) - int(self.coord.COORD_2_NumOfTools_Live[i])
            total_dif += temp
            temp = int(self.coord.COORD_2_NumOfTools_Live[i])
            if temp < 0:
                temp = 0
            for j in range(temp):
                self.coord.COORD_2_NumOfTools_LiveAll[counter + j] = 1
            counter += self.coord.COORD_2_NumOfTools[i]


        self.readBoundings_2()

        for i in range(len(self.coord.COORD_2_NumOfTools_LiveAll)):
            if (int(self.lastStatusOfDrawers[1][i]) < int(self.coord.COORD_2_NumOfTools_LiveAll[i])):  
                self.toolsGiven.append(self.coord.COORD_2_ToolNames[i])

            elif (int(self.lastStatusOfDrawers[1][i]) > int(self.coord.COORD_2_NumOfTools_LiveAll[i])):
                self.toolsTaken.append(self.coord.COORD_2_ToolNames[i])

        for i in range(len(self.coord.COORD_2_NumOfTools_LiveAll)):
            if self.coord.COORD_2_NumOfTools_LiveAll[i] == 0:
                
                (x, y) = (self.COORD_2[i][0], self.COORD_2[i][1])
                (w, h) = (self.COORD_2[i][2], self.COORD_2[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_2.append(frame) 
        self.lastStatusOfDrawers[1] = self.coord.COORD_2_NumOfTools_LiveAll 

        if self.clickStatus[1] == 1:
            self.showFrames(1)

        self.toolLabels[1].setText(str(total_dif))

        for i in range(4):
            try:
                path = "runs/detect/exp3/labels/al_camera0367_foto_" + str(i) + "_1.txt"
                with open(path, "w") as dosya:
                    dosya.write("")
            except FileNotFoundError as err:
                print(err)

        for i in range(3):
            try:
                path = "runs/detect/exp4/labels/al_camera0367_foto_" + str(i) + "_2.txt"
                with open(path, "w") as dosya:
                    dosya.write("")
            except FileNotFoundError as err:
                print(err)

    def readToolsFromFile_6(self):
        toolsArr = []
        self.hideFrames(5)
        for temp in self.frames_6:
            temp.deleteLater()
        self.frames_6 = []

        try:
            with open("runs/detect/exp9/labels/al_camera0367_foto_0_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0" or ilk_eleman == "4" or ilk_eleman == "5":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)
        
        try:
            with open("runs/detect/exp9/labels/al_camera0367_foto_1_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "3" or ilk_eleman == "6":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)


        try:
            with open("runs/detect/exp9/labels/al_camera0367_foto_2_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "0" or ilk_eleman == "2":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        try:
            with open("runs/detect/exp9/labels/al_camera0367_foto_3_2.txt", "r") as dosya:
                for satir in dosya:
                    satir = satir.strip().split(" ")  # satırı boşluklardan ayırarak bir liste yap
                    ilk_eleman = satir[0]  # listenin ilk elemanını seç
                    if ilk_eleman == "1":
                        toolsArr.append(ilk_eleman)
        except FileNotFoundError as err:
            print(err)

        self.coord.COORD_6_NumOfTools_Live = [0]*len(self.coord.COORD_6_NumOfTools)
        self.coord.COORD_6_NumOfTools_LiveAll = [0]*len(self.coord.COORD_6_NumOfTools_LiveAll)

        
        for i in range(len(toolsArr)):
             self.coord.COORD_6_NumOfTools_Live[int(toolsArr[i])] += 1
                    
        total_dif = 0
        counter = 0
        for i in range(len(self.coord.COORD_6_NumOfTools)):
            if int(self.coord.COORD_6_NumOfTools_Live[i]) > int(self.coord.COORD_6_NumOfTools[i]):
                self.coord.COORD_6_NumOfTools_Live[i] = self.coord.COORD_6_NumOfTools[i]
            temp = int(self.coord.COORD_6_NumOfTools[i]) - int(self.coord.COORD_6_NumOfTools_Live[i])
            total_dif += temp
            temp = int(self.coord.COORD_6_NumOfTools_Live[i])
            if temp < 0:
                temp = 0
            for j in range(temp):
                self.coord.COORD_6_NumOfTools_LiveAll[counter + j] = 1
            counter += self.coord.COORD_6_NumOfTools[i]

        
        cnt = 0
        width = 602
        try:
            with open("runs/detect/exp9/labels/al_camera0367_foto_2_2.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_6_Predefined_1:

                    for line in lines:
                        result = self.coord.splitLine(line, tool_id, width)
                        if result == True:
                            break
                        
                    self.coord.COORD_6_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_6_Predefined_1)
            print(err)

        try:
            with open("runs/detect/exp9/labels/al_camera0367_foto_0_2.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_6_Predefined_2:

                    for line in lines:
                        result = self.coord.splitLine(line, tool_id, width)
                        if result == True:
                            break
                        
                    self.coord.COORD_6_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_6_Predefined_2)
            print(err)

        for i in range(len(self.coord.COORD_6_NumOfTools_LiveAll)):
            if self.coord.COORD_6_NumOfTools_LiveAll[i] == 0:
                
                (x, y) = (self.coord.COORD_6[i][0], self.coord.COORD_6[i][1])
                (w, h) = (self.coord.COORD_6[i][2], self.coord.COORD_6[i][3])
                frame = QLabel(self)
                frame.setGeometry(QtCore.QRect(x, y, w, h))
                frame.setStyleSheet("border: 3px solid red; border-color: rgb(255, 5, 0); background-color: rgba(255, 5, 0, 60)")
                frame.hide()
                self.frames_6.append(frame) 

        for i in range(len(self.coord.COORD_6_NumOfTools_LiveAll)):
            if (int(self.lastStatusOfDrawers[5][i]) < int(self.coord.COORD_6_NumOfTools_LiveAll[i])): 
                self.toolsGiven.append(self.coord.COORD_6_ToolNames[i])

            elif (int(self.lastStatusOfDrawers[5][i]) > int(self.coord.COORD_6_NumOfTools_LiveAll[i])):
                self.toolsTaken.append(self.coord.COORD_6_ToolNames[i])

        self.lastStatusOfDrawers[5] = self.coord.COORD_6_NumOfTools_LiveAll

        for i in range(4):
            try:
                path = "runs/detect/exp9/labels/al_camera0367_foto_" + str(i) + "_2.txt"
                with open(path, "w") as dosya:
                    dosya.write("")
            except FileNotFoundError as err:
                print(err)

        self.toolLabels[5].setText(str(total_dif))
        if self.clickStatus[5] == 1:
            self.showFrames(5)

    def readBoundings_2(self):
        cnt = 0
        width = 926

        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_3_1.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_2_Predefined_1:
                    for line in lines:
                        result = self.coord.splitLine(line, tool_id, width)
                        if result == True:
                            break
                    self.coord.COORD_2_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_2_Predefined_1)
            print(err)

        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_2_1.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_2_Predefined_2_1:
                    for line in lines:
                        if line[0] != "3":
                            result = self.coord.splitLine(line, tool_id, width)
                            if result == True:
                                break
                    self.coord.COORD_2_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_2_Predefined_2_1)
            print(err)

        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_2_1.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_2_Predefined_2_2:
                    for line in lines:
                        if line[0] != "2":
                            result = self.coord.splitLine(line, tool_id, width)
                            if result == True:
                                break
                    
                    self.coord.COORD_2_NumOfTools_LiveAll[cnt] = result
                    cnt += 1

        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_2_Predefined_2_2)
            print(err)

        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_1_1.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_2_Predefined_3_1:
                    for line in lines:
                        if line[0] == "4":
                            result = self.coord.splitLine(line, tool_id, width)
                            if result == True:
                                break
                    self.coord.COORD_2_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_2_Predefined_3_1)
            print(err)

        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_1_1.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_2_Predefined_3_2:
                    for line in lines:
                        if line[0] == "5":
                            result = self.coord.splitLine(line, tool_id, width)
                            if result == True:
                                break
                    
                    self.coord.COORD_2_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_2_Predefined_3_2)
            print(err)


        try:
            with open("runs/detect/exp3/labels/al_camera0367_foto_1_1.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_2_Predefined_3_3:
                    for line in lines:
                        if line[0] == "6" or line[0] == "7" or line[0] == "8" or line[0] == "9":
                            result = self.coord.splitLine(line, tool_id, width)
                            if result == True:
                                break
                    

                    self.coord.COORD_2_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
                
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_2_Predefined_3_3)
            print(err)
                
        cnt += 8
        width = 595

        try:
            with open("runs/detect/exp4/labels/al_camera0367_foto_2_2.txt", 'r') as dosya:
                lines = dosya.readlines()
                for tool_id in self.coord.COORD_2_Predefined_4:
                    for line in lines:
                        result = self.coord.splitLine(line, tool_id, width)
                        if result == True:
                            break
                    
                    self.coord.COORD_2_NumOfTools_LiveAll[cnt] = result
                    cnt += 1
                    
        except FileNotFoundError as err:
            cnt += len(self.coord.COORD_2_Predefined_4)
            print(err)
    
    def colorAnimation(self, index):
        self.anim = QPropertyAnimation(self.toolLabels[0], b"color")
        self.anim.setDuration(2500)
        self.anim.setLoopCount(1000)
        self.anim.setStartValue(QColor(0, 0, 0))
        self.anim.setEndValue(QColor(0, 110, 150))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ToolWindow()
    win.show()
    sys.exit(app.exec_())