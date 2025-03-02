from PyQt5.QtCore import Qt, QSize, QSettings, QThread, pyqtSignal, QPropertyAnimation, QRect, QTimer
from PyQt5 import QtWidgets, QtGui, QtCore
from datetime import date, datetime

from PyQt5.QtGui import QIcon, QFont, QColor, QPainter, QPixmap
from PyQt5.QtWidgets import *
from functools import partial
import sqlite3

import sys

class UserWindow(QDialog):
    """Main Window."""
    def __init__(self, parent=None):
        super(UserWindow, self).__init__(parent)
        self.setMinimumSize(QtCore.QSize(500, 715))
        self.setMaximumSize(QtCore.QSize(500, 715))

        self.setWindowFlag(Qt.FramelessWindowHint)

        self.setFont((QFont('Arial', 15)))
        self.setStyleSheet('font-size: 16pt; background-color: #0d0d0d')

        self.createUserImage()
        self.createLabels()
        self.createLayout()
        self.createCloseButton()
        
        self.cardLineEdit = QLineEdit(self)
        self.cardLineEdit.setFixedWidth(0)
        self.cardLineEdit.hide()
        self.cardLineEdit.textChanged.connect(self.readCard)
        self.addButton.clicked.connect(self.addUser)

        self.closeButton.clicked.connect(self.closeWindow)
        self.setLayout(self.vLayout)

    def addUser(self):
        isim = self.nameLabel_entry.text()
        soyisim = self.surnameLabel_entry.text()
        sicil = self.sicilLabel_entry.text()
        departman = self.departmanLabel_entry.text()

        if isim == "" or soyisim == "" or sicil == "" or departman == "":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Hata!")
            msg.setInformativeText("Lütfen tüm alanları doldurunuz.")
            msg.setWindowTitle("Hata")
            msg.exec_()
        else:
            self.addButton.setText("KARTINIZI OKUTUN")
            self.addButton.setEnabled(False)
            self.cardLineEdit.show()
            self.cardLineEdit.setFocus(True)

    def readCard(self):
        password = self.cardLineEdit.text()
        if len(password) == 8:
            self.signUp(self.nameLabel_entry.text(), self.surnameLabel_entry.text(), self.departmanLabel_entry.text(), password)
            self.cardLineEdit.setFocus(False)
            self.cardLineEdit.hide()
            self.addButton.setText("EKLE")
            self.addButton.setEnabled(True)
            self.cardLineEdit.clear()
        print(password)

    def closeWindow(self):
        self.close()

    def createCloseButton(self):
        self.closeButton = QPushButton(self)
        self.closeButton.setIcon(QIcon("images/close-icon-old.png"))
        self.closeButton.setStyleSheet("background-color: transparent; border: 0px")
        self.closeButton.setIconSize(QSize(40, 40))
        self.closeButton.move(410, 25)
        
    def createLabels(self):
        self.nameLabel = QLabel("İsim:")
        self.surnameLabel = QLabel("Soyisim: ")
        self.departmanLabel = QLabel("Departman: ")

    def createUserImage(self):
        self.userImg = QPushButton(self)
        self.userImg.setIcon(QIcon("images/mechanic-icon.png"))
        self.userImg.setStyleSheet("background-color: transparent; border: 0px")
        self.userImg.setIconSize(QSize(220,220))

    def createLayout(self):
        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.userImg)
        self.vLayout.setContentsMargins(25, 10, 25, 10)
        self.groupBox = QGroupBox()
        self.groupBox.setStyleSheet("color: #B8B8B8; font-weight: bold; padding: 2px; font-size: 14pt; background-color: rgba(0, 153, 255, 20);")
        self.groupBox.setMaximumHeight(250)
        
        # self.groupBox.setCheckable(True)
        self.mainLabel = QLabel("KULLANICI EKLE")
        self.mainLabel.setFixedHeight(50)
        self.mainLabel.setStyleSheet("color: #B8B8B8; font-weight: bold; padding: 8px; font-size: 26pt;")
        self.vLayout.addWidget(self.mainLabel)
        self.mainLabel.setAlignment(Qt.AlignCenter)
        self.vLayout.addWidget(self.groupBox)

        gridBox = QGridLayout()

        self.nameLabel = QLabel("İSİM   ")
        self.surnameLabel = QLabel("SOYİSİM  ")
        self.departmanLabel = QLabel("DEPARTMAN   ")
        self.sicilLabel = QLabel("SİCİL  ")

        self.nameLabel_entry = QLineEdit()
        self.surnameLabel_entry = QLineEdit()
        self.departmanLabel_entry = QLineEdit()
        self.sicilLabel_entry = QLineEdit()

        self.nameLabel_entry.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.surnameLabel_entry.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.departmanLabel_entry.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.sicilLabel_entry.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        
        self.nameLabel.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.surnameLabel.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.departmanLabel.setStyleSheet("background-color: rgba(0, 153, 255, 3);")
        self.sicilLabel.setStyleSheet("background-color: rgba(0, 153, 255, 3);")



        self.groupBox.setLayout(gridBox)

        gridBox.addWidget(self.nameLabel, 0, 0)
        gridBox.addWidget(self.surnameLabel, 1, 0)
        gridBox.addWidget(self.departmanLabel, 2, 0)
        gridBox.addWidget(self.sicilLabel, 3, 0)

        gridBox.addWidget(self.nameLabel_entry, 0, 3)
        gridBox.addWidget(self.surnameLabel_entry, 1, 3)
        gridBox.addWidget(self.departmanLabel_entry, 2, 3)
        gridBox.addWidget(self.sicilLabel_entry, 3, 3)



        self.addButton = QPushButton("EKLE")
        self.addButton.setStyleSheet("color: #B8B8B8; font-weight: bold; padding: 8px; background-color: rgba(0, 153, 255, 100); font-size: 17pt;")
        
        self.vLayout.addWidget(self.addButton)

    def signUp(self, name, surname, department, password):

        try:
            sqlConnection = sqlite3.connect('database_files/login_data.db')
            cursor = sqlConnection.cursor()
            insert_data = (name.upper(), surname.upper(), department.upper(), password.upper())
            cursor.execute('''INSERT INTO login_data (USERNAME, LASTNAME, DEPARTMENT, PASSWORD)
             VALUES(?,?,?,?);''', insert_data)
            sqlConnection.commit()
            self.close()
        except sqlite3.Error as err:
            print("HATA!!! :", err)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UserWindow()
    win.show()
    sys.exit(app.exec_())