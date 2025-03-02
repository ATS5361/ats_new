# This file is created for handling SQLITE dependencies to prevent "sphagetti code"

import sqlite3
import psycopg2

def end_connection():
    sqlConnection.close()

def clear_local_db(table_name):
    sqlConnection = sqlite3.connect(f'database_files/{table_name}.db')
    cursor = sqlConnection.cursor()
    cursor.execute("""DELETE FROM TOOL_TIME WHERE 1=1""")
    sqlConnection.commit()
    sqlConnection.close()

def insert_to_postgre():
    sqlConnection = sqlite3.connect('database_files/TOOL_TIME.db')
    cursorSqlite = sqlConnection.cursor()
    cursorSqlite.execute("""SELECT * FROM TOOL_TIME""")
    sqLiteData = cursorSqlite.fetchall()
    #print(sqLiteData)
    conn = psycopg2.connect(database="toolboxtakip", user="toctoolbox", password="T*00l@Bax!06", host="pgcons.dmnint.intra", port="54001")
    cursor = conn.cursor()
    cursor.executemany(""" INSERT INTO TOOLTRACK VALUES(nextval('record_sequence'),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",sqLiteData)
    
    conn.commit()
    conn.close()

    ## 1. trace neden yapılıyor -> dnn
    ## fusing layers ne -> dnn
    ## sql buradakiş gibi oop ayrılsa olur mu -> olmaz

def passCheck(self):
    password = self.passwordEntry.text()
    if len(password) == 8:
        try:
            sqlConnectionAdm = sqlite3.connect('database_files/add_user_data.db')
            cursorAdm = sqlConnectionAdm.cursor()
            cursorAdm.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM login_data WHERE PASSWORD =:password", {"password":password.upper()})
            recordroot = cursorAdm.fetchall()
            sqlConnectionUsr = sqlite3.connect('database_files/login_data.db')
            cursorUsr = sqlConnectionUsr.cursor()
            cursorUsr.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM login_data WHERE PASSWORD =:password", {"password":password.upper()})
            recorduser = cursorUsr.fetchall()
            sqlConnectionAdm.close()
            sqlConnectionUsr.close()
            if len(recordroot) == 1 and self.isForLogin == False:
                self.showButtons()
            elif len(recorduser) == 1:
                if self.toolWindowFlag:
                    sqlConnection = sqlite3.connect('database_files/login_data.db')
                    cursor = sqlConnection.cursor()
                elif self.userWindowFlag:
                    sqlConnection = sqlite3.connect('database_files/add_user_data.db')
                    cursor = sqlConnection.cursor()
                else:
                    print("HATA!!! db bağlantısı için gerekli ayarlamalar(flagler) eksik yapılmış.")
                cursor.execute("SELECT USERNAME, LASTNAME, DEPARTMENT, PASSWORD FROM login_data WHERE PASSWORD =:password", {"password":password.upper()})
                record = cursor.fetchall()
                dbcon.end_connection()
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

def dataMigrate(self):
    self.insertSQLiteToPostgre()
    if self.completeFlag:
        try:
            self.dbcon.clear_local_db("tools_data")
            self.completeFlag = False
        except Exception as e:
            print(e)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Veri tabanı aktarımı tamamlandı.")
        msg.setWindowTitle("İşlem Tamamlandı")
        msg.exec_()

def insertSQLiteToPostgre(self):
    try:
        dbcon.insert_to_postgre()
    except Exception as e:
        self.completeFlag = False
        print(e)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("OET-TUSAS ağına bağlanamadığı için \nişlem gerçekleştirilemedi lütfen tekrar deneyiniz.")
        msg.setWindowTitle("Bağlantı Hatası")
        msg.exec_()