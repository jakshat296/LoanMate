import os
import io
import sys
import time
import pytz
import math
import cv2
import random
import urllib3
import joblib
import subprocess
import requests  
import string
import ctypes
import resources
import traceback
import numpy as np
import mysql.connector
from PIL import Image
from datetime import date
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from add_cash import LoginDialog2
from remove_cash import LoginDialog1
from loading_dialog import FingerprintDialog
from datetime import date, timedelta
from PyQt5.QtGui import QColor, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QColor, QFont, QBrush, QImage, QMovie
from PyQt5.QtCore import Qt, QTime, QTimer, QDateTime, QPropertyAnimation, QEasingCurve, QSize, QBuffer, QStringListModel
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QLabel, QDialog, QMainWindow, QApplication, QCompleter, QMainWindow, QPushButton, QHeaderView, QFileDialog, QProgressBar, QVBoxLayout, QProgressDialog, QDesktopWidget
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis, QLineSeries




#Essential Functions before defining main ui class and additional functionalities


isoTemplate = ''
def get_info():
    res = requests.get('https://localhost:8003/mfs100/info', verify=False)

def capture():
    global isoTemplate
    res = requests.post('https://localhost:8003/mfs100/capture', data={
        "Quality": 60,
        "TimeOut": 10
    }, verify=False)
    isoTemplate = res.json()['IsoTemplate']

def fingerprint_match(isoTemplateToMatch, fingerprint_data, mycursor):
        try:
                res2 = requests.post('https://localhost:8003/mfs100/verify', data={
                "ProbTemplate": fingerprint_data,
                "GalleryTemplate": isoTemplateToMatch,
                "BioType": "FMR"
                }, verify=False)
                matchResponse = res2.json()
                if matchResponse.get('Status'):
                        query = "select user_id from fingerprint_table where fingerprint_data = %s"
                        mycursor.execute(query, (fingerprint_data,))
                        id = mycursor.fetchone()
                        return id[0]
        except Exception as e:
                messagebox.showerror("Error",f"{str(e)}")
        return None

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#applying customized styles to QtWidgets using this class
class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

class Ui_MainWindow(object):
    
    #---------order of defining functionalities------------------------------
    ### 1. Calling user interfaces
    ### 2. additional functionalities
    ### 3. Necessary functions
    ### 4. File handling Functions 


#functions to call different Ui 
    def close(self):
        self.close()

    def DashBoard(self):
        self.stackedWidget.setCurrentIndex(0)
        self.insert_current_date()
        self.plainTextEdit.clear()
        self.lineEdit.clear()
        self.plainTextEdit.setPlainText("Daily Assessment Report!!")
        self.populate_chart()
        self.statistics()

    def add_record(self):
        self.stackedWidget.setCurrentIndex(1)
        self.insert_current_date()
        utc_now = datetime.utcnow()
        tz = pytz.timezone('Asia/Kolkata')
        local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
        date = local_now.strftime("%Y-%m-%d")
        self.jewellery_7.setText(date)
        self.clear()

    def remove(self):
        self.stackedWidget.setCurrentIndex(2)
        self.label_4.setStyleSheet("QPushButton {\n"
"    background-color: rgb(18,18,18);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
     
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        self.tableWidget_exist_5.setRowCount(0)
        self.comboBox_3.setCurrentIndex(0)
        self.user_id = 0
    def deposit(self):
        self.stackedWidget.setCurrentIndex(3)
        self.lineEdit_7.clear()
        self.lineEdit_8.clear()
        self.tableWidget_5.setRowCount(0)
        self.comboBox_4.setCurrentIndex(0)

    def view(self):
        self.stackedWidget.setCurrentIndex(4)
        self.lineEdit_removed_3.clear()
        self.tableWidget_removed_9.setRowCount(0)

    def removed(self):
        self.stackedWidget.setCurrentIndex(5)
        self.lineEdit_removed_4.clear()
        self.tableWidget_removed_10.setRowCount(0)

    def accounts(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Date", "Amount"])
        self.lineEdit_2.clear()
        self.label_3.setText("")
        self.stackedWidget.setCurrentIndex(6)
    
    def add_cash(self):
        self.insert_current_date()
        self.window = QtWidgets.QMainWindow()
        self.ui = LoginDialog2()
        self.center_on_screen(self.ui)
        self.ui.show()

    def remove_cash(self):
        self.insert_current_date()
        self.window = QtWidgets.QMainWindow()
        self.ui = LoginDialog1()
        self.center_on_screen(self.ui)
        self.ui.show()

    def open_loading_dialog(self):
        self.window = QtWidgets.QMainWindow()
        self.loading = FingerprintDialog()
        self.center_on_screen(self.loading)
        self.loading.show()

    def close_loading_dialog(self):
        self.loading.close()

    def center_on_screen(self, widget):
        # Get the available geometry of the screen
        desktop = QDesktopWidget()
        screen_geometry = desktop.availableGeometry()

        # Calculate the center point
        center_point = screen_geometry.center()

        # Move the widget to the center
        widget.move(center_point - widget.rect().center())

    def updateTime(self):
        current_time = QTime.currentTime()
        time_text = current_time.toString("hh:mm:ss")

#---------------------------Necessary Functionalities------------------------------
    ###creating function for additional functionalities
    ### 1. function to setup connection with database
    ### 2. statistics function
    ### 3. extracting id of triggered record
    ### 4. graphical presentation of investments and returns 
    ### 5. Updating lineEdits with completer models
    ### 6. function to call fingerprint scanner through get and post commands
    ### 7. function to create a list of dates of past 5 days
    ### 8. function to fetch current date in specified format
    ### 9. function to fetch previous record from the database
    ### 10. function to clear the lineEdits of add record
    ### 11. function to prevent double click of pushbuttons
    ### 12. function to clear lineEdits
    ### 13. function to search for available usb drive
    ### 14. Function to format the number according to the Indian numbering system
    ### 15. function to disable lineEdits on certain conditions
    ### 16. Function TO Centre the Imported UIs

    #function to set up connection with the database
    def call(self):
        self.con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="akshat",
        database="loan_management",
        auth_plugin="caching_sha2_password" 
        )
    
    #function to fetch previous record
    def insert_current_date(self):
        self.call()
        cursor = self.con.cursor()
        utc_now = datetime.utcnow()
        tz = pytz.timezone('Asia/Kolkata')
        local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
        current_date = local_now.strftime("%Y-%m-%d")
        num = np.arange(1,25,2)
        query = f'SELECT DATE_SUB("{current_date}", INTERVAL 1 DAY) AS PreviousDate;'
        cursor.execute(query)
        previous_date = cursor.fetchone()
        previous_date = str(previous_date[0])
        query = f'SELECT COUNT(*) FROM daily_assessment WHERE date = "{current_date}"'
        cursor.execute(query)
        count = cursor.fetchone()[0]
        cursor.execute(f'delete From daily_assessment where date < "{previous_date}"')
        self.con.commit()
        if count == 0:
            # Insert the current date
            cursor.execute(f'INSERT INTO daily_assessment (date) VALUES ("{current_date}")')
            self.con.commit()
        else:
               pass

    # function to fetch current date in specified format
    def get_current_date_time_day(self):
        utc_now = QDateTime.currentDateTimeUtc()
        tz = pytz.timezone('Asia/Kolkata')  # Replace with your time zone
        local_now = utc_now.toTimeZone(tz)
        current_date = local_now.toString("yyyy-MM-dd")
        current_time = local_now.toString("HH:mm:ss")
        current_day = local_now.toString("dddd")  # Day of the week
        return f"{current_date} {current_time} {current_day}"
    
    # Function to move the Wdiget to Center
    def center_on_screen(self, widget):
        desktop = QDesktopWidget()
        screen_geometry = desktop.availableGeometry()
        center_point = screen_geometry.center()
        widget.move(center_point - widget.rect().center())

    #function to create instance of capture function
    def capture1(self):
         capture()    

    #function to add fingerprint in mysql database
    def cap(self):
         try:
                self.capture1()
                self.call()
                cursor = self.con.cursor()
                insert_query = "INSERT INTO fingerprint_table (user_id , fingerprint_data) VALUES (%s,%s)"
                cursor.execute(insert_query, (user,isoTemplate,))
                self.con.commit()
                messagebox.showinfo("Success!","Fingerprint Stored Successfully!")
                self.clear()

         except Exception as ex:
              if str(ex) == "'IsoTemplate'":
                        messagebox.showerror("Error", "Connect The Scanner")
              else:
                        messagebox.showerror("Error",f"{str(ex)}")

         finally:
                if self.con:
                        self.con.close()

    # function to create a list of dates of past 5 days
    def get_past_5_dates(self):
        current_date = date.today()
        date_list = []
        for i in range(5):
                past_date = current_date - timedelta(days=i)
                date_list.append(past_date.strftime("%d-%m"))
        self.labels = date_list

    #function to extract id of triggered record
    def extract_id(self, item):
        try:
            self.id = item.text()
        except Exception as ex:
            messagebox.showerror("Error",f"{str(ex)}")

    #function to locate available usb drive 
    def get_available_drive_letter(self):
        used_drive_letters = set()
        for drive in string.ascii_uppercase:
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(f"{drive}:\\")
            if drive_type == 2:  # Drive is a removable storage (like USB)
                used_drive_letters.add(drive)
        return used_drive_letters
    
    # Function to format the number according to the Indian numbering system
    def format_indian_number(self,number_str):
        num_parts = []
        length = len(number_str)
        
        if length <= 3:
                return number_str  # No need for commas if the number is less than 1000.

        num_parts.append(number_str[-3:])
        number_str = number_str[:-3]

        while number_str:
                num_parts.append(number_str[-2:])
                number_str = number_str[:-2]

        formatted_number = ",".join(reversed(num_parts))
        return formatted_number

    #function to create graph
    def populate_chart(self):
        self.chart.removeAllSeries()
        for axis in self.chart.axes():
                self.chart.removeAxis(axis)
        self.get_past_5_dates()
        self.call()
        cursor = self.con.cursor()
        utc_now = datetime.utcnow()
        tz = pytz.timezone('Asia/Kolkata')
        local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
        date = local_now.strftime("%Y-%m-%d")
        current1 = self.comboBox.currentIndex()
        if current1 == 0:
                self.label_22.setText("Total Investments")
                self.chart.setTitle("Total Investments")
                query = f"""
                        SELECT
    IFNULL(SUM(all_records.amount), 0) AS total_investment
FROM
    (
        SELECT "{date}" AS date
        UNION ALL
        SELECT "{date}" - INTERVAL 1 DAY
        UNION ALL
        SELECT "{date}" - INTERVAL 2 DAY
        UNION ALL
        SELECT "{date}" - INTERVAL 3 DAY
        UNION ALL
        SELECT "{date}" - INTERVAL 4 DAY
    ) AS calendar
LEFT JOIN
    all_records ON calendar.date = DATE(all_records.date)
GROUP BY
    calendar.date;
"""
        elif current1 == 1:
                self.label_22.setText("Total Returns")
                self.chart.setTitle("Total Returns")
                query = f"""
                        SELECT
        IFNULL(SUM(removed_records.amount+interest), 0) AS total_interest
        FROM
        (
                SELECT "{date}" AS date
                UNION ALL
                SELECT "{date}" - INTERVAL 1 DAY
                UNION ALL
                SELECT "{date}" - INTERVAL 2 DAY
                UNION ALL
                SELECT "{date}" - INTERVAL 3 DAY
                UNION ALL
                SELECT "{date}" - INTERVAL 4 DAY
        ) AS calendar
        LEFT JOIN
        removed_records ON calendar.date = DATE(removed_records.removed_date)
        GROUP BY
        calendar.date;

                """
        # Set the title font size
        title_font = QFont("Arial", 16)
        title_font.setBold(True)
        self.chart.setTitleFont(title_font)
        title_brush = QBrush(QColor(200, 200, 200))
        self.chart.setTitleBrush(title_brush)
        cursor.execute(query)
        results = cursor.fetchall()
        sum_amounts = [row[0] for row in results]
        cursor.close()
        self.con.close()
        #return sum_amounts
        amount = [int(amount) for amount in sum_amounts]
        values = amount
        series = QBarSeries()
        set0 = QBarSet("Values")
        for i in range(len(amount)):
                set0.append(values[i])
        series.append(set0)
        self.chart.addSeries(series)
        axis_x = QBarCategoryAxis()
        axis_x.append(self.labels)
        self.chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        axis_y = QValueAxis()
        self.chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        if current1 == 0:
                axis_x.setTitleText("Past 5 Days")
                axis_y.setTitleText("Total Investments")
        elif current1 == 1:
                axis_x.setTitleText("Past 5 Days")
                axis_y.setTitleText("Total Interest Earned") 
        axis_x.setTitleFont(QFont("Arial", 10))
        axis_x.setTitleBrush(QBrush(QColor(200, 200, 200)))
        axis_y.setTitleFont(QFont("Arial", 10))
        axis_y.setTitleBrush(QBrush(QColor(200, 200, 200)))
        axis_x.setGridLineVisible(False)
        axis_y.setGridLineVisible(False)
        axis_x.setLabelsColor(QColor(255, 255, 255))
        axis_x.setLabelsFont(QFont("Arial", 12))
        axis_y.setLabelsColor(QColor(255, 255, 255))
        axis_y.setLabelsFont(QFont("Arial", 12))
        self.chart.legend().setVisible(False)

    #functions to set up QCompleter for different lineEdits
    def update_completer_model(self):
        try:
                self.call()
                mycursor = self.con.cursor()
                current = self.comboBox_3.currentText()
                text = self.lineEdit_5.text()
                if current == "Name":
                        query = f'SELECT distinct(name) FROM all_records WHERE name LIKE "{text}%"'
                elif current == "Location":
                        query = f'SELECT distinct(location) FROM all_records WHERE location LIKE "{text}%"'
                elif current == "Date":
                               query = f'SELECT distinct(date) from all_records where date = "2000-01-01"'
                #execute and fetch data
                mycursor.execute(query)
                result = mycursor.fetchall()
                if len(result) >= 1:
                        # Update the completer's model
                        model = QStringListModel([str(i[0]) for i in result], self.completer)
                        self.completer.setModel(model)
        except Exception as ex:
               messagebox.showerror("Error",f"{ex}")
    def update_completer_1_model(self):
        try:
                        self.call()
                        mycursor = self.con.cursor()
                        text = self.jewellery_4.text()
                        query = f'SELECT distinct(location) FROM all_records WHERE location LIKE "{text}%"'
                        #execute and fetch data
                        mycursor.execute(query)
                        result = mycursor.fetchall()                        
                        # Update the completer's model
                        model = QStringListModel([str(i[0]) for i in result], self.completer_1)
                        self.completer_1.setModel(model)
        except Exception as ex:
               messagebox.showerror("Error",f"{ex}")
    def update_completer_2_model(self):
        try:
                        self.call()
                        mycursor = self.con.cursor()
                        current = self.comboBox_4.currentText()
                        text = self.lineEdit_7.text()
                        if current == "Name":
                                query = f'SELECT distinct(name) FROM all_records WHERE name LIKE "{text}%"'
                        elif current == "Location":
                                query = f'SELECT distinct(location) FROM all_records WHERE location LIKE "{text}%"'                       
                        #execute and fetch data
                        mycursor.execute(query)
                        result = mycursor.fetchall()
                        # Update the completer's model
                        model = QStringListModel([str(i[0]) for i in result], self.completer_2)
                        self.completer_2.setModel(model)
        except Exception as ex:
               messagebox.showerror("Error",f"{ex}")
    def update_completer_3_model(self):
        try:
                        self.call()
                        mycursor = self.con.cursor()
                        current = self.comboBox_removed_3.currentText()
                        text = self.lineEdit_removed_3.text()
                        if current == "By Name":
                                query = f'SELECT distinct(name) FROM all_records WHERE name LIKE "{text}%"'
                        elif current == "By Location":
                                query = f'SELECT distinct(location) FROM all_records WHERE location LIKE "{text}%"'
                        elif current == "By Date":
                               query = f'SELECT distinct(date) from all_records where date = "2000-01-01"'
                        #execute and fetch data
                        mycursor.execute(query)
                        result = mycursor.fetchall()
                        if len(result) >= 1:
                                # Update the completer's model
                                model = QStringListModel([str(i[0]) for i in result], self.completer_3)
                                self.completer_3.setModel(model)
        except Exception as ex:
               messagebox.showerror("Error",f"{ex}")
    def update_completer_4_model(self):
        try:
                        self.call()
                        mycursor = self.con.cursor()
                        current = self.comboBox_removed_4.currentText()
                        text = self.lineEdit_removed_4.text()
                        if current == "By Name":
                                query = f'SELECT distinct(name) FROM removed_records WHERE name LIKE "{text}%"'
                        elif current == "By Location":
                                query = f'SELECT distinct(location) FROM removed_records WHERE location LIKE "{text}%"'
                        elif current == "By Date":
                               query = f'SELECT distinct(date) from removed_records where date = "2000-01-01"'
                        #execute and fetch data
                        mycursor.execute(query)
                        result = mycursor.fetchall()
                        if len(result) >= 1:
                                # Update the completer's model
                                model = QStringListModel([str(i[0]) for i in result], self.completer_4)
                                self.completer_4.setModel(model)
        except Exception as ex:
               messagebox.showerror("Error",f"{ex}")
    def update_completer_6_model(self):
        try:
                        self.call()
                        mycursor = self.con.cursor()
                        text = self.jewellery_2.text()
                        query = f'select distinct(name) from all_records where name like "{text}"'
                        #execute and fetch data
                        mycursor.execute(query)
                        result = mycursor.fetchall()
                        # Update the completer's model
                        model = QStringListModel([str(i[0]) for i in result], self.completer_6)
                        self.completer_6.setModel(model)
        except Exception as ex:
               messagebox.showerror("Error",f"{ex}")

    #function to disable a lineEdit_5 on a condition
    def disable_lineEdit_5(self):
        current = self.comboBox_3.currentText()
        if current == "Fingerprint":
               self.lineEdit_5.setDisabled(True)
               self.lineEdit_5.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(18,18,18);\n"
"}\n"
)
        else:
              self.lineEdit_5.setDisabled(False)
              self.lineEdit_5.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")

    #function to disable a lineEdit
    def disable_lineEdit_7(self):
        current = self.comboBox_4.currentText()
        if current == "Fingerprint":
               self.lineEdit_7.setDisabled(True)
               self.lineEdit_7.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(18,18,18);\n"
"}\n"
)
        else:
              self.lineEdit_7.setDisabled(False)
              self.lineEdit_7.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
    # creating statistics function to extract realtime data from database
    def statistics(self):
        self.call()
        utc_now = datetime.utcnow()
        tz = pytz.timezone('Asia/Kolkata')
        local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
        date = local_now.strftime("%Y-%m-%d")
        mycursor = self.con.cursor()
        #executing query for total investment
        query = "select sum(amount) from all_records"
        mycursor.execute(query)
        total_i = mycursor.fetchone()
        total_i = str(total_i[0])
        if total_i == "None":
              self.total_investment.setText(f"[ {str(0)} ]")
        else:
                total_i = self.format_indian_number(total_i)
                self.total_investment.setText(f"[ {total_i} ]")
        #executing query for total count
        query = "select count(*) from all_records"
        mycursor.execute(query)
        total_n = mycursor.fetchone()
        total_n = str(total_n[0])
        self.lineEdit_9.setText(f"[ {total_n} ]")
        #executing query for todays investment
        query = f'select sum(amount) from all_records where date = "{date}"'
        mycursor.execute(query)
        total_i = mycursor.fetchone()
        total_i = str(total_i[0])
        if total_i == "None":
            self.todays_investment.setText(f"[ {str(0)} ]")
        else:
                total_i = self.format_indian_number(total_i)
                self.todays_investment.setText(f"[ {total_i} ]")
        #executing query for today's count
        query = f'select count(*) from all_records where date = "{date}" '
        mycursor.execute(query)
        total_ino = mycursor.fetchone()
        total_ino = str(total_ino[0])
        if total_i == "None":
            self.lineEdit_10.setText(f"[ {str(0)} ]")
        else:
                self.lineEdit_10.setText(f"[ {total_ino} ]")
        #executing query for todays return including interest
        query = f' select sum(amount+interest) from removed_records where removed_date = "{date}";'
        mycursor.execute(query)
        total_i = mycursor.fetchone()
        total_i = str(total_i[0])
        if total_i == "None":
            self.todays_return.setText(f"[ {str(0)} ]")
        else:
                total_i = self.format_indian_number(total_i)
                self.todays_return.setText(f"[ {total_i} ]")
        #executing query for todays return including interest
        query = f'select count(*) from removed_records where removed_date = "{date}";'
        mycursor.execute(query)
        total_i = mycursor.fetchone()
        total_i = str(total_i[0])
        if total_i == "None":
            self.lineEdit_11.setText(f"[ {str(0)} ]")
        else:
                self.lineEdit_11.setText(f"[ {total_i} ]")
        #executing query for todays interest
        query = f' select sum(interest) from removed_records where removed_date = "{date}" '
        mycursor.execute(query)
        total_i = mycursor.fetchone()
        total_i = str(total_i[0])
        if total_i == "None":
            self.todays_interest.setText(f"[ {str(0)} ]")
        else:
                total_i = self.format_indian_number(total_i)
                self.todays_interest.setText(f"[ {total_i} ]")

    #function to center the called UIs
    def center_on_screen(self, widget):
        desktop = QDesktopWidget()
        screen_geometry = desktop.availableGeometry()
        center_point = screen_geometry.center()
        widget.move(center_point - widget.rect().center())

    #function to clear the lineEdits of add record
    def clear(self):
        self.jewellery_4.clear()
        self.jewellery_2.clear()
        self.jewellery_3.clear()
        self.jewellery_5.clear()
        self.jewellery_6.clear()
        self.jewellery_8.clear()

    #function to prevent double click on a pushButton
    def allowClick(self):
        self.pushButton_13.setEnabled(True)

    def call_camera(self):
        # Initialize the camera
        cap = cv2.VideoCapture(0)

        while True:
                # Capture frame-by-frame
                ret, frame = cap.read()

                # Display the resulting frame
                cv2.imshow('Press space to capture', frame)

                # Check if space key is pressed
                if cv2.waitKey(1) & 0xFF == ord(' '):
                        # Save the image
                        cv2.imwrite(f'C:\\Users\\Jitendra Jain\\Downloads\\LoanMate\\LoanMate\\images\\{user}.jpg', frame)
                        break

        # When everything done, release the capture and destroy windows
        cap.release()
        cv2.destroyAllWindows()

    def check_image_exists(self,id):
        # Specify the path to the folder where your images are stored
        folder_path = 'C:\\Users\\Jitendra Jain\\Downloads\\LoanMate\\LoanMate\\images'

        # Create the full file path
        self.file_path = os.path.join(folder_path, f'{id}.jpg')
        # Check if the file exists
        if os.path.isfile(self.file_path):
                self.label_4.setStyleSheet("QPushButton {\n"
"    background-color: rgb(0,170,0);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
                self.label_4.setText("View")
        else:
                self.label_4.setStyleSheet("QPushButton {\n"
"    background-color: rgb(170,0,0);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
    
    def open_image(self):
        from PIL import Image
        try:
                id = int(self.user_id)
                # Specify the path to the folder where your images are stored
                folder_path = 'C:\\Users\\Jitendra Jain\\Downloads\\LoanMate\\LoanMate\\images'

                # Create the full file path
                file_path = os.path.join(folder_path, f'{id}.jpg')
                img = Image.open(file_path)   
                img.show()   
        except Exception as ex:
               print(ex)
           
#-----------------------------------Important Functionalities----------------------------------------
        ### 1. Function to add new record
        ### 2. Search record function for remove record
        ### 3. Calculate interest of selected record
        ### 4. function to remove record
        ### 5. function to delete record
        ### 6. search record function to add deposit
        ### 7. function to add deposit
        ### 8. search record function to view existing records
        ### 9. search record function to view removed records

    #function to add data into database
    user = 0
    def addnew(self):
        global user
        self.double_click_protect.start(8000) 
        self.pushButton_13.setEnabled(False)
        self.call()
        cursor = self.con.cursor()
        try: 
                if self.jewellery_5.text() == "" or self.jewellery_2.text() == "" or self.jewellery_3.text() == "" or self.jewellery_4.text() == "" or self.jewellery_6.text() == "" or self.jewellery_8.text() == "":
                       messagebox.showerror("Error","Fill all the Details")
                else:
                       
                        amount  = int(self.jewellery_5.text())
                        name  = self.jewellery_2.text()
                        name = name[0].upper() + name[1:].lower()
                        fname = self.jewellery_3.text()
                        fname = fname[0].upper() + fname[1:].lower()
                        location = self.jewellery_4.text()
                        location = location[0].upper() + location[1:].lower()
                        type = self.jewellery_6.text()
                        type = type[0].upper() + type[1:].lower()
                        weight = self.jewellery_8.text()
                date = self.jewellery_7.text()
                query = "select max(user_id) + 1 from all_records"
                cursor.execute(query)
                user = cursor.fetchone()
                if str(user[0]) == "None":
                       user = int(101)
                else:
                        user = int(user[0])
                # Prepare the SQL query
                query = "INSERT INTO all_records (user_id,amount,name,Father_name,Location,Date,Type,Weight) values (%s,%s, %s, %s,%s,%s,%s,%s)"
                values = (user,amount,name,fname,location,date,type,weight)
                # Execute the query
                cursor.execute(query, values)
                self.con.commit()
                messagebox.showinfo("Success!","Data Added Successfully.")
                # Close the cursor and connection
                cursor.close()
                self.con.close()
                #self.clear()
        except Exception as ex:
             if str(ex) == "cannot access local variable 'amount' where it is not associated with a value":
                        pass
             else:
                messagebox.showerror("Error",f"{str(ex)}")


    #function to search records in order to remove or delete them from the database
    def search_remove(self):
        self.call()
        mycursor = self.con.cursor()
        self.tableWidget_exist_5.setRowCount(0)
        current = self.comboBox_3.currentText()
        try:
                if current == "Fingerprint":
                # Capture the template to match                                         
                        res = requests.post('https://localhost:8003/mfs100/capture', data={
                                "Quality": 60,
                                "TimeOut": 10
                        }, verify=False)
                        isoTemplateToMatch = res.json()['IsoTemplate']
                        self.open_loading_dialog()
                        query = "SELECT fingerprint_data FROM fingerprint_table;"
                        mycursor.execute(query)
                        result = mycursor.fetchall()
                        
                        ilist = []
                        
                        # Use joblib to parallelize fingerprint matching
                        num_jobs = 30
                        parallel = joblib.Parallel(n_jobs=num_jobs, backend="threading")  # Use threading backend for PyQt
                        fingerprint_matches = parallel(
                                joblib.delayed(fingerprint_match)(isoTemplateToMatch, i[0], mycursor) for i in result
                        )
                        
                        # Collect the matching user IDs
                        ilist = [id for id in fingerprint_matches if id is not None]
                        self.close_loading_dialog()

                        if len(ilist) == 0:
                                messagebox.showinfo("Oops!", "No Record Found")
                        else:
                                user_ids_str = ",".join(str(user_id) for user_id in ilist)
                                query = f"SELECT * FROM all_records WHERE user_id IN ({user_ids_str})"
                                mycursor.execute(query)

                elif current == "Location":
                        if self.lineEdit_5.text() == "":
                              messagebox.showerror("Error","Please enter location")
                        else:
                                location = self.lineEdit_5.text()
                                location = location[0].upper() + location[1:]
                                query = f'SELECT * FROM all_records WHERE location = "{location}"'
                                mycursor.execute(query)
                elif current == "Name": 

                        if self.lineEdit_5.text() == "":
                              messagebox.showerror("Error","Please enter Name")
                        else:
                                # Create a QCompleter object for the line edit
                                name = self.lineEdit_5.text()
                                name = name[0].upper() + name[1:]
                                query = f'SELECT * FROM all_records WHERE name = "{name}"'
                                mycursor.execute(query)
                
                elif current == "Date": 
                        if self.lineEdit_5.text() == "":
                              messagebox.showerror("Error","Please enter Date")
                        else:
                                date = self.lineEdit_5.text()
                                date = date[0].upper() + date[1:]
                                query = f'SELECT * FROM all_records WHERE date = "{date}"'
                                mycursor.execute(query)

                else:
                        messagebox.showerror("Error","Something Unexpected Occur")

                result = mycursor.fetchall()
                if len(result) == 0:
                       messagebox.showinfo("Oops!","No record Found")
                else:
                       
                        self.tableWidget_exist_5.setRowCount(0)
                        for row_number, row_data in enumerate(result):
                                self.tableWidget_exist_5.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                        item = QTableWidgetItem(str(data))
                                        item.setForeground(QColor(255, 255, 255))
                                        self.tableWidget_exist_5.setItem(row_number,
                                                column_number, item)
                        self.tableWidget_exist_5.itemClicked.connect(self.calculate)  

        except Exception as ex:
                if str(ex) == "'IsoTemplate'":
                        messagebox.showerror("Error", "Connect The Scanner")
                elif str(ex) == "No result set to fetch from":
                       pass
                else:
                        messagebox.showerror("Error",f"{str(ex)}")

        finally:
                if self.con.is_connected():
                        mycursor.close()
                        self.con.close()
    
    #function to calculate interest of the particular record
    def calculate(self, item):
        try: 
                self.call()
                self.user_id = item.text()
                mycursor = self.con.cursor()
                """query = f"SELECT fingerprint_data FROM fingerprint_table WHERE user_id = {self.user_id}"
                mycursor.execute(query)
                data = mycursor.fetchone()
                if str(data) == "None":
                       self.label_4.setStyleSheet("background-color: rgb(170,0,0);")
                elif str(data) != "None":
                       self.label_4.setStyleSheet("background-color: rgb(0,170,0);")"""
                self.check_image_exists(self.user_id)
                query = "SELECT date FROM all_records WHERE user_id = %s"
                values = (self.user_id,)
                mycursor.execute(query, values)
                date = mycursor.fetchone()
                previous_date = str(date[0])
                query = "SELECT amount FROM all_records WHERE user_id = %s"
                values = (self.user_id,)
                mycursor.execute(query, values)
                principle = mycursor.fetchone()
                p = int(principle[0])
                current_date = datetime.now().strftime("%Y-%m-%d")
                start_dt = datetime.strptime(previous_date, "%Y-%m-%d")
                end_dt = datetime.strptime(current_date, "%Y-%m-%d")
                time_diff = end_dt - start_dt
                time_in_seconds = time_diff.total_seconds()
                seconds_per_year = 365.24 * 24 * 3600  # Account for leap years
                time_in_years = time_in_seconds / seconds_per_year
                string_value = str(time_in_years)
                decimal_index = string_value.index('.')
                after_decimal = float(string_value[decimal_index:])
                interest_rate = 0.36
                if time_in_years <= 1:
                       interest = p*interest_rate*time_in_years
                       interest = str(round(interest))
                       self.lineEdit_6.setText(str(interest))
                if time_in_years > 1 and time_in_years <= 2:
                        interest1 = p*interest_rate
                        p = p + interest1
                        interest2 = p*interest_rate*after_decimal
                        interest = interest1 + interest2
                        interest = str(round(interest))
                        self.lineEdit_6.setText(interest)
                if time_in_years > 2 and time_in_years <= 3:
                        interest1 = p*interest_rate
                        p = p + interest1
                        interest2 = p*interest_rate
                        p = p + interest2
                        interest3 = p*interest_rate*after_decimal
                        interest = interest1 + interest2 + interest3
                        interest = str(round(interest))
                        self.lineEdit_6.setText(interest)
                if time_in_years > 3 and time_in_years <= 4:
                        interest1 = p*interest_rate
                        p = p + interest1
                        interest2 = p*interest_rate
                        p = p + interest2
                        interest3 = p*interest_rate
                        p = p + interest3
                        interest4 = p*interest_rate*after_decimal
                        interest = interest1 + interest2 + interest3 + interest4
                        interest = str(round(interest))
                        self.lineEdit_6.setText(interest)
                if time_in_years > 4:
                       amount = p * pow( 1+(36/100), time_in_years)
                       interest = amount - p
                       interest = str(round(interest))
                       self.lineEdit_6.setText(interest)
        except Exception as ex:
             messagebox.showerror("Error",f"{str(ex)}")

        finally:
                if self.con.is_connected():
                        mycursor.close()
                        self.con.close()
    
    #function to remove a record from the database
    def remove_record(self):
        user_response = messagebox.askyesno("Removing Record", "Confirm Removing Record")
        if user_response:
                try:
                
                        self.call()
                        if self.lineEdit_6.text == "":
                                messagebox.showerror("Error","Interst is required")
                        else:
                                interest = self.lineEdit_6.text()
                                id = self.user_id
                                try:
                                        utc_now = datetime.utcnow()
                                        tz = pytz.timezone('Asia/Kolkata')
                                        local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
                                        current_date = local_now.strftime("%Y-%m-%d")
                                        mycursor = self.con.cursor()
                                        query = f'select deposit from all_records where user_id = {id}'
                                        mycursor.execute(query)
                                        deposit_amt = mycursor.fetchone()
                                        deposit_amt = deposit_amt[0]
                                        if deposit_amt != None:
                                                deposit_amt = int(deposit_amt)
                                                query = '''UPDATE daily_assessment
                                                SET deposit_debit = COALESCE(deposit_debit, 0) + %s
                                                WHERE date = %s;'''
                                                values = (deposit_amt, current_date)
                                                mycursor.execute(query, values)
                                                self.con.commit()
                                        query = '''INSERT INTO removed_records (user_id, amount, name, father_name, location, Date, Type, Weight) 
                                                SELECT user_id, amount, name, father_name, location, Date, Type, Weight 
                                                FROM all_records 
                                                WHERE user_id = %s;'''
                                        values = (id,)
                                        mycursor.execute(query, values)
                                        query = "DELETE FROM fingerprint_table WHERE user_id = %s;"
                                        mycursor.execute(query, values)
                                        query = "DELETE FROM all_records WHERE user_id = %s;"
                                        mycursor.execute(query, values)
                                        query = "UPDATE removed_records SET interest = %s WHERE user_id = %s"
                                        values = (interest, id)
                                        mycursor.execute(query, values)
                                        self.con.commit()
                                        messagebox.showinfo("Success!","Data Removed")
                                        self.lineEdit_5.clear()
                                        self.lineEdit_6.clear()
                                        self.label_4.setStyleSheet("QPushButton {\n"
"    background-color: rgb(18,18,18);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
                                        self.tableWidget_exist_5.setRowCount(0)
                                except mysql.connector.Error as error:
                                        messagebox.showerror("Error",f"{str(error)}")
                                finally:
                                        if self.con.is_connected():
                                                self.con.close()
                except Exception as ex:
                        messagebox.showerror("Error",f"{str(ex)}")
        else:
               pass

    #function to delete a record from the database 
    def delete_record(self):
        user_response = messagebox.askyesno("Deleting Record", "Confirm Deleting Record")
        if user_response:
           self.call()
           try:
                mycursor = self.con.cursor()
                id = self.user_id
                id = int(id)
                query = f'delete from fingerprint_table where user_id = {id}'
                mycursor.execute(query)
                self.con.commit()
                query = f'delete from all_records where user_id = {id}'
                mycursor.execute(query)
                self.con.commit()
                messagebox.showinfo("Success","Data deleted")
                self.label_4.setStyleSheet("QPushButton {\n"
"    background-color: rgb(18,18,18);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
                self.lineEdit_5.clear()
                self.lineEdit_6.clear()
                self.tableWidget_exist_5.setRowCount(0)
           except Exception as ex:
                  messagebox.showerror("Error",f"{str(ex)} ")
        else:
                pass

    #function for searching records to add deposit
    def search_deposit(self):
        self.tableWidget_5.setRowCount(0)
        current = self.comboBox_4.currentText()
        self.call()
        mycursor = self.con.cursor()
        try:
                if current == "Fingerprint":
                        # Capture the template to match
                        res = requests.post('https://localhost:8003/mfs100/capture', data={
                                "Quality": 60,
                                "TimeOut": 10
                        }, verify=False)
                        isoTemplateToMatch = res.json()['IsoTemplate']
                        
                        query = "SELECT fingerprint_data FROM fingerprint_table;"
                        mycursor.execute(query)
                        result = mycursor.fetchall()
                        
                        ilist = []
                        
                        # Use joblib to parallelize fingerprint matching
                        num_jobs = 30
                        parallel = joblib.Parallel(n_jobs=num_jobs, backend="threading")  # Use threading backend for PyQt
                        fingerprint_matches = parallel(
                                joblib.delayed(fingerprint_match)(isoTemplateToMatch, i[0], mycursor) for i in result
                        )
                        
                        # Collect the matching user IDs
                        ilist = [id for id in fingerprint_matches if id is not None]
                        if len(ilist) == 0:
                               messagebox.showinfo("Oops!","No Record Found")
                        else:
                                user_ids_str = ",".join(str(user_id) for user_id in ilist)
                                query = f"SELECT * FROM all_records WHERE user_id IN ({user_ids_str})"
                                mycursor.execute(query)
                elif current == "Name": 
                        name = self.lineEdit_7.text()
                        if name == "":
                               messagebox.showerror("Error","Please enter Name")
                        else:
                                name = name[0].upper() + name[1:]
                                query = "SELECT * FROM all_records WHERE name = %s"
                                values = (name,)
                                mycursor.execute(query, values)
                elif current == "Location": 
                        location = self.lineEdit_7.text()
                        if location == "":
                               messagebox.showerror("Error","Please enter Location")
                        else:
                                location = location[0].upper() + location[1:]
                                query = "SELECT * FROM all_records WHERE location = %s"
                                values = (location,)
                                mycursor.execute(query, values)
                else:
                        messagebox.showerror("Error","Something Unexpected Occur")
                result = mycursor.fetchall()
                if len(result) == 0:
                        messagebox.showinfo("Oops!","No Record Found")
                else:
                        self.tableWidget_5.setRowCount(0)                            
                        for row_number, row_data in enumerate(result):
                                        self.tableWidget_5.insertRow(row_number)                               
                                        for column_number, data in enumerate(row_data):
                                                item = QTableWidgetItem(str(data))
                                                item.setForeground(QColor(255, 255, 255))
                                                self.tableWidget_5.setItem(row_number,
                                                                       column_number, item)
                        self.tableWidget_5.itemClicked.connect(self.extract_id)       
        except Exception as ex:
                if str(ex) == "'IsoTemplate'":
                        messagebox.showerror("Error", "Connect The Scanner")
                else:
                        messagebox.showerror("Error",f"{str(ex)}")
        finally:
                if self.con.is_connected():
                        mycursor.close()
                        self.con.close()
    
    #function to add deposit to a record in database with current date fetched automatically
    def add_deposit(self):
        try:
            self.call()
            id = int(self.id)
            utc_now = datetime.utcnow()
            tz = pytz.timezone('Asia/Kolkata')
            local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
            date = local_now.strftime("%Y-%m-%d")
            mycursor = self.con.cursor()
            deposit = int(self.lineEdit_8.text())
            query = f'''UPDATE all_records
                        SET deposit = IFNULL(deposit, 0) + {deposit},
                        deposit_date = "{date}"
                        WHERE user_id = {id};'''
            mycursor.execute(query)
            self.con.commit()
            mycursor.close()
            messagebox.showinfo("Success","Deposit Added Successfully")
            self.lineEdit_7.clear()
            self.lineEdit_8.clear()
            self.tableWidget_5.setRowCount(0)
            query = f"SELECT * FROM all_records WHERE user_id = {id}"
            mycursor = self.con.cursor()
            mycursor.execute(query)
            result = mycursor.fetchall()
            for row_number, row_data in enumerate(result):
                self.tableWidget_5.insertRow(row_number)                           
                for column_number, data in enumerate(row_data):
                        item = QTableWidgetItem(str(data))
                        item.setForeground(QColor(255, 255, 255))
                        self.tableWidget_5.setItem(row_number, column_number, item)
            self.con.commit()
        except Exception as ex:
            messagebox.showerror("Error",f"{str(ex)}")
            traceback.print_exc()

    #function to search records to view existing records in the database
    def search_view(self):
        current = self.comboBox_removed_3.currentText()
        self.call()
        mycursor = self.con.cursor()
        try:   
                if current == "Search By":
                        messagebox.showerror("Error","PLease choose either name,location or date")
                elif current == "By Location":
                        if self.lineEdit_removed_3.text() == "":
                              messagebox.showerror("Error","Please enter location")
                        else:
                                location = self.lineEdit_removed_3.text()
                                query = "SELECT * FROM all_records WHERE location = %s"
                                values = (location,)
                                mycursor.execute(query, values)
                elif current == "By Date":
                        if self.lineEdit_removed_3.text() == "":
                                messagebox.showerror("Error","Please enter date")
                        else:
                                date = self.lineEdit_removed_3.text()
                                query = "SELECT * FROM all_records WHERE date = %s"
                                values = (date,)
                                mycursor.execute(query, values)
                elif current == "By Name": 
                        if self.lineEdit_removed_3.text() == "":
                              messagebox.showerror("Error","Please enter Name")
                        else:
                                name = self.lineEdit_removed_3.text()
                                query = "SELECT * FROM all_records WHERE name = %s"
                                values = (name,)
                                mycursor.execute(query, values)
                else:
                        messagebox.showerror("Error","Something Unexpected Occur")

                result = mycursor.fetchall()
                if len(result) == 0:
                        self.lineEdit_removed_3.clear()
                        self.tableWidget_removed_9.setRowCount(0)
                        messagebox.showinfo("Oops!","No Record Found")
                else:   
                        self.tableWidget_removed_9.setRowCount(0)
                
                        for row_number, row_data in enumerate(result):
                                self.tableWidget_removed_9.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                        item = QTableWidgetItem(str(data))
                                        item.setForeground(QColor(255, 255, 255))
                                        self.tableWidget_removed_9.setItem(row_number,
                                        column_number, item)    
        except Exception as e:
                messagebox.showerror("Error",f"{str(e)}")
        finally:
                if self.con.is_connected():
                        self.con.close()

    #function to search all the removed records from the database
    def search_removed(self):
        current = self.comboBox_removed_4.currentText()
        self.call()
        mycursor = self.con.cursor()
        try: 
                if current == "Search By":
                        messagebox.showerror("Error","PLease choose either name,location or date")
                elif current == "By Location":
                        if self.lineEdit_removed_4.text() == "":
                              messagebox.showerror("Error","Please enter location")
                        else:
                                location = self.lineEdit_removed_4.text()
                                query = "SELECT * FROM removed_records WHERE location = %s"
                                values = (location,)
                                mycursor.execute(query, values)
                elif current == "By Date":
                        if self.lineEdit_removed_4.text() == "":
                              messagebox.showerror("Error","Please enter date")
                        else:
                                date = self.lineEdit_removed_4.text()
                                query = "SELECT * FROM removed_records WHERE removed_date = %s"
                                values = (date,)
                                mycursor.execute(query, values)
                elif current == "By Name": 
                        if self.lineEdit_removed_4.text() == "":
                              messagebox.showerror("Error","Please enter Name")
                        else:
                                name = self.lineEdit_removed_4.text()
                                query = "SELECT * FROM removed_records WHERE name = %s"
                                values = (name,)
                                mycursor.execute(query, values)
                else:
                        messagebox.showerror("Error","Something Unexpected Occur")
                result = mycursor.fetchall()
                if len(result) == 0:
                        self.lineEdit_removed_4.clear()
                        self.tableWidget_removed_10.setRowCount(0)
                        messagebox.showinfo("Oops!","No Record Found")
                else:
                        self.tableWidget_removed_10.setRowCount(0)
                        for row_number, row_data in enumerate(result):
                                self.tableWidget_removed_10.insertRow(row_number)
                                for column_number, data in enumerate(row_data):
                                        item = QTableWidgetItem(str(data))
                                        item.setForeground(QColor(255, 255, 255))
                                        self.tableWidget_removed_10.setItem(row_number,
                                        column_number, item)
                
        except Exception as e:
                        messagebox.showerror("Error",f"{str(e)}")
        finally:
                if self.con.is_connected():
                        self.con.close()

#-------------------------------File Handling Functionalities--------------------------------
        ### 1. generate Daily assessment Report
        ### 2. save daily assessment report in pre specified location
        ### 3. view saved reports by entering the particular date
        ### 4. Function to backup mysql database
        ### 5. function to view accounting statements
        ### 6. function to save accounting statements as pdf

    #function to generate daily assessment report
    def generate_report(self):
        try:
                self.lineEdit.clear()
                self.call()
                utc_now = datetime.utcnow()
                tz = pytz.timezone('Asia/Kolkata')
                local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
                date = local_now.strftime("%Y-%m-%d")
                mycursor = self.con.cursor()
                # Executing query for total investment
                query = f'select sum(amount) from all_records where date = "{date}" '
                mycursor.execute(query)
                investment = mycursor.fetchone()
                self.investment = str(investment[0])
                if self.investment == "None":
                       self.investment = int(0)
                else:
                       self.investment = int(investment[0])
                # Query for returns
                query = f'select sum(amount+interest) from removed_records where removed_date = "{date}";'
                mycursor.execute(query)
                returns = mycursor.fetchone()
                self.returns = str(returns[0])
                if self.returns == "None":
                       self.returns = int(0)
                else:
                       self.returns = int(returns[0])
                # Query for added cash
                query = f'select added_cash from daily_assessment where date = "{date}" '
                mycursor.execute(query)
                added_cash = mycursor.fetchone()
                self.added_cash = str(added_cash[0])
                if self.added_cash == "None":
                       self.added_cash = int(0)
                else:
                       self.added_cash = int(added_cash[0])
                # Query for removed cash
                query = f'select removed_cash from daily_assessment where date = "{date}" '
                mycursor.execute(query)
                removed_cash = mycursor.fetchone()
                self.removed_cash = str(removed_cash[0])
                if self.removed_cash == "None":
                       self.removed_cash = int(0)
                else:
                       self.removed_cash = int(removed_cash[0])
                # Query for deposit debit
                query = f'select deposit_debit from daily_assessment where date = "{date}" '
                mycursor.execute(query)
                deposit_debit = mycursor.fetchone()
                self.deposit_debit = str(deposit_debit[0])
                if self.deposit_debit == "None":
                       self.deposit_debit = int(0)
                else:
                       self.deposit_debit = int(deposit_debit[0])
                #query for deposit credit
                query = f'select sum(deposit) from all_records where deposit_date = "{date}" '
                mycursor.execute(query)
                deposit_credit = mycursor.fetchone()
                self.deposit_credit = str(deposit_credit[0])
                if self.deposit_credit == "None":
                       self.deposit_credit = int(0)
                else:
                       self.deposit_credit = int(deposit_credit[0])
                #query for total cash balance
                query = f'SELECT DATE_SUB("{date}", INTERVAL 1 DAY) AS PreviousDate;'
                mycursor.execute(query)
                previous_date = mycursor.fetchone()
                previous_date = str(previous_date[0])
                query = f'select count(*) from daily_assessment where date = "{previous_date}"'
                mycursor.execute(query)
                cash_balance = mycursor.fetchone()
                cash_balance = str(cash_balance[0])
                if cash_balance != "1":
                       self.cash_balance = int(0)
                else:
                       query = f'select left_cash from daily_assessment where date = "{previous_date}"'
                       mycursor.execute(query)
                       cash_balance = mycursor.fetchone()
                       cash_balance_str = str(cash_balance)
                       if cash_balance_str[1:5] == "None":
                              self.cash_balance = int(0)
                       else:
                                self.cash_balance = int(cash_balance[0])
                # Final Cash Balance
                left_cash = self.added_cash+self.cash_balance +self.returns+self.deposit_credit-self.removed_cash-self.investment-self.deposit_debit
                self.left_cash = left_cash
                query = f'update daily_assessment set left_cash = {self.left_cash} where date = "{date}"'
                mycursor.execute(query)
                self.con.commit()
                report_template = (
            "<pre>"
            "Daily Assessment Report\n"
            "============================\n"
            "Cash Summary\n"
            "----------------------------\n"
            "Cash Balance:      {cash_balance}\n"
            "Added Cash:        {added_cash}\n"
            "Removed Cash:     ({removed_cash})\n"
            "============================\n"
            "Investment and Returns\n"
            "----------------------------\n"
            "Investment:        ({investment})\n"
            "Returns:            {returns}\n"
            "============================\n"
            "Deposit\n"
            "----------------------------\n"
            "Deposit (Cr.):      {deposit_credit}\n"
            "Deposit (Dr.):     ({deposit_debit})\n"
            "============================\n"
            "Total Cash Left:   {left_cash}\n"
            "</pre>"
        ).format(cash_balance = self.cash_balance,
                added_cash = self.added_cash,
                removed_cash = self.removed_cash,
                investment = self.investment,
                returns = self.returns,
                deposit_credit = self.deposit_credit,
                deposit_debit = self.deposit_debit,
                left_cash = self.left_cash)

                # Set the report text in the QTextEdit with HTML content
                self.plainTextEdit.setHtml(report_template)
        except Exception as ex:
                messagebox.showerror("Error",f"{str(ex)}")

    #function to save the report generated above
    def save_text(self):
        try:
                # Get the text from the QPlainTextEdit
                text = self.plainTextEdit.toPlainText()
                if text == "":
                       messagebox.showerror("Error","First Generate the Report")
                else:
                        available_drive_letters = self.get_available_drive_letter()
                        preferred_drive_letters = ["D", "E", "H"]
                        usb_drive_path = None
                        for letter in preferred_drive_letters:
                                if letter in available_drive_letters:
                                        usb_drive_path = f"{letter}:\\records\\"
                                        break
                
                        if usb_drive_path is None:
                                messagebox.showerror("Error", "No available USB drive found.")
                                return

                        # Set the file name to the current date
                        file_name = datetime.now().strftime("%d%m%Y") + ".txt"
                        file_path = os.path.join(usb_drive_path, file_name)

                        # Save the PDF to the file
                        with open(file_path, 'w') as file:
                                file.write(text)
                        messagebox.showinfo("Success!!",f"File Stored Successfully at {str(file_path)}")
        except Exception as ex:
                messagebox.showerror("Error",f"{str(ex)}")

    #function to view the saved report in plain text area
    def view_text(self):
        try:
                file_name = self.lineEdit.text()
                if file_name == "location":
                       self.call()
                       mycursor = self.con.cursor()
                       query = "select distinct(location) from all_records order by location"
                       mycursor.execute(query)
                       results = mycursor.fetchall()
                       text = ""
                       for result in results:
                                location = result[0] 
                                text += location + "\n" 

                       self.plainTextEdit.setPlainText(text)
                elif file_name == "type":
                       self.call()
                       mycursor = self.con.cursor()
                       query = "select distinct(type) from all_records order by type"
                       mycursor.execute(query)
                       results = mycursor.fetchall()
                       text = ""
                       for result in results:
                                location = result[0] 
                                text += location + "\n" 

                       self.plainTextEdit.setPlainText(text)

                else:
                        # Create a "records" folder on the desktop if it doesn't exist
                        available_drive_letters = self.get_available_drive_letter()
                        preferred_drive_letters = ["D", "E", "H","A","F","B"]
                        usb_drive_path = None
                        for letter in preferred_drive_letters:
                                if letter in available_drive_letters:
                                        usb_drive_path = f"{letter}:\\"
                                        break
                
                        if usb_drive_path is None:
                                messagebox.showerror("Error", "No available USB drive found.")
                                return
                        records_folder_path = os.path.join(usb_drive_path, "records")
                        file_name = self.lineEdit.text()
                        if file_name == "":
                                messagebox.showerror("Error","Please choose date")

                        else:
                                txt_path = fr"{records_folder_path}\{file_name}.txt"

                                if txt_path:
                                        with open(txt_path, 'r') as file:
                                                text = file.read()
                                                self.plainTextEdit.setPlainText(text)
                                                self.plainTextEdit.setStyleSheet("font: 18pt \"Segoe UI\";\n"
                                                "border:none;\n"
                                                "color: rgb(200,200,200);")

        except Exception as ex:
               messagebox.showerror("Error",f"{str(ex)}")

    #function to backup the mysql database    
    def backup_sql(self):
        db_host = "localhost"
        db_user = "root"
        db_password = "akshat"
        db_name = "loan_management"
        mysqldump_path = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe"
        
        available_drive_letters = self.get_available_drive_letter()
        preferred_drive_letters = ["D", "E", "H"]
        usb_drive_path = None
        for letter in preferred_drive_letters:
            if letter in available_drive_letters:
                usb_drive_path = f"{letter}:\\"
                break
    
        if usb_drive_path is None:
            messagebox.showerror("Error", "No available USB drive found.")
            return
    
        backup_file_path = os.path.join(usb_drive_path, "backup.sql")
        os.environ["MYSQL_PWD"] = db_password
        mysqldump_cmd = [
            mysqldump_path,
            "--host=" + db_host,
            "--user=" + db_user,
            db_name
        ]
        
        try:
            with open(backup_file_path, "w") as backup_file:
                subprocess.run(mysqldump_cmd, stdout=backup_file)
            messagebox.showinfo("Success", f"Backup created at: {str(backup_file_path)}")
        except Exception as ex:
            messagebox.showerror("Error", f"{str(ex)}")
    
    #function to generate report of the accounts section
    def generate_report1(self):
        try:
                self.call()
                mycursor = self.con.cursor()
                current = self.comboBox_2.currentText()
                from_date = self.dateEdit.date().toString("yyyy-MM-dd")
                to_date = self.dateEdit_2.date().toString("yyyy-MM-dd")
                print(to_date)

                if current == "Investment":                                                     
                        # Modify the SQL query to match your specific query
                        query1 = f"""SELECT SUM(total_amount) AS combined_sum
FROM (
    SELECT SUM(amount) AS total_amount FROM all_records WHERE date BETWEEN "{from_date}" AND "{to_date}"
    UNION ALL
    SELECT SUM(amount) AS total_amount FROM removed_records WHERE date BETWEEN "{from_date}" AND "{to_date}"
) AS combined_records;
"""
                        mycursor.execute(query1)
                        total_in = mycursor.fetchone()
                        total_in = str(total_in[0])
                        total_in = self.format_indian_number(total_in)
                        self.lineEdit_2.setText(f"{total_in}")
                        self.label_3.setText(f"Investment from {from_date} to {to_date}")
                        query = f"""
                        SELECT date, SUM(amount) AS total_amount
                        FROM (
                        SELECT date, amount FROM all_records
                        UNION ALL
                        SELECT date, amount FROM removed_records
                        ) AS combined_records
                        WHERE date BETWEEN "{from_date}" AND "{to_date}"
                        GROUP BY date
                        ORDER BY date;
                        """

                elif current == "Returns":                                                     
                        # Modify the SQL query to match your specific query
                        query1 = f"""select sum(amount+interest) from removed_records
                        WHERE removed_date BETWEEN "{from_date}" AND "{to_date}" """
                        mycursor.execute(query1)
                        total_re = mycursor.fetchone()
                        total_re = str(total_re[0])
                        total_re = self.format_indian_number(total_re)
                        self.lineEdit_2.setText(f"{total_re}")
                        self.label_3.setText(f"Returns from {from_date} to {to_date}")
                        query = f"""
                        SELECT removed_date, SUM(amount+interest) as "amount"
                        FROM removed_records
                        WHERE removed_date BETWEEN "{from_date}" AND "{to_date}"
                        GROUP BY removed_date
                        order by removed_date
                        """

                elif current == "Interest":                                                     
                        # Modify the SQL query to match your specific query
                        query1 = f"""select sum(interest) from removed_records
                        WHERE removed_date BETWEEN "{from_date}" AND "{to_date}" """
                        mycursor.execute(query1)
                        total_te = mycursor.fetchone()
                        total_te = str(total_te[0])
                        total_te = self.format_indian_number(total_te)
                        self.lineEdit_2.setText(f"{total_te}")
                        self.label_3.setText(f"Interest Earned from {from_date} to {to_date}")
                        query = f"""
                        SELECT removed_date, SUM(interest) as "amount"
                        FROM removed_records
                        WHERE removed_date BETWEEN "{from_date}" AND "{to_date}"
                        GROUP BY removed_date
                        order by removed_date
                        """

                mycursor.execute(query)
                data = mycursor.fetchall()

                self.model.clear()
                self.model.setHorizontalHeaderLabels(["Date", "Amount"])
                for row, item in enumerate(data):
                        date_item = QStandardItem(item[0].strftime("%Y-%m-%d"))
                        amount_item = QStandardItem(str(item[1]))
                        self.model.appendRow([date_item, amount_item])


        except Exception as ex:
                print(ex)
                messagebox.showerror("Error",ex)

        finally:
                mycursor.close()
                self.con.close()

    #function to save the generated report as a pdf in specified location
    def save_as_pdf(self):
        from fpdf import FPDF 
        try:
                current = self.comboBox_2.currentText()
                from_date = self.dateEdit.date().toString("yyyy-MM-dd")
                to_date = self.dateEdit_2.date().toString("yyyy-MM-dd")
                amount_pdf = self.lineEdit_2.text() 
                class CustomPDF(FPDF):
                        def header(self):
                                # Add your firm's name and logo here
                                self.set_font("Arial", "B", 30)
                                self.set_xy(75,17) 
                                self.cell(0, 20, "LoanMate Accounts")
                                
                                # Get the Y position after adding the title
                                title_y = self.get_y()
                                
                                self.ln(15)
                                pixmap = QPixmap(":/icons/resources/images/loanmate1.png")  # Replace with your resource path
                                pixmap = pixmap.scaled(QSize(250, 400))  # Scale the logo as needed

                                # Convert QPixmap to QImage
                                image = pixmap.toImage()

                                # Save the QImage to a temporary file (assuming PNG format)
                                temp_image_path = "temp_image.png"
                                image.save(temp_image_path, "PNG")

                                # Add the logo to the PDF using image()
                                self.image(temp_image_path, x=10, y=5, w=50, h=40)
                                os.remove(temp_image_path)
                                
                                # Calculate the X and Y positions for the underline
                                underline_x1 = self.l_margin
                                underline_x2 = self.w - self.r_margin
                                underline_y = title_y + 25  # Adjust this value to control the underline's position
                                
                                # Draw the underline
                                self.set_draw_color(0, 0, 0)  # Set the line color to black
                                self.line(underline_x1, underline_y, underline_x2, underline_y)
                                self.ln(10) 

                        def chapter_title(self, title):
                                # Add a heading for the table
                                self.set_font("Arial", "B", 12)
                                self.cell(0, 10, title, ln=True)
                                self.ln(5)  # Move down by 10 units (adjust as needed)

                        def footer(self):
                                # Add a footer note here
                                self.set_y(-15)
                                self.set_font("Arial", "I", 8)
                                self.cell(0, 10, f"Note:- This is a computer generated statement of Total {current} over a period of time. This is saved automatically in Available USB Drive", align="C")
                # Create a "records" folder on the desktop if it doesn't exist
                available_drive_letters = self.get_available_drive_letter()
                preferred_drive_letters = ["D", "E", "H","A","F","B"]
                usb_drive_path = None
                for letter in preferred_drive_letters:
                        if letter in available_drive_letters:
                                usb_drive_path = f"{letter}:\\"
                                break
                if usb_drive_path is None:
                        messagebox.showerror("Error", "No available USB drive found.")
                        return
                statements_folder_path = os.path.join(usb_drive_path, "statement")
                # Construct the PDF file path (e.g., ~/Desktop/account_summary.pdf)
                pdf_filename = os.path.join(statements_folder_path, f"{current[0:3]}-{from_date}-{to_date}.pdf")
                pdf = CustomPDF()
                pdf.add_page()
                pdf.ln(5) 
                # Add a title to the PDF 
                pdf.set_font("Arial", "B", 16)
                pdf.cell(200, 20, txt=f"Total {current} from {from_date} to {to_date}", ln=True, align='C')
                pdf.ln(0) 
                # Add headers for "Date" and "Amount"
                pdf.set_font("Arial", "B", size=12)
                pdf.cell(95, 10, txt="Date", border=1, align='C')
                pdf.cell(90, 10, txt="Amount", border=1, ln=True, align='C')
                # Export table data to PDF
                for row in range(self.model.rowCount()):
                        if pdf.get_y() > 190:
                                pdf.add_page()
                                pdf.set_font("Arial", "B", 16)
                                pdf.cell(200, 20, txt="", ln=True, align='C')
                                pdf.ln(0)
                                pdf.set_font("Arial", "B", size=12)
                                pdf.cell(95, 10, txt="Date", border=1, align='C')
                                pdf.cell(90, 10, txt="Amount", border=1, ln=True, align='C')

                        date_item = self.model.item(row, 0)
                        amount_item = self.model.item(row, 1)

                        if date_item and amount_item:
                                date = date_item.text()
                                amount = amount_item.text()
                                pdf.set_font("Arial", size=12)
                                pdf.cell(95, 10, txt=date, border=1, align='C')
                                pdf.cell(90, 10, txt=amount, border=1, ln=True, align='C')
                if current == "Interest":
                        pdf.chapter_title(f"Total {current} Earned from {from_date} to {to_date} = {amount_pdf}.")
                else:
                       pdf.chapter_title(f"Total {current} from {from_date} to {to_date} = {amount_pdf}.")

                # Save the PDF to the desktop
                pdf.output(pdf_filename)

                messagebox.showinfo("Success",f"PDF saved as {pdf_filename}")
        except Exception as ex:
               messagebox.showerror("Error",ex)
#xx--------------------------Defining BackEnd Function Completed-------------------------xx

#ffunction to set up ui for this application
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 700)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("://icons/resources/icons/download.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolBar = QtWidgets.QFrame(self.centralwidget)
        self.toolBar.setMinimumSize(QtCore.QSize(0, 30))
        self.toolBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.toolBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.toolBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolBar.setObjectName("toolBar")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.toolBar)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.headerFrame = QtWidgets.QFrame(self.toolBar)
        self.headerFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.headerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.headerFrame.setObjectName("headerFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.headerFrame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(218, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.headerFrame)
        self.label.setMinimumSize(QtCore.QSize(200, 0))
        self.label.setStyleSheet("color: rgb(176, 176, 176);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(58, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.userFrame = QtWidgets.QFrame(self.headerFrame)
        self.userFrame.setMinimumSize(QtCore.QSize(400, 30))
        self.userFrame.setMaximumSize(QtCore.QSize(200, 30))
        self.userFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.userFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.userFrame.setObjectName("userFrame")
        self.toggleButton_7 = QtWidgets.QPushButton(self.userFrame)
        self.toggleButton_7.setGeometry(QtCore.QRect(230, 2, 130, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton_7.sizePolicy().hasHeightForWidth())
        self.toggleButton_7.setSizePolicy(sizePolicy)
        self.toggleButton_7.setMinimumSize(QtCore.QSize(130, 26))
        self.toggleButton_7.setMaximumSize(QtCore.QSize(150, 26))
        font = QtGui.QFont()
        font.setBold(True)
        self.toggleButton_7.setFont(font)
        self.toggleButton_7.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("://icons/icons8_multiply.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggleButton_7.setIcon(icon)
        self.toggleButton_7.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_7.setObjectName("toggleButton_7")
        self.toggleButton_11 = QtWidgets.QPushButton(self.userFrame)
        self.toggleButton_11.setGeometry(QtCore.QRect(60, 2, 130, 26))
        self.toggleButton_11.setMinimumSize(QtCore.QSize(130, 26))
        self.toggleButton_11.setMaximumSize(QtCore.QSize(150, 26))
        font = QtGui.QFont()
        font.setBold(True)
        self.toggleButton_11.setFont(font)
        self.toggleButton_11.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("://icons/icons8_plus_math.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggleButton_11.setIcon(icon1)
        self.toggleButton_11.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_11.setObjectName("toggleButton_11")
        self.horizontalLayout_3.addWidget(self.userFrame)
        self.horizontalLayout_2.addWidget(self.headerFrame)
        self.verticalLayout.addWidget(self.toolBar)
        self.Body = QtWidgets.QFrame(self.centralwidget)
        self.Body.setStyleSheet("")
        self.Body.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Body.setObjectName("Body")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Body)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftMenu = QtWidgets.QFrame(self.Body)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftMenu.sizePolicy().hasHeightForWidth())
        self.leftMenu.setSizePolicy(sizePolicy)
        self.leftMenu.setMinimumSize(QtCore.QSize(195, 0))
        self.leftMenu.setMaximumSize(QtCore.QSize(195, 16777215))
        self.leftMenu.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.leftMenu.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.leftMenu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftMenu.setObjectName("leftMenu")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.leftMenu)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_5 = QtWidgets.QLabel(self.leftMenu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(0, 140))
        self.label_5.setStyleSheet("image: url(://icons/resources/images/loanmate1.png);")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.verticalLayout_3.addWidget(self.label_5)
        self.aframe = QtWidgets.QFrame(self.leftMenu)
        self.aframe.setMinimumSize(QtCore.QSize(200, 500))
        self.aframe.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.aframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.aframe.setObjectName("aframe")
        self.dashbtn = QtWidgets.QPushButton(self.aframe)
        self.dashbtn.setGeometry(QtCore.QRect(-2, 18, 200, 45))
        self.dashbtn.setMinimumSize(QtCore.QSize(200, 45))
        self.dashbtn.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.dashbtn.setFont(font)
        self.dashbtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.dashbtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(154, 154, 149);\n"
"    border-left: 0px solid rgb(25, 25, 25);\n"
"    border:2px solid black;\n"
"    text-align: left;\n"
"    padding-right: 5px;\n"
"    padding-bottom: 5px;\n"
"    font:27px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-bottom: 3px solid rgb(255, 85, 0);\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("://icons/icons8_keypad.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dashbtn.setIcon(icon2)
        self.dashbtn.setIconSize(QtCore.QSize(25, 25))
        self.dashbtn.setObjectName("dashbtn")
        self.addbtn = QtWidgets.QPushButton(self.aframe)
        self.addbtn.setGeometry(QtCore.QRect(-2, 77, 200, 45))
        self.addbtn.setMinimumSize(QtCore.QSize(200, 45))
        self.addbtn.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.addbtn.setFont(font)
        self.addbtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.addbtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(154, 154, 149);\n"
"    border:2px solid black;\n"
"    text-align: left;\n"
"    padding-right: 5px;\n"
"    padding-bottom: 5px;\n"
"    font:27px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-bottom: 3px solid rgb(255, 85, 0);\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("://icons/icons8_plus_math.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addbtn.setIcon(icon1)
        self.addbtn.setIconSize(QtCore.QSize(25, 25))
        self.addbtn.setObjectName("addbtn")
        self.removebtn = QtWidgets.QPushButton(self.aframe)
        self.removebtn.setGeometry(QtCore.QRect(-2, 136, 200, 45))
        self.removebtn.setMinimumSize(QtCore.QSize(200, 45))
        self.removebtn.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.removebtn.setFont(font)
        self.removebtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.removebtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(154, 154, 149);\n"
"    border: 2px solid black;\n"
"    text-align: left;\n"
"    padding-right: 5px;\n"
"    padding-bottom: 5px;\n"
"    font:25px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-bottom: 3px solid rgb(255, 85, 0);\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("://icons/icons8_multiply.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removebtn.setIcon(icon)
        self.removebtn.setIconSize(QtCore.QSize(24, 24))
        self.removebtn.setObjectName("removebtn")
        self.depositbtn = QtWidgets.QPushButton(self.aframe)
        self.depositbtn.setGeometry(QtCore.QRect(-2, 195, 200, 45))
        self.depositbtn.setMinimumSize(QtCore.QSize(200, 45))
        self.depositbtn.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.depositbtn.setFont(font)
        self.depositbtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.depositbtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(154, 154, 149);\n"
"    border: 2px solid black;\n"
"    text-align: left;\n"
"    padding-right: 5px;\n"
"padding-bottom: 5px;\n"
"    font:27px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-bottom: 3px solid rgb(255, 85, 0);\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("://icons/icons8_mastercard_credit_card.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.depositbtn.setIcon(icon3)
        self.depositbtn.setIconSize(QtCore.QSize(25, 25))
        self.depositbtn.setObjectName("depositbtn")
        self.viewbtn = QtWidgets.QPushButton(self.aframe)
        self.viewbtn.setGeometry(QtCore.QRect(-2, 254, 200, 45))
        self.viewbtn.setMinimumSize(QtCore.QSize(200, 45))
        self.viewbtn.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.viewbtn.setFont(font)
        self.viewbtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.viewbtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(154, 154, 149);\n"
"    border: 2px solid black;\n"
"    text-align: left;\n"
"    padding-right: 5px;\n"
"padding-bottom: 5px;\n"
"    font:25px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-bottom: 3px solid rgb(255, 85, 0);\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("://icons/icons8_todo_list.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.viewbtn.setIcon(icon4)
        self.viewbtn.setIconSize(QtCore.QSize(25, 25))
        self.viewbtn.setObjectName("viewbtn")
        self.removedbtn = QtWidgets.QPushButton(self.aframe)
        self.removedbtn.setGeometry(QtCore.QRect(-2, 313, 200, 45))
        self.removedbtn.setMinimumSize(QtCore.QSize(200, 45))
        self.removedbtn.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.removedbtn.setFont(font)
        self.removedbtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.removedbtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(154, 154, 149);\n"
"    border: 2px solid black;\n"
"    text-align: left;\n"
"    padding-right: 5px;\n"
"padding-bottom: 5px;\n"
"    font:23px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-bottom: 3px solid rgb(255, 85, 0);\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("://icons/icons8_microsoft_excel.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.removedbtn.setIcon(icon5)
        self.removedbtn.setIconSize(QtCore.QSize(25, 25))
        self.removedbtn.setObjectName("removedbtn")
        self.accountsbtn = QtWidgets.QPushButton(self.aframe)
        self.accountsbtn.setGeometry(QtCore.QRect(-5, 370, 200, 45))
        self.accountsbtn.setMinimumSize(QtCore.QSize(200, 45))
        self.accountsbtn.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.accountsbtn.setFont(font)
        self.accountsbtn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.accountsbtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(154, 154, 149);\n"
"    border: 2px solid black;\n"
"    text-align: left;\n"
"    padding-right: 5px;\n"
"padding-bottom: 5px;\n"
"    font:23px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-bottom: 3px solid rgb(255, 85, 0);\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")     
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("://icons/icons8_receipt.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.accountsbtn.setIcon(icon5)
        self.accountsbtn.setIconSize(QtCore.QSize(25, 25))
        self.accountsbtn.setObjectName("accountsbtn")
        self.verticalLayout_3.addWidget(self.aframe)
        spacerItem2 = QtWidgets.QSpacerItem(20, 271, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.frame_2 = QtWidgets.QFrame(self.leftMenu)
        self.frame_2.setMinimumSize(QtCore.QSize(200, 50))
        self.frame_2.setMaximumSize(QtCore.QSize(200, 50))
        self.frame_2.setStyleSheet("")
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_2)
        self.pushButton.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton.setMaximumSize(QtCore.QSize(200, 45))
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(204, 204, 204);\n"
"    border: none;\n"
"    border-left: 3px solid rgb(25, 25, 25);\n"
"    text-align: left;\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    background-color: rgb(18, 18, 18);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 0, 0);\n"
"}\n"
"\n"
"")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("://icons/icons8_logout_rounded_down.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon6)
        self.pushButton.setIconSize(QtCore.QSize(30, 30))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_3.addWidget(self.frame_2)
        self.horizontalLayout.addWidget(self.leftMenu)
        self.Container = QtWidgets.QFrame(self.Body)
        self.Container.setStyleSheet("background-color: rgb(34, 34, 34);")
        self.Container.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Container.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Container.setObjectName("Container")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.Container)
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.stackedWidget = QtWidgets.QStackedWidget(self.Container)
        self.stackedWidget.setLineWidth(0)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.page)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame = QtWidgets.QFrame(self.page)
        self.frame.setStyleSheet("background-color: rgb(28, 31, 34);")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMinimumSize(QtCore.QSize(1100, 160))
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 230))
        self.frame_4.setStyleSheet("background-color: rgb(18,18,18);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame_10 = QtWidgets.QFrame(self.frame_4)
        self.frame_10.setStyleSheet("QFrame {\n"
"    background-color: rgb(25, 25, 25);\n"
"    border-radius: 15px;\n"
"}\n"
"\n"
"QFrame:hover {\n"
"    border: 1px solid rgb(255, 85, 0);\n"
"}")
        self.frame_10.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_9.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_11 = QtWidgets.QLabel(self.frame_10)
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("QLabel {\n"
"font:20pt;\n"
"    color: rgb(152, 152, 152);\n"
"    border: none;\n"
"}")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_9.addWidget(self.label_11)
        self.total_investment = QtWidgets.QLabel(self.frame_10)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.total_investment.setFont(font)
        self.total_investment.setStyleSheet("QLabel {\n"
                                            "font:15pt;\n"
"    color: rgb(199, 199, 199);\n"
"    border: none;\n"
"}")
        self.total_investment.setAlignment(QtCore.Qt.AlignCenter)
        self.total_investment.setObjectName("total_investment")
        self.verticalLayout_9.addWidget(self.total_investment)
        self.lineEdit_9 = QtWidgets.QLabel(self.frame_10)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_9.setFont(font)
        self.lineEdit_9.setStyleSheet("QLabel {\n"
"    color: rgb(70, 255, 3);\n"
"    border: none;\n"
"}")
        self.lineEdit_9.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.verticalLayout_9.addWidget(self.lineEdit_9)
        self.horizontalLayout_5.addWidget(self.frame_10)
        self.frame_8 = QtWidgets.QFrame(self.frame_4)
        self.frame_8.setStyleSheet("QFrame {\n"
"    background-color: rgb(25, 25, 25);\n"
"    border-radius: 15px;\n"
"}\n"
"\n"
"QFrame:hover {\n"
"    border: 1px solid rgb(255, 85, 0);\n"
"}")
        self.frame_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_7.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_2 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("QLabel {\n"
                                   "font:20pt;\n"
"    color: rgb(152, 152, 152);\n"
"    border: none;\n"
"}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_7.addWidget(self.label_2)
        self.todays_investment = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.todays_investment.setFont(font)
        self.todays_investment.setStyleSheet("QLabel {\n"
                                             "font:15pt;\n"
"    color: rgb(199, 199, 199);\n"
"    border: none;\n"
"}")
        self.todays_investment.setAlignment(QtCore.Qt.AlignCenter)
        self.todays_investment.setObjectName("todays_investment")
        self.verticalLayout_7.addWidget(self.todays_investment)
        self.lineEdit_10 = QtWidgets.QLabel(self.frame_8)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_10.setFont(font)
        self.lineEdit_10.setStyleSheet("QLabel {\n"
"    color: rgb(70, 255, 3);\n"
"    border: none;\n"
"}")
        self.lineEdit_10.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.verticalLayout_7.addWidget(self.lineEdit_10)
        self.horizontalLayout_5.addWidget(self.frame_8)
        self.frame_11 = QtWidgets.QFrame(self.frame_4)
        self.frame_11.setStyleSheet("QFrame {\n"
"    background-color: rgb(25, 25, 25);\n"
"    border-radius: 15px;\n"
"}\n"
"\n"
"QFrame:hover {\n"
"    border: 1px solid rgb(255, 85, 0);\n"
"}")
        self.frame_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_10.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_15 = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("QLabel {\n"
                                    "font:20pt;\n"
"    color: rgb(152, 152, 152);\n"
"    border: none;\n"
"}")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.verticalLayout_10.addWidget(self.label_15)
        self.todays_return = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.todays_return.setFont(font)
        self.todays_return.setStyleSheet("QLabel {\n"
                                         "font:15pt;\n"
"    color: rgb(199, 199, 199);\n"
"    border: none;\n"
"}")
        self.todays_return.setAlignment(QtCore.Qt.AlignCenter)
        self.todays_return.setObjectName("todays_return")
        self.verticalLayout_10.addWidget(self.todays_return)
        self.lineEdit_11 = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.lineEdit_11.setFont(font)
        self.lineEdit_11.setStyleSheet("QLabel {\n"
"    color: rgb(70, 255, 3);\n"
"    border: none;\n"
"}")
        self.lineEdit_11.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.verticalLayout_10.addWidget(self.lineEdit_11)
        self.horizontalLayout_5.addWidget(self.frame_11)
        self.frame_9 = QtWidgets.QFrame(self.frame_4)
        self.frame_9.setStyleSheet("QFrame {\n"
"    background-color: rgb(25, 25, 25);\n"
"    border-radius: 15px;\n"
"}\n"
"\n"
"QFrame:hover {\n"
"    border: 1px solid rgb(255, 85, 0);\n"
"}")
        self.frame_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_8.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("QLabel {\n"
                                   "font:20pt;\n"
"    color: rgb(152, 152, 152);\n"
"    border: none;\n"
"}")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_8.addWidget(self.label_7)
        self.todays_interest = QtWidgets.QLabel(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.todays_interest.setFont(font)
        self.todays_interest.setStyleSheet("QLabel {\n"
                                           "font:15pt;\n"
"    color: rgb(199, 199, 199);\n"
"    border: none;\n"
"}")
        self.todays_interest.setAlignment(QtCore.Qt.AlignCenter)
        self.todays_interest.setObjectName("todays_interest")
        self.verticalLayout_8.addWidget(self.todays_interest)
        self.horizontalLayout_5.addWidget(self.frame_9)
        self.horizontalLayout_6.addWidget(self.frame_4)
        self.verticalLayout_6.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(self.page)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 800))
        self.frame_3.setStyleSheet("background-color: rgb(18, 18, 18);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_7.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setMinimumSize(QtCore.QSize(600, 0))
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_6.setStyleSheet("background-color: rgb(18, 18, 18);")
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_13.setContentsMargins(10, 0, 10, 0)
        self.verticalLayout_13.setSpacing(2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.frame_16 = QtWidgets.QFrame(self.frame_6)
        self.frame_16.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_16.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_16.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.frame_16.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_16)
        self.horizontalLayout_11.setContentsMargins(5, 0, 5, 0)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_22 = QtWidgets.QLabel(self.frame_16)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label_22.setFont(font)
        self.label_22.setStyleSheet("color: rgb(152, 152, 152);")
        self.label_22.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_11.addWidget(self.label_22)
        self.comboBox = QtWidgets.QComboBox(self.frame_16)
        self.comboBox.setMaximumSize(QtCore.QSize(220, 16777215))
        self.comboBox.setStyleSheet("font: 15pt \"Segoe UI\";\n"
"border-radius:3px;\n"
"color: rgb(200,200,200);\n"
"border: 2px solid Black;\n"
"")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_11.addWidget(self.comboBox)
        self.verticalLayout_13.addWidget(self.frame_16)
        self.dataFrame = QtWidgets.QFrame(self.frame_6)
        self.dataFrame.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.dataFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dataFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dataFrame.setObjectName("dataFrame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.dataFrame)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_5 = QtWidgets.QFrame(self.dataFrame)
        self.frame_5.setStyleSheet("border:none;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_198 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_198.setObjectName("verticalLayout_198")
        self.frame_342 = QtWidgets.QFrame(self.frame_5)
        self.frame_342.setStyleSheet("border: none;")
        self.frame_342.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_342.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_342.setObjectName("frame_342")
        self.verticalLayout_199 = QtWidgets.QVBoxLayout(self.frame_342)
        self.verticalLayout_199.setObjectName("verticalLayout_199")
        self.verticalLayout_198.addWidget(self.frame_342)
        # Create the chart
        self.chart = QChart()
        self.chart.setBackgroundBrush(QColor(25, 25, 25))

        # Create the chart view
        self.chart_view = QChartView(self.chart)
        self.chart_view.setStyleSheet("border: none;")

        # Populate the chart with data
        self.populate_chart()

        # Add the chart view to the existing frame
        self.verticalLayout_199.addWidget(self.chart_view)

        self.verticalLayout_5.addWidget(self.frame_5)
        self.verticalLayout_13.addWidget(self.dataFrame)
        self.horizontalLayout_7.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_3)
        self.frame_7.setMinimumSize(QtCore.QSize(450, 0))
        self.frame_7.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_7.setStyleSheet("background-color: rgb(7, 31, 62);")
        self.frame_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.frame_12 = QtWidgets.QFrame(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy)
        self.frame_12.setMinimumSize(QtCore.QSize(450, 0))
        self.frame_12.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_12.setStyleSheet("background-color: rgb(7, 31, 62);")
        self.frame_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.frame_12)
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.frame_15 = QtWidgets.QFrame(self.frame_12)
        self.frame_15.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_15.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_15.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.frame_17 = QtWidgets.QFrame(self.frame_15)
        self.frame_17.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_17.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_17.setStyleSheet("background-color: rgb(25, 25, 25);\n"
"border-bottom:1px solid black;\n"
"")
        self.frame_17.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_23 = QtWidgets.QLabel(self.frame_17)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        self.label_23.setFont(font)
        self.label_23.setStyleSheet("color: rgb(152, 152, 152);\n"
"border-bottom-color: rgb(18, 18, 18);\n"
"border-bottom:1px solid black;")
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_13.addWidget(self.label_23)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_17)
        self.lineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit.setStyleSheet("QLineEdit {\n"
"font: 14pt \"Segoe UI\";\n"
"color: rgb(250,250,250);\n"
"border:2px solid grey;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setPlaceholderText("Eg: 01012023")
        self.horizontalLayout_13.addWidget(self.lineEdit)
        self.toggleButton_8 = QtWidgets.QPushButton(self.frame_17)
        self.toggleButton_8.setMinimumSize(QtCore.QSize(85, 26))
        self.toggleButton_8.setMaximumSize(QtCore.QSize(85, 26))
        font = QtGui.QFont()
        font.setBold(True)
        self.toggleButton_8.setFont(font)
        self.toggleButton_8.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 1px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("://icons/icons8_save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggleButton_8.setIcon(icon7)
        self.toggleButton_8.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_8.setObjectName("toggleButton_8")
        self.horizontalLayout_13.addWidget(self.toggleButton_8)
        self.horizontalLayout_12.addWidget(self.frame_17)
        self.verticalLayout_17.addWidget(self.frame_15)
        self.frame_18 = QtWidgets.QFrame(self.frame_12)
        self.frame_18.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.frame_18.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_18)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_13 = QtWidgets.QFrame(self.frame_18)
        self.frame_13.setStyleSheet("border:none;")
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_13)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.plainTextEdit = QtWidgets.QTextEdit(self.frame_13)
        self.plainTextEdit.setMinimumSize(QtCore.QSize(0, 240))
        self.plainTextEdit.setStyleSheet("font: 18pt \"Segoe UI\";\n"
"border:none;\n"
"color: rgb(200,200,200);")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setPlainText("Daily Assessment Report!!")
        self.horizontalLayout_9.addWidget(self.plainTextEdit)
        self.verticalLayout_11.addWidget(self.frame_13)
        self.frame_19 = QtWidgets.QFrame(self.frame_18)
        self.frame_19.setStyleSheet("border:none;")
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_19)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame_343 = QtWidgets.QFrame(self.frame_19)
        self.frame_343.setStyleSheet("border:none;")
        self.frame_343.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_343.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_343.setObjectName("frame_343")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_343)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.toggleButton_9 = QtWidgets.QPushButton(self.frame_343)
        self.toggleButton_9.setMinimumSize(QtCore.QSize(90, 26))
        self.toggleButton_9.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.toggleButton_9.setFont(font)
        self.toggleButton_9.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"    padding-right:2px;\n"
"    font:25px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 1px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("://icons/icons8_calendar_1.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggleButton_9.setIcon(icon8)
        self.toggleButton_9.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_9.setObjectName("toggleButton_9")
        self.horizontalLayout_14.addWidget(self.toggleButton_9)
        self.toggleButton_10 = QtWidgets.QPushButton(self.frame_343)
        self.toggleButton_10.setMinimumSize(QtCore.QSize(90, 26))
        self.toggleButton_10.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.toggleButton_10.setFont(font)
        self.toggleButton_10.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"    font:25px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 1px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("://icons/icons8_download.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggleButton_10.setIcon(icon9)
        self.toggleButton_10.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_10.setObjectName("toggleButton_10")
        self.horizontalLayout_14.addWidget(self.toggleButton_10)
        self.toggleButton_12 = QtWidgets.QPushButton(self.frame_343)
        self.toggleButton_12.setMinimumSize(QtCore.QSize(90, 26))
        self.toggleButton_12.setMaximumSize(QtCore.QSize(200, 40))
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(False)
        font.setItalic(False)
        self.toggleButton_12.setFont(font)
        self.toggleButton_12.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"    padding-right:2px;\n"
"    font:25px\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 1px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("://icons/icons8_update_left_rotation.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toggleButton_12.setIcon(icon9)
        self.toggleButton_12.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_12.setObjectName("toggleButton_12")
        self.horizontalLayout_14.addWidget(self.toggleButton_12)
        self.horizontalLayout_8.addWidget(self.frame_343)
        self.verticalLayout_11.addWidget(self.frame_19)
        self.verticalLayout_11.setStretch(0, 8)
        self.verticalLayout_11.setStretch(1, 1)
        self.verticalLayout_17.addWidget(self.frame_18)
        self.verticalLayout_16.addWidget(self.frame_12)
        self.horizontalLayout_7.addWidget(self.frame_7)
        self.horizontalLayout_7.setStretch(0, 2)
        self.horizontalLayout_7.setStretch(1, 1)
        self.verticalLayout_6.addWidget(self.frame_3)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.frame_14 = QtWidgets.QFrame(self.page_2)
        self.frame_14.setStyleSheet("border:none;")
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.frame_307 = QtWidgets.QFrame(self.frame_14)
        self.frame_307.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_307.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"border-radius: 15px;\n"
"border:2px solid white;")
        self.frame_307.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_307.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_307.setObjectName("frame_307")
        self.verticalLayout_181 = QtWidgets.QVBoxLayout(self.frame_307)
        self.verticalLayout_181.setObjectName("verticalLayout_181")
        self.frame_308 = QtWidgets.QFrame(self.frame_307)
        self.frame_308.setStyleSheet("border: none;")
        self.frame_308.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_308.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_308.setObjectName("frame_308")
        self.verticalLayout_182 = QtWidgets.QVBoxLayout(self.frame_308)
        self.verticalLayout_182.setObjectName("verticalLayout_182")
        self.frame_309 = QtWidgets.QFrame(self.frame_308)
        self.frame_309.setStyleSheet("border: none;")
        self.frame_309.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_309.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_309.setObjectName("frame_309")
        self.verticalLayout_183 = QtWidgets.QVBoxLayout(self.frame_309)
        self.verticalLayout_183.setObjectName("verticalLayout_183")
        self.label_92 = QtWidgets.QLabel(self.frame_309)
        self.label_92.setMinimumSize(QtCore.QSize(0, 0))
        self.label_92.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_92.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_92.setStyleSheet("QFrame {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 15px;\n"
"    font: 24pt \"Segoe UI\";\n"
"    font: 9pt \"Segoe UI\";\n"
"    font: 550 35pt \"Segoe UI\";\n"
"    border-bottom: 2px solid white;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"\n"
"")
        self.label_92.setAlignment(QtCore.Qt.AlignCenter)
        self.label_92.setObjectName("label_92")
        self.verticalLayout_183.addWidget(self.label_92)
        self.verticalLayout_182.addWidget(self.frame_309)
        self.verticalLayout_181.addWidget(self.frame_308)
        self.frame_310 = QtWidgets.QFrame(self.frame_307)
        self.frame_310.setStyleSheet("border:none;")
        self.frame_310.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_310.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_310.setObjectName("frame_310")
        self.horizontalLayout_149 = QtWidgets.QHBoxLayout(self.frame_310)
        self.horizontalLayout_149.setObjectName("horizontalLayout_149")
        self.frame_311 = QtWidgets.QFrame(self.frame_310)
        self.frame_311.setStyleSheet("border:none;")
        self.frame_311.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_311.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_311.setObjectName("frame_311")
        self.horizontalLayout_150 = QtWidgets.QHBoxLayout(self.frame_311)
        self.horizontalLayout_150.setObjectName("horizontalLayout_150")
        self.frame_312 = QtWidgets.QFrame(self.frame_311)
        self.frame_312.setStyleSheet("border: none;")
        self.frame_312.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_312.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_312.setObjectName("frame_312")
        self.verticalLayout_184 = QtWidgets.QVBoxLayout(self.frame_312)
        self.verticalLayout_184.setObjectName("verticalLayout_184")
        self.frame_313 = QtWidgets.QFrame(self.frame_312)
        self.frame_313.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_313.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_313.setObjectName("frame_313")
        self.horizontalLayout_151 = QtWidgets.QHBoxLayout(self.frame_313)
        self.horizontalLayout_151.setObjectName("horizontalLayout_151")
        self.label_93 = QtWidgets.QLabel(self.frame_313)
        self.label_93.setStyleSheet("QLabel {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(255,255,255);\n"
"    border-radius: 15px;\n"
"    font: 550 23pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"}\n"
"\n"
"\n"
"")
        
        self.label_93.setAlignment(QtCore.Qt.AlignCenter)
        self.label_93.setObjectName("label_93")
        self.horizontalLayout_151.addWidget(self.label_93)
        self.verticalLayout_184.addWidget(self.frame_313)
        self.frame_314 = QtWidgets.QFrame(self.frame_312)
        self.frame_314.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_314.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_314.setObjectName("frame_314")
        self.verticalLayout_185 = QtWidgets.QVBoxLayout(self.frame_314)
        self.verticalLayout_185.setObjectName("verticalLayout_185")
        self.label_94 = QtWidgets.QLabel(self.frame_314)
        self.label_94.setStyleSheet("QLabel {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(255,255,255);\n"
"    border-radius: 15px;\n"
"    font: 550 19pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"}\n"
"\n"
"\n"
"")
        self.label_94.setAlignment(QtCore.Qt.AlignCenter)
        self.label_94.setObjectName("label_94")
        self.verticalLayout_185.addWidget(self.label_94)
        self.verticalLayout_184.addWidget(self.frame_314)
        self.horizontalLayout_150.addWidget(self.frame_312)
        self.frame_315 = QtWidgets.QFrame(self.frame_311)
        self.frame_315.setStyleSheet("border:none;")
        self.frame_315.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_315.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_315.setObjectName("frame_315")
        self.verticalLayout_186 = QtWidgets.QVBoxLayout(self.frame_315)
        self.verticalLayout_186.setObjectName("verticalLayout_186")
        self.jewellery_2 = QtWidgets.QLineEdit(self.frame_315)
        self.jewellery_2.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.jewellery_2.setObjectName("jewellery_2")
        self.completer_6 = QCompleter()
        self.completer_6.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_6.popup().setStyleSheet("font-size: 30px") 
        self.jewellery_2.setCompleter(self.completer_6)
        # Connect the textChanged signal to your new function
        self.jewellery_2.textChanged.connect(self.update_completer_6_model)
        self.verticalLayout_186.addWidget(self.jewellery_2)
        self.jewellery_3 = QtWidgets.QLineEdit(self.frame_315)
        self.jewellery_3.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.jewellery_3.setObjectName("jewellery_3")
        self.verticalLayout_186.addWidget(self.jewellery_3)
        self.horizontalLayout_150.addWidget(self.frame_315)
        self.horizontalLayout_150.setStretch(0, 1)
        self.horizontalLayout_150.setStretch(1, 1)
        self.horizontalLayout_149.addWidget(self.frame_311)
        self.frame_316 = QtWidgets.QFrame(self.frame_310)
        self.frame_316.setStyleSheet("border:none;")
        self.frame_316.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_316.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_316.setObjectName("frame_316")
        self.horizontalLayout_152 = QtWidgets.QHBoxLayout(self.frame_316)
        self.horizontalLayout_152.setObjectName("horizontalLayout_152")
        self.frame_317 = QtWidgets.QFrame(self.frame_316)
        self.frame_317.setStyleSheet("border: none;")
        self.frame_317.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_317.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_317.setObjectName("frame_317")
        self.verticalLayout_187 = QtWidgets.QVBoxLayout(self.frame_317)
        self.verticalLayout_187.setObjectName("verticalLayout_187")
        self.frame_318 = QtWidgets.QFrame(self.frame_317)
        self.frame_318.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_318.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_318.setObjectName("frame_318")
        self.horizontalLayout_153 = QtWidgets.QHBoxLayout(self.frame_318)
        self.horizontalLayout_153.setObjectName("horizontalLayout_153")
        self.label_95 = QtWidgets.QLabel(self.frame_318)
        self.label_95.setStyleSheet("QLabel {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(255,255,255);\n"
"    border-radius: 15px;\n"
"    font: 550 23pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"}\n"
"\n"
"\n"
"")
        self.label_95.setAlignment(QtCore.Qt.AlignCenter)
        self.label_95.setObjectName("label_95")
        self.horizontalLayout_153.addWidget(self.label_95)
        self.verticalLayout_187.addWidget(self.frame_318)
        self.frame_319 = QtWidgets.QFrame(self.frame_317)
        self.frame_319.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_319.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_319.setObjectName("frame_319")
        self.verticalLayout_188 = QtWidgets.QVBoxLayout(self.frame_319)
        self.verticalLayout_188.setObjectName("verticalLayout_188")
        self.label_96 = QtWidgets.QLabel(self.frame_319)
        self.label_96.setStyleSheet("QLabel {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(255,255,255);\n"
"    border-radius: 15px;\n"
"    font: 550 23pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"}\n"
"\n"
"\n"
"")
        self.label_96.setAlignment(QtCore.Qt.AlignCenter)
        self.label_96.setObjectName("label_96")
        self.verticalLayout_188.addWidget(self.label_96)
        self.verticalLayout_187.addWidget(self.frame_319)
        self.horizontalLayout_152.addWidget(self.frame_317)
        self.frame_320 = QtWidgets.QFrame(self.frame_316)
        self.frame_320.setStyleSheet("border:none;")
        self.frame_320.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_320.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_320.setObjectName("frame_320")
        self.verticalLayout_189 = QtWidgets.QVBoxLayout(self.frame_320)
        self.verticalLayout_189.setObjectName("verticalLayout_189")
        self.jewellery_4 = QtWidgets.QLineEdit(self.frame_320)
        self.jewellery_4.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.jewellery_4.setObjectName("jewellery_4")
        self.verticalLayout_189.addWidget(self.jewellery_4)
        self.completer_1 = QCompleter()
        self.completer_1.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_1.popup().setStyleSheet("font-size: 30px") 
        self.jewellery_4.setCompleter(self.completer_1)
        # Connect the textChanged signal to your new function
        self.jewellery_4.textChanged.connect(self.update_completer_1_model)
        self.jewellery_5 = QtWidgets.QLineEdit(self.frame_320)
        self.jewellery_5.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.jewellery_5.setObjectName("jewellery_5")
        self.verticalLayout_189.addWidget(self.jewellery_5)
        self.horizontalLayout_152.addWidget(self.frame_320)
        self.horizontalLayout_152.setStretch(0, 1)
        self.horizontalLayout_152.setStretch(1, 1)
        self.horizontalLayout_149.addWidget(self.frame_316)
        self.horizontalLayout_149.setStretch(0, 1)
        self.horizontalLayout_149.setStretch(1, 1)
        self.verticalLayout_181.addWidget(self.frame_310)
        self.frame_321 = QtWidgets.QFrame(self.frame_307)
        self.frame_321.setStyleSheet("border: none;")
        self.frame_321.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_321.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_321.setObjectName("frame_321")
        self.horizontalLayout_154 = QtWidgets.QHBoxLayout(self.frame_321)
        self.horizontalLayout_154.setObjectName("horizontalLayout_154")
        self.frame_322 = QtWidgets.QFrame(self.frame_321)
        self.frame_322.setStyleSheet("")
        self.frame_322.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_322.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_322.setObjectName("frame_322")
        self.horizontalLayout_155 = QtWidgets.QHBoxLayout(self.frame_322)
        self.horizontalLayout_155.setObjectName("horizontalLayout_155")
        self.frame_323 = QtWidgets.QFrame(self.frame_322)
        self.frame_323.setStyleSheet("border:none;")
        self.frame_323.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_323.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_323.setObjectName("frame_323")
        self.horizontalLayout_156 = QtWidgets.QHBoxLayout(self.frame_323)
        self.horizontalLayout_156.setObjectName("horizontalLayout_156")
        self.frame_324 = QtWidgets.QFrame(self.frame_323)
        self.frame_324.setStyleSheet("border: none;")
        self.frame_324.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_324.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_324.setObjectName("frame_324")
        self.verticalLayout_190 = QtWidgets.QVBoxLayout(self.frame_324)
        self.verticalLayout_190.setObjectName("verticalLayout_190")
        self.frame_325 = QtWidgets.QFrame(self.frame_324)
        self.frame_325.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_325.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_325.setObjectName("frame_325")
        self.horizontalLayout_157 = QtWidgets.QHBoxLayout(self.frame_325)
        self.horizontalLayout_157.setObjectName("horizontalLayout_157")
        self.label_97 = QtWidgets.QLabel(self.frame_325)
        self.label_97.setStyleSheet("QFrame {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(255,255,255);\n"
"    border-radius: 15px;\n"
"    font: 550 23pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"}\n"
"\n"
"\n"
"")
        self.label_97.setAlignment(QtCore.Qt.AlignCenter)
        self.label_97.setObjectName("label_97")
        self.horizontalLayout_157.addWidget(self.label_97)
        self.verticalLayout_190.addWidget(self.frame_325)
        self.frame_326 = QtWidgets.QFrame(self.frame_324)
        self.frame_326.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_326.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_326.setObjectName("frame_326")
        self.verticalLayout_191 = QtWidgets.QVBoxLayout(self.frame_326)
        self.verticalLayout_191.setObjectName("verticalLayout_191")
        self.label_98 = QtWidgets.QLabel(self.frame_326)
        self.label_98.setStyleSheet("QFrame {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(255,255,255);\n"
"    border-radius: 15px;\n"
"    font: 550 23pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"}\n"
"\n"
"\n"
"")
        self.label_98.setAlignment(QtCore.Qt.AlignCenter)
        self.label_98.setObjectName("label_98")
        self.verticalLayout_191.addWidget(self.label_98)
        self.verticalLayout_190.addWidget(self.frame_326)
        self.horizontalLayout_156.addWidget(self.frame_324)
        self.frame_327 = QtWidgets.QFrame(self.frame_323)
        self.frame_327.setStyleSheet("border:none;")
        self.frame_327.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_327.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_327.setObjectName("frame_327")
        self.verticalLayout_192 = QtWidgets.QVBoxLayout(self.frame_327)
        self.verticalLayout_192.setObjectName("verticalLayout_192")
        self.jewellery_6 = QtWidgets.QLineEdit(self.frame_327)
        self.jewellery_6.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.jewellery_6.setObjectName("jewellery_6")
        self.verticalLayout_192.addWidget(self.jewellery_6)
        self.jewellery_7 = QtWidgets.QLineEdit(self.frame_327)
        self.jewellery_7.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.jewellery_7.setObjectName("jewellery_7")
        self.verticalLayout_192.addWidget(self.jewellery_7)
        self.horizontalLayout_156.addWidget(self.frame_327)
        self.horizontalLayout_156.setStretch(0, 1)
        self.horizontalLayout_156.setStretch(1, 1)
        self.horizontalLayout_155.addWidget(self.frame_323)
        self.frame_328 = QtWidgets.QFrame(self.frame_322)
        self.frame_328.setStyleSheet("border: none;")
        self.frame_328.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_328.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_328.setObjectName("frame_328")
        self.verticalLayout_193 = QtWidgets.QVBoxLayout(self.frame_328)
        self.verticalLayout_193.setObjectName("verticalLayout_193")
        self.frame_329 = QtWidgets.QFrame(self.frame_328)
        self.frame_329.setMinimumSize(QtCore.QSize(0, 50))
        self.frame_329.setStyleSheet("border: none;\n"
"")
        self.frame_329.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_329.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_329.setObjectName("frame_329")
        self.horizontalLayout_158 = QtWidgets.QHBoxLayout(self.frame_329)
        self.horizontalLayout_158.setObjectName("horizontalLayout_158")
        self.frame_330 = QtWidgets.QFrame(self.frame_329)
        self.frame_330.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_330.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_330.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_330.setObjectName("frame_330")
        self.horizontalLayout_159 = QtWidgets.QHBoxLayout(self.frame_330)
        self.horizontalLayout_159.setObjectName("horizontalLayout_159")
        self.label_99 = QtWidgets.QLabel(self.frame_330)
        self.label_99.setMinimumSize(QtCore.QSize(0, 50))
        self.label_99.setMaximumSize(QtCore.QSize(16777215, 50))
        self.label_99.setStyleSheet("QLabel {\n"
"    background-color: rgb(25, 25, 25);\n"
"    color: rgb(255,255,255);\n"
"    border-radius: 15px;\n"
"    font: 550 23pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"}\n"
"\n"
"\n"
"")
        self.label_99.setAlignment(QtCore.Qt.AlignCenter)
        self.label_99.setObjectName("label_99")
        self.horizontalLayout_159.addWidget(self.label_99, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_158.addWidget(self.frame_330)
        self.frame_331 = QtWidgets.QFrame(self.frame_329)
        self.frame_331.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_331.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_331.setObjectName("frame_331")
        self.horizontalLayout_160 = QtWidgets.QHBoxLayout(self.frame_331)
        self.horizontalLayout_160.setObjectName("horizontalLayout_160")
        self.jewellery_8 = QtWidgets.QLineEdit(self.frame_331)
        self.jewellery_8.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.jewellery_8.setObjectName("jewellery_8")
        self.horizontalLayout_160.addWidget(self.jewellery_8, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_158.addWidget(self.frame_331)
        self.horizontalLayout_158.setStretch(0, 1)
        self.horizontalLayout_158.setStretch(1, 1)
        self.verticalLayout_193.addWidget(self.frame_329)
        self.horizontalLayout_155.addWidget(self.frame_328)
        self.horizontalLayout_155.setStretch(0, 1)
        self.horizontalLayout_155.setStretch(1, 1)
        self.horizontalLayout_154.addWidget(self.frame_322)
        self.verticalLayout_181.addWidget(self.frame_321)
        self.frame_336 = QtWidgets.QFrame(self.frame_307)
        self.frame_336.setStyleSheet("border:none;")
        self.frame_336.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_336.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_336.setObjectName("frame_336")
        self.horizontalLayout_163 = QtWidgets.QHBoxLayout(self.frame_336)
        self.horizontalLayout_163.setObjectName("horizontalLayout_163")
        self.frame_337 = QtWidgets.QFrame(self.frame_336)
        self.frame_337.setStyleSheet("border:none;")
        self.frame_337.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_337.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_337.setObjectName("frame_337")
        self.verticalLayout_194 = QtWidgets.QVBoxLayout(self.frame_337)
        self.verticalLayout_194.setObjectName("verticalLayout_194")
        self.frame_338 = QtWidgets.QFrame(self.frame_337)
        self.frame_338.setStyleSheet("border:none;")
        self.frame_338.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_338.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_338.setObjectName("frame_338")
        self.verticalLayout_195 = QtWidgets.QVBoxLayout(self.frame_338)
        self.verticalLayout_195.setObjectName("verticalLayout_195")
        self.label_100 = QtWidgets.QLabel(self.frame_338)
        self.label_100.setStyleSheet("font: 26pt \"Segoe UI\";\n"
"color: rgb(200,200,200);")
        self.label_100.setAlignment(QtCore.Qt.AlignCenter)
        self.label_100.setObjectName("label_100")
        self.verticalLayout_195.addWidget(self.label_100)
        self.verticalLayout_194.addWidget(self.frame_338)
        self.frame_339 = QtWidgets.QFrame(self.frame_337)
        self.frame_339.setStyleSheet("border:none;")
        self.frame_339.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_339.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_339.setObjectName("frame_339")
        self.verticalLayout_196 = QtWidgets.QVBoxLayout(self.frame_339)
        self.verticalLayout_196.setObjectName("verticalLayout_196")
        self.label_101 = QtWidgets.QLabel(self.frame_339)
        self.label_101.setStyleSheet("font: 25pt \"Segoe UI\";\n"
"color: rgb(200,200,200);")
        self.label_101.setAlignment(QtCore.Qt.AlignCenter)
        self.label_101.setObjectName("label_101")
        self.verticalLayout_196.addWidget(self.label_101)
        self.verticalLayout_194.addWidget(self.frame_339)
        self.horizontalLayout_163.addWidget(self.frame_337)
        self.frame_340 = QtWidgets.QFrame(self.frame_336)
        self.frame_340.setStyleSheet("border:none;")
        self.frame_340.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_340.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_340.setObjectName("frame_340")
        self.horizontalLayout_164 = QtWidgets.QHBoxLayout(self.frame_340)
        self.horizontalLayout_164.setObjectName("horizontalLayout_164")
        self.label_102 = QtWidgets.QLabel(self.frame_340)
        self.label_102.setStyleSheet("image: url(://icons/resources/images/download.png);")
        self.label_102.setText("")
        self.label_102.setPixmap(QtGui.QPixmap("../../../ims/Loan Management System/download.png"))
        self.label_102.setObjectName("label_102")
        self.horizontalLayout_164.addWidget(self.label_102)
        self.horizontalLayout_163.addWidget(self.frame_340)
        self.frame_341 = QtWidgets.QFrame(self.frame_336)
        self.frame_341.setStyleSheet("border:none;")
        self.frame_341.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_341.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_341.setObjectName("frame_341")
        self.verticalLayout_197 = QtWidgets.QVBoxLayout(self.frame_341)
        self.verticalLayout_197.setObjectName("verticalLayout_197")
        self.pushButton_13 = QtWidgets.QPushButton(self.frame_341)
        self.pushButton_13.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButton_13.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(255, 114, 43);\n"
"font: 22pt \"Segoe UI\";\n"
"border-radius: 15px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/icons/icons/add.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_13.setIcon(icon10)
        self.pushButton_13.setObjectName("pushButton_13")
        self.double_click_protect = QTimer()
        self.double_click_protect.setSingleShot(True)
        self.double_click_protect.timeout.connect(self.allowClick)
        self.verticalLayout_197.addWidget(self.pushButton_13)
        self.pushButton_14 = QtWidgets.QPushButton(self.frame_341)
        self.pushButton_14.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(3, 53, 127);\n"
"font: 20pt \"Segoe UI\";\n"
"border-radius: 15px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/icons/icons/fingerprint.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_14.setIcon(icon11)
        self.pushButton_14.setObjectName("pushButton_14")
        self.verticalLayout_197.addWidget(self.pushButton_14)
        self.horizontalLayout_163.addWidget(self.frame_341)
        self.verticalLayout_181.addWidget(self.frame_336)
        self.verticalLayout_181.setStretch(0, 1)
        self.verticalLayout_181.setStretch(1, 1)
        self.verticalLayout_181.setStretch(2, 1)
        self.verticalLayout_181.setStretch(3, 1)
        self.verticalLayout_14.addWidget(self.frame_307)
        self.verticalLayout_12.addWidget(self.frame_14)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.page_3)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_20 = QtWidgets.QFrame(self.page_3)
        self.frame_20.setStyleSheet("border:none;")
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.frame_345 = QtWidgets.QFrame(self.frame_20)
        self.frame_345.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"border-radius: 15px;\n"
"border:2px solid white;")
        self.frame_345.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_345.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_345.setObjectName("frame_345")
        self.verticalLayout_202 = QtWidgets.QVBoxLayout(self.frame_345)
        self.verticalLayout_202.setObjectName("verticalLayout_202")
        self.frame_346 = QtWidgets.QFrame(self.frame_345)
        self.frame_346.setStyleSheet("border:none;")
        self.frame_346.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_346.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_346.setObjectName("frame_346")
        self.verticalLayout_203 = QtWidgets.QVBoxLayout(self.frame_346)
        self.verticalLayout_203.setObjectName("verticalLayout_203")
        self.frame_347 = QtWidgets.QFrame(self.frame_346)
        self.frame_347.setStyleSheet("border:none;")
        self.frame_347.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_347.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_347.setObjectName("frame_347")
        self.horizontalLayout_166 = QtWidgets.QHBoxLayout(self.frame_347)
        self.horizontalLayout_166.setObjectName("horizontalLayout_166")
        self.label_103 = QtWidgets.QLabel(self.frame_347)
        self.label_103.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_103.setStyleSheet("QFrame {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 15px;\n"
"    font: 24pt \"Segoe UI\";\n"
"    font: 9pt \"Segoe UI\";\n"
"    font: 550 35pt \"Segoe UI\";\n"
"    border-bottom: 2px solid white;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"\n"
"")
        self.label_103.setAlignment(QtCore.Qt.AlignCenter)
        self.label_103.setObjectName("label_103")
        self.horizontalLayout_166.addWidget(self.label_103)
        self.verticalLayout_203.addWidget(self.frame_347)
        self.frame_348 = QtWidgets.QFrame(self.frame_346)
        self.frame_348.setMinimumSize(QtCore.QSize(0, 170))
        self.frame_348.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_348.setStyleSheet("\n"
"border:none;")
        self.frame_348.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_348.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_348.setObjectName("frame_348")
        self.horizontalLayout_167 = QtWidgets.QHBoxLayout(self.frame_348)
        self.horizontalLayout_167.setObjectName("horizontalLayout_167")
        self.frame_349 = QtWidgets.QFrame(self.frame_348)
        self.frame_349.setMaximumSize(QtCore.QSize(450, 16777215))
        self.frame_349.setStyleSheet("border:none;")
        self.frame_349.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_349.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_349.setObjectName("frame_349")
        self.verticalLayout_204 = QtWidgets.QVBoxLayout(self.frame_349)
        self.verticalLayout_204.setObjectName("verticalLayout_204")
        self.comboBox_3 = QtWidgets.QComboBox(self.frame_349)
        self.comboBox_3.setMinimumSize(QtCore.QSize(327, 0))
        self.comboBox_3.setStyleSheet("border: 2px solid Black;\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius:0px;\n"
"color: rgb(200,200,200);\n"
"")
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.verticalLayout_204.addWidget(self.comboBox_3, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.frame_30 = QtWidgets.QFrame(self.frame_349)
        self.frame_30.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_30.setObjectName("frame_30")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.frame_30)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_4 = QtWidgets.QPushButton(self.frame_30)
        self.label_4.setStyleSheet("QPushButton {\n"
"    background-color: rgb(18,18,18);\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_25.addWidget(self.label_4)
        self.label_104 = QtWidgets.QLabel(self.frame_30)
        self.label_104.setStyleSheet("font: 15pt \"Segoe UI\";\n"
"color: rgb(200,200,200);")
        self.label_104.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_104.setObjectName("label_104")
        self.horizontalLayout_25.addWidget(self.label_104)
        self.horizontalLayout_25.setStretch(0, 1)
        self.horizontalLayout_25.setStretch(1, 3)
        self.verticalLayout_204.addWidget(self.frame_30)
        self.horizontalLayout_167.addWidget(self.frame_349)
        self.frame_350 = QtWidgets.QFrame(self.frame_348)
        self.frame_350.setStyleSheet("border:none;")
        self.frame_350.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_350.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_350.setObjectName("frame_350")
        self.verticalLayout_205 = QtWidgets.QVBoxLayout(self.frame_350)
        self.verticalLayout_205.setObjectName("verticalLayout_205")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame_350)
        self.lineEdit_5.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.verticalLayout_205.addWidget(self.lineEdit_5)
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.popup().setStyleSheet("font-size: 30px") 
        self.lineEdit_5.setCompleter(self.completer)
        # Connect the textChanged signal to your new function
        self.lineEdit_5.textChanged.connect(self.update_completer_model)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame_350)
        self.lineEdit_6.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.lineEdit_6.setPlaceholderText("")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.verticalLayout_205.addWidget(self.lineEdit_6)
        self.horizontalLayout_167.addWidget(self.frame_350)
        self.frame_351 = QtWidgets.QFrame(self.frame_348)
        self.frame_351.setStyleSheet("border:none;")
        self.frame_351.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_351.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_351.setObjectName("frame_351")
        self.verticalLayout_206 = QtWidgets.QVBoxLayout(self.frame_351)
        self.verticalLayout_206.setObjectName("verticalLayout_206")
        self.pushButton_16 = QtWidgets.QPushButton(self.frame_351)
        self.pushButton_16.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_16.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_16.setFont(font)
        self.pushButton_16.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(3, 53, 127);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.pushButton_16.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_16.setObjectName("pushButton_16")
        self.verticalLayout_206.addWidget(self.pushButton_16)
        self.pushButton_17 = QtWidgets.QPushButton(self.frame_351)
        self.pushButton_17.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_17.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_17.setFont(font)
        self.pushButton_17.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(255, 114, 43);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"")
        self.pushButton_17.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_17.setObjectName("pushButton_17")
        self.verticalLayout_206.addWidget(self.pushButton_17)
        self.pushButton_20 = QtWidgets.QPushButton(self.frame_351)
        self.pushButton_20.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_20.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_20.setFont(font)
        self.pushButton_20.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(255, 0,0);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.pushButton_20.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_20.setObjectName("pushButton_20")
        self.verticalLayout_206.addWidget(self.pushButton_20)
        self.horizontalLayout_167.addWidget(self.frame_351)
        self.verticalLayout_203.addWidget(self.frame_348)
        self.verticalLayout_202.addWidget(self.frame_346)
        self.frame_352 = QtWidgets.QFrame(self.frame_345)
        self.frame_352.setStyleSheet("border:none;")
        self.frame_352.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_352.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_352.setObjectName("frame_352")
        self.horizontalLayout_168 = QtWidgets.QHBoxLayout(self.frame_352)
        self.horizontalLayout_168.setObjectName("horizontalLayout_168")
        self.tableWidget_exist_5 = QtWidgets.QTableWidget(self.frame_352)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_exist_5.sizePolicy().hasHeightForWidth())
        self.tableWidget_exist_5.setSizePolicy(sizePolicy)
        self.tableWidget_exist_5.setMouseTracking(False)
        self.tableWidget_exist_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget_exist_5.setStyleSheet("border: 2px solid Black;\n"
"border-radius:0px;")
        self.tableWidget_exist_5.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableWidget_exist_5.setShowGrid(True)
        self.tableWidget_exist_5.setCornerButtonEnabled(True)
        self.tableWidget_exist_5.setObjectName("tableWidget_exist_5")
        self.tableWidget_exist_5.setColumnCount(10)
        self.tableWidget_exist_5.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_exist_5.setHorizontalHeaderItem(9, item)
        self.tableWidget_exist_5.horizontalHeader().setDefaultSectionSize(165)
        self.horizontalLayout_168.addWidget(self.tableWidget_exist_5)
        self.verticalLayout_202.addWidget(self.frame_352)
        self.verticalLayout_202.setStretch(0, 1)
        self.verticalLayout_202.setStretch(1, 2)
        self.horizontalLayout_17.addWidget(self.frame_345)
        self.horizontalLayout_10.addWidget(self.frame_20)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.frame_21 = QtWidgets.QFrame(self.page_4)
        self.frame_21.setStyleSheet("border:none;")
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame_21)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.frame_354 = QtWidgets.QFrame(self.frame_21)
        self.frame_354.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"border-radius: 15px;\n"
"border:2px solid white;")
        self.frame_354.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_354.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_354.setObjectName("frame_354")
        self.verticalLayout_209 = QtWidgets.QVBoxLayout(self.frame_354)
        self.verticalLayout_209.setObjectName("verticalLayout_209")
        self.frame_355 = QtWidgets.QFrame(self.frame_354)
        self.frame_355.setStyleSheet("border:none;")
        self.frame_355.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_355.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_355.setObjectName("frame_355")
        self.verticalLayout_210 = QtWidgets.QVBoxLayout(self.frame_355)
        self.verticalLayout_210.setObjectName("verticalLayout_210")
        self.frame_356 = QtWidgets.QFrame(self.frame_355)
        self.frame_356.setStyleSheet("QFrame {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 15px;\n"
"    font: 24pt \"Segoe UI\";\n"
"    font: 9pt \"Segoe UI\";\n"
"    font: 550 35pt \"Segoe UI\";\n"
"    border-bottom: 2px solid white;\n"
"}\n"
"\n"
"\n"
"")
        self.frame_356.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_356.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_356.setObjectName("frame_356")
        self.horizontalLayout_169 = QtWidgets.QHBoxLayout(self.frame_356)
        self.horizontalLayout_169.setObjectName("horizontalLayout_169")
        self.label_105 = QtWidgets.QLabel(self.frame_356)
        self.label_105.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_105.setStyleSheet("font: 24pt \"Segoe UI\";\n"
"font: 9pt \"Segoe UI\";\n"
"font: 550 35pt \"Segoe UI\";\n"
"border: none;\n"
"color: rgb(200,200,200);")
        self.label_105.setAlignment(QtCore.Qt.AlignCenter)
        self.label_105.setObjectName("label_105")
        self.horizontalLayout_169.addWidget(self.label_105)
        self.verticalLayout_210.addWidget(self.frame_356)
        self.frame_357 = QtWidgets.QFrame(self.frame_355)
        self.frame_357.setStyleSheet("\n"
"border:none;")
        self.frame_357.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_357.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_357.setObjectName("frame_357")
        self.horizontalLayout_170 = QtWidgets.QHBoxLayout(self.frame_357)
        self.horizontalLayout_170.setObjectName("horizontalLayout_170")
        self.frame_358 = QtWidgets.QFrame(self.frame_357)
        self.frame_358.setStyleSheet("border:none;")
        self.frame_358.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_358.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_358.setObjectName("frame_358")
        self.verticalLayout_211 = QtWidgets.QVBoxLayout(self.frame_358)
        self.verticalLayout_211.setObjectName("verticalLayout_211")
        self.comboBox_4 = QtWidgets.QComboBox(self.frame_358)
        self.comboBox_4.setMinimumSize(QtCore.QSize(327, 0))
        self.comboBox_4.setStyleSheet("border: 2px solid Black;\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius:0px;\n"
"color: rgb(200,200,200);\n"
"")
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.verticalLayout_211.addWidget(self.comboBox_4, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.label_106 = QtWidgets.QLabel(self.frame_358)
        self.label_106.setStyleSheet("font: 15pt \"Segoe UI\";\n"
"color: rgb(200,200,200);")
        self.label_106.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_106.setObjectName("label_106")
        self.verticalLayout_211.addWidget(self.label_106)
        self.horizontalLayout_170.addWidget(self.frame_358)
        self.frame_359 = QtWidgets.QFrame(self.frame_357)
        self.frame_359.setStyleSheet("border:none;")
        self.frame_359.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_359.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_359.setObjectName("frame_359")
        self.verticalLayout_212 = QtWidgets.QVBoxLayout(self.frame_359)
        self.verticalLayout_212.setObjectName("verticalLayout_212")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame_359)
        self.lineEdit_7.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.completer_2 = QCompleter()
        self.completer_2.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_2.popup().setStyleSheet("font-size: 30px") 
        self.lineEdit_7.setCompleter(self.completer_2)
        # Connect the textChanged signal to your new function
        self.lineEdit_7.textChanged.connect(self.update_completer_2_model)
        self.verticalLayout_212.addWidget(self.lineEdit_7)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.frame_359)
        self.lineEdit_8.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.lineEdit_8.setPlaceholderText("")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.verticalLayout_212.addWidget(self.lineEdit_8)
        self.horizontalLayout_170.addWidget(self.frame_359)
        self.frame_360 = QtWidgets.QFrame(self.frame_357)
        self.frame_360.setStyleSheet("border:none;")
        self.frame_360.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_360.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_360.setObjectName("frame_360")
        self.verticalLayout_213 = QtWidgets.QVBoxLayout(self.frame_360)
        self.verticalLayout_213.setObjectName("verticalLayout_213")
        self.pushButton_18 = QtWidgets.QPushButton(self.frame_360)
        self.pushButton_18.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_18.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_18.setFont(font)
        self.pushButton_18.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(3, 53, 127);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.pushButton_18.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_18.setObjectName("pushButton_18")
        self.verticalLayout_213.addWidget(self.pushButton_18)
        self.pushButton_19 = QtWidgets.QPushButton(self.frame_360)
        self.pushButton_19.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_19.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_19.setFont(font)
        self.pushButton_19.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(255, 114, 43);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}\n"
"")
        self.pushButton_19.setIcon(icon10)
        self.pushButton_19.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_19.setObjectName("pushButton_19")
        self.verticalLayout_213.addWidget(self.pushButton_19)
        self.horizontalLayout_170.addWidget(self.frame_360)
        self.verticalLayout_210.addWidget(self.frame_357)
        self.verticalLayout_209.addWidget(self.frame_355)
        self.frame_361 = QtWidgets.QFrame(self.frame_354)
        self.frame_361.setStyleSheet("border:none;")
        self.frame_361.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_361.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_361.setObjectName("frame_361")
        self.horizontalLayout_171 = QtWidgets.QHBoxLayout(self.frame_361)
        self.horizontalLayout_171.setObjectName("horizontalLayout_171")
        self.tableWidget_5 = QtWidgets.QTableWidget(self.frame_361)
        self.tableWidget_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget_5.setStyleSheet("border:2px solid black;\n"
"border-radius:0px;")
        self.tableWidget_5.setShowGrid(True)
        self.tableWidget_5.setCornerButtonEnabled(True)
        self.tableWidget_5.setObjectName("tableWidget_5")
        self.tableWidget_5.setColumnCount(10)
        self.tableWidget_5.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_5.setHorizontalHeaderItem(9, item)
        self.tableWidget_5.horizontalHeader().setDefaultSectionSize(165)
        self.horizontalLayout_171.addWidget(self.tableWidget_5)
        self.verticalLayout_209.addWidget(self.frame_361)
        self.horizontalLayout_18.addWidget(self.frame_354)
        self.verticalLayout_15.addWidget(self.frame_21)
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.page_5)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.frame_22 = QtWidgets.QFrame(self.page_5)
        self.frame_22.setStyleSheet("border:none;")
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_22)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.frame_363 = QtWidgets.QFrame(self.frame_22)
        self.frame_363.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"border-radius: 15px;\n"
"border:2px solid white;")
        self.frame_363.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_363.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_363.setObjectName("frame_363")
        self.verticalLayout_215 = QtWidgets.QVBoxLayout(self.frame_363)
        self.verticalLayout_215.setObjectName("verticalLayout_215")
        self.frame_364 = QtWidgets.QFrame(self.frame_363)
        self.frame_364.setStyleSheet("border:none;")
        self.frame_364.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_364.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_364.setObjectName("frame_364")
        self.verticalLayout_216 = QtWidgets.QVBoxLayout(self.frame_364)
        self.verticalLayout_216.setObjectName("verticalLayout_216")
        self.frame_365 = QtWidgets.QFrame(self.frame_364)
        self.frame_365.setStyleSheet("border:none;")
        self.frame_365.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_365.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_365.setObjectName("frame_365")
        self.horizontalLayout_173 = QtWidgets.QHBoxLayout(self.frame_365)
        self.horizontalLayout_173.setObjectName("horizontalLayout_173")
        self.label_107 = QtWidgets.QLabel(self.frame_365)
        self.label_107.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_107.setStyleSheet("QFrame {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 15px;\n"
"    font: 24pt \"Segoe UI\";\n"
"    font: 9pt \"Segoe UI\";\n"
"    font: 550 35pt \"Segoe UI\";\n"
"    border-bottom: 2px solid white;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"\n"
"")
        self.label_107.setAlignment(QtCore.Qt.AlignCenter)
        self.label_107.setObjectName("label_107")
        self.horizontalLayout_173.addWidget(self.label_107)
        self.verticalLayout_216.addWidget(self.frame_365)
        self.frame_366 = QtWidgets.QFrame(self.frame_364)
        self.frame_366.setStyleSheet("\n"
"border:none;")
        self.frame_366.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_366.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_366.setObjectName("frame_366")
        self.horizontalLayout_174 = QtWidgets.QHBoxLayout(self.frame_366)
        self.horizontalLayout_174.setObjectName("horizontalLayout_174")
        self.frame_367 = QtWidgets.QFrame(self.frame_366)
        self.frame_367.setStyleSheet("border:none;")
        self.frame_367.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_367.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_367.setObjectName("frame_367")
        self.verticalLayout_217 = QtWidgets.QVBoxLayout(self.frame_367)
        self.verticalLayout_217.setObjectName("verticalLayout_217")
        self.comboBox_removed_3 = QtWidgets.QComboBox(self.frame_367)
        self.comboBox_removed_3.setMinimumSize(QtCore.QSize(327, 0))
        self.comboBox_removed_3.setStyleSheet("border: 2px solid Black;\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius:0px;\n"
"color: rgb(200,200,200);\n"
"")
        self.comboBox_removed_3.setObjectName("comboBox_removed_3")
        self.comboBox_removed_3.addItem("")
        self.comboBox_removed_3.addItem("")
        self.comboBox_removed_3.addItem("")
        self.verticalLayout_217.addWidget(self.comboBox_removed_3, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_174.addWidget(self.frame_367)
        self.frame_368 = QtWidgets.QFrame(self.frame_366)
        self.frame_368.setStyleSheet("border:none;")
        self.frame_368.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_368.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_368.setObjectName("frame_368")
        self.horizontalLayout_175 = QtWidgets.QHBoxLayout(self.frame_368)
        self.horizontalLayout_175.setObjectName("horizontalLayout_175")
        self.lineEdit_removed_3 = QtWidgets.QLineEdit(self.frame_368)
        self.lineEdit_removed_3.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.lineEdit_removed_3.setObjectName("lineEdit_removed_3")
        self.completer_3 = QCompleter()
        self.completer_3.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_3.popup().setStyleSheet("font-size: 30px") 
        self.lineEdit_removed_3.setCompleter(self.completer_3)
        # Connect the textChanged signal to your new function
        self.lineEdit_removed_3.textChanged.connect(self.update_completer_3_model)
        self.horizontalLayout_175.addWidget(self.lineEdit_removed_3)
        self.horizontalLayout_174.addWidget(self.frame_368)
        self.frame_369 = QtWidgets.QFrame(self.frame_366)
        self.frame_369.setStyleSheet("border:none;")
        self.frame_369.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_369.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_369.setObjectName("frame_369")
        self.verticalLayout_218 = QtWidgets.QVBoxLayout(self.frame_369)
        self.verticalLayout_218.setObjectName("verticalLayout_218")
        self.pushButton_removed_3 = QtWidgets.QPushButton(self.frame_369)
        self.pushButton_removed_3.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_removed_3.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_removed_3.setFont(font)
        self.pushButton_removed_3.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(3, 53, 127);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.pushButton_removed_3.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_removed_3.setObjectName("pushButton_removed_3")
        self.verticalLayout_218.addWidget(self.pushButton_removed_3)
        self.horizontalLayout_174.addWidget(self.frame_369)
        self.verticalLayout_216.addWidget(self.frame_366)
        self.verticalLayout_215.addWidget(self.frame_364)
        self.frame_370 = QtWidgets.QFrame(self.frame_363)
        self.frame_370.setStyleSheet("border:none;")
        self.frame_370.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_370.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_370.setObjectName("frame_370")
        self.horizontalLayout_176 = QtWidgets.QHBoxLayout(self.frame_370)
        self.horizontalLayout_176.setObjectName("horizontalLayout_176")
        self.tableWidget_removed_9 = QtWidgets.QTableWidget(self.frame_370)
        self.tableWidget_removed_9.setStyleSheet("border:2px solid black;\n"
"border-radius:0px;")
        self.tableWidget_removed_9.setObjectName("tableWidget_removed_9")
        self.tableWidget_removed_9.setColumnCount(10)
        self.tableWidget_removed_9.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_9.setHorizontalHeaderItem(9, item)
        self.tableWidget_removed_9.horizontalHeader().setDefaultSectionSize(165)
        self.horizontalLayout_176.addWidget(self.tableWidget_removed_9)
        self.verticalLayout_215.addWidget(self.frame_370)
        self.horizontalLayout_19.addWidget(self.frame_363)
        self.horizontalLayout_15.addWidget(self.frame_22)
        self.stackedWidget.addWidget(self.page_5)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.page_6)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.frame_23 = QtWidgets.QFrame(self.page_6)
        self.frame_23.setStyleSheet("border:none;")
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.frame_23)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.frame_372 = QtWidgets.QFrame(self.frame_23)
        self.frame_372.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"border-radius: 15px;\n"
"border:2px solid white;")
        self.frame_372.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_372.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_372.setObjectName("frame_372")
        self.verticalLayout_219 = QtWidgets.QVBoxLayout(self.frame_372)
        self.verticalLayout_219.setObjectName("verticalLayout_219")
        self.frame_373 = QtWidgets.QFrame(self.frame_372)
        self.frame_373.setStyleSheet("border:none;")
        self.frame_373.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_373.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_373.setObjectName("frame_373")
        self.verticalLayout_220 = QtWidgets.QVBoxLayout(self.frame_373)
        self.verticalLayout_220.setObjectName("verticalLayout_220")
        self.frame_374 = QtWidgets.QFrame(self.frame_373)
        self.frame_374.setStyleSheet("border:none;")
        self.frame_374.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_374.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_374.setObjectName("frame_374")
        self.horizontalLayout_179 = QtWidgets.QHBoxLayout(self.frame_374)
        self.horizontalLayout_179.setObjectName("horizontalLayout_179")
        self.label_108 = QtWidgets.QLabel(self.frame_374)
        self.label_108.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_108.setStyleSheet("QFrame {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 15px;\n"
"    font: 24pt \"Segoe UI\";\n"
"    font: 9pt \"Segoe UI\";\n"
"    font: 550 35pt \"Segoe UI\";\n"
"    border-bottom: 2px solid white;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"\n"
"")
        self.label_108.setAlignment(QtCore.Qt.AlignCenter)
        self.label_108.setObjectName("label_108")
        self.horizontalLayout_179.addWidget(self.label_108)
        self.verticalLayout_220.addWidget(self.frame_374)
        self.frame_375 = QtWidgets.QFrame(self.frame_373)
        self.frame_375.setStyleSheet("\n"
"border:none;")
        self.frame_375.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_375.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_375.setObjectName("frame_375")
        self.horizontalLayout_180 = QtWidgets.QHBoxLayout(self.frame_375)
        self.horizontalLayout_180.setObjectName("horizontalLayout_180")
        self.frame_376 = QtWidgets.QFrame(self.frame_375)
        self.frame_376.setStyleSheet("border:none;")
        self.frame_376.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_376.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_376.setObjectName("frame_376")
        self.verticalLayout_221 = QtWidgets.QVBoxLayout(self.frame_376)
        self.verticalLayout_221.setObjectName("verticalLayout_221")
        self.comboBox_removed_4 = QtWidgets.QComboBox(self.frame_376)
        self.comboBox_removed_4.setMinimumSize(QtCore.QSize(327, 0))
        self.comboBox_removed_4.setStyleSheet("border: 2px solid Black;\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius:0px;\n"
"color: rgb(200,200,200);\n"
"")
        self.comboBox_removed_4.setObjectName("comboBox_removed_4")
        self.comboBox_removed_4.addItem("")
        self.comboBox_removed_4.addItem("")
        self.comboBox_removed_4.addItem("")
        self.verticalLayout_221.addWidget(self.comboBox_removed_4, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.horizontalLayout_180.addWidget(self.frame_376)
        self.frame_377 = QtWidgets.QFrame(self.frame_375)
        self.frame_377.setStyleSheet("border:none;")
        self.frame_377.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_377.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_377.setObjectName("frame_377")
        self.horizontalLayout_181 = QtWidgets.QHBoxLayout(self.frame_377)
        self.horizontalLayout_181.setObjectName("horizontalLayout_181")
        self.lineEdit_removed_4 = QtWidgets.QLineEdit(self.frame_377)
        self.lineEdit_removed_4.setStyleSheet("QLineEdit {\n"
"    background-color: rgb(50,50,50);\n"
"    border-radius: 5px;\n"
"    font: 21pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(255, 85, 0);\n"
"}")
        self.lineEdit_removed_4.setObjectName("lineEdit_removed_4")
        self.completer_4 = QCompleter()
        self.completer_4.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer_4.popup().setStyleSheet("font-size: 30px") 
        self.lineEdit_removed_4.setCompleter(self.completer_4)
        # Connect the textChanged signal to your new function
        self.lineEdit_removed_4.textChanged.connect(self.update_completer_4_model)
        self.horizontalLayout_181.addWidget(self.lineEdit_removed_4)
        self.horizontalLayout_180.addWidget(self.frame_377)
        self.frame_378 = QtWidgets.QFrame(self.frame_375)
        self.frame_378.setStyleSheet("border:none;")
        self.frame_378.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_378.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_378.setObjectName("frame_378")
        self.verticalLayout_222 = QtWidgets.QVBoxLayout(self.frame_378)
        self.verticalLayout_222.setObjectName("verticalLayout_222")
        self.pushButton_removed_4 = QtWidgets.QPushButton(self.frame_378)
        self.pushButton_removed_4.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_removed_4.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_removed_4.setFont(font)
        self.pushButton_removed_4.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(3, 53, 127);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.pushButton_removed_4.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_removed_4.setObjectName("pushButton_removed_4")
        self.verticalLayout_222.addWidget(self.pushButton_removed_4)
        self.horizontalLayout_180.addWidget(self.frame_378)
        self.verticalLayout_220.addWidget(self.frame_375)
        self.verticalLayout_219.addWidget(self.frame_373)
        self.frame_379 = QtWidgets.QFrame(self.frame_372)
        self.frame_379.setStyleSheet("border:none;")
        self.frame_379.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_379.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_379.setObjectName("frame_379")
        self.horizontalLayout_182 = QtWidgets.QHBoxLayout(self.frame_379)
        self.horizontalLayout_182.setObjectName("horizontalLayout_182")
        self.tableWidget_removed_10 = QtWidgets.QTableWidget(self.frame_379)
        self.tableWidget_removed_10.setStyleSheet("border:2px solid black;\n"
"border-radius:0px;")
        self.tableWidget_removed_10.setObjectName("tableWidget_removed_10")
        self.tableWidget_removed_10.setColumnCount(10)
        self.tableWidget_removed_10.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(15)
        item.setFont(font)
        self.tableWidget_removed_10.setHorizontalHeaderItem(9, item)
        self.tableWidget_removed_10.horizontalHeader().setDefaultSectionSize(165)
        self.horizontalLayout_182.addWidget(self.tableWidget_removed_10)
        self.verticalLayout_219.addWidget(self.frame_379)
        self.horizontalLayout_20.addWidget(self.frame_372)
        self.horizontalLayout_16.addWidget(self.frame_23)
        self.stackedWidget.addWidget(self.page_6)
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.page_7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame_332 = QtWidgets.QFrame(self.page_7)
        self.frame_332.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_332.setStyleSheet("background-color: rgb(18, 18, 18);\n"
"border-radius: 15px;\n"
"border:2px solid white;")
        self.frame_332.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_332.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_332.setObjectName("frame_332")
        self.verticalLayout_198 = QtWidgets.QVBoxLayout(self.frame_332)
        self.verticalLayout_198.setObjectName("verticalLayout_198")
        self.frame_333 = QtWidgets.QFrame(self.frame_332)
        self.frame_333.setStyleSheet("border: none;")
        self.frame_333.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_333.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_333.setObjectName("frame_333")
        self.verticalLayout_199 = QtWidgets.QVBoxLayout(self.frame_333)
        self.verticalLayout_199.setObjectName("verticalLayout_199")
        self.frame_334 = QtWidgets.QFrame(self.frame_333)
        self.frame_334.setStyleSheet("border: none;")
        self.frame_334.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_334.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_334.setObjectName("frame_334")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_334)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_109 = QtWidgets.QLabel(self.frame_334)
        self.label_109.setMinimumSize(QtCore.QSize(0, 0))
        self.label_109.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_109.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_109.setStyleSheet("QFrame {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 15px;\n"
"    font: 24pt \"Segoe UI\";\n"
"    font: 9pt \"Segoe UI\";\n"
"    font: 550 35pt \"Segoe UI\";\n"
"    border-bottom: 2px solid white;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"\n"
"\n"
"")
        self.label_109.setAlignment(QtCore.Qt.AlignCenter)
        self.label_109.setObjectName("label_109")
        self.verticalLayout_4.addWidget(self.label_109)
        self.frame_5 = QtWidgets.QFrame(self.frame_334)
        self.frame_5.setStyleSheet("border:none;")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.frame_24 = QtWidgets.QFrame(self.frame_5)
        self.frame_24.setStyleSheet("border:none;")
        self.frame_24.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.frame_24)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.frame_28 = QtWidgets.QFrame(self.frame_24)
        self.frame_28.setStyleSheet("border:none;")
        self.frame_28.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_28.setObjectName("frame_28")
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout(self.frame_28)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.comboBox_2 = QtWidgets.QComboBox(self.frame_28)
        self.comboBox_2.setStyleSheet("border: 2px solid Black;\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius:0px;\n"
"color: rgb(200,200,200);\n"
"")
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_21.addWidget(self.comboBox_2)
        self.dateEdit = QtWidgets.QDateEdit(self.frame_28)
        self.dateEdit.setStyleSheet("border: 2px solid Black;\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius:0px;\n"
"color: rgb(200,200,200);\n"
"")
        self.dateEdit.setObjectName("dateEdit")
        self.horizontalLayout_21.addWidget(self.dateEdit)
        self.dateEdit_2 = QtWidgets.QDateEdit(self.frame_28)
        self.dateEdit_2.setStyleSheet("border: 2px solid Black;\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius:0px;\n"
"color: rgb(200,200,200);\n"
"")
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.horizontalLayout_21.addWidget(self.dateEdit_2)
        self.pushButton_removed_5 = QtWidgets.QPushButton(self.frame_28)
        self.pushButton_removed_5.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_removed_5.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_removed_5.setFont(font)
        self.pushButton_removed_5.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(3, 53, 127);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.pushButton_removed_5.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_removed_5.setObjectName("pushButton_removed_5")
        self.horizontalLayout_21.addWidget(self.pushButton_removed_5)
        self.verticalLayout_20.addWidget(self.frame_28)
        '''
        self.frame_27 = QtWidgets.QFrame(self.frame_24)
        self.frame_27.setStyleSheet("border:none;")
        self.frame_27.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_27.setObjectName("frame_27")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.frame_27)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.toggleButton_13 = QtWidgets.QPushButton(self.frame_27)
        self.toggleButton_13.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton_13.sizePolicy().hasHeightForWidth())
        self.toggleButton_13.setSizePolicy(sizePolicy)
        self.toggleButton_13.setMinimumSize(QtCore.QSize(200, 50))
        self.toggleButton_13.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setBold(True)
        self.toggleButton_13.setFont(font)
        self.toggleButton_13.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    font: 18pt 'Segoe UI';\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.toggleButton_13.setIcon(icon2)
        self.toggleButton_13.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_13.setObjectName("toggleButton_13")
        self.horizontalLayout_22.addWidget(self.toggleButton_13)
        self.toggleButton_14 = QtWidgets.QPushButton(self.frame_27)
        self.toggleButton_14.setMinimumSize(QtCore.QSize(200,50))
        self.toggleButton_14.setMaximumSize(QtCore.QSize(200,50))
        font = QtGui.QFont()
        font.setBold(True)
        self.toggleButton_14.setFont(font)
        self.toggleButton_14.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    font: 18pt 'Segoe UI';\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.toggleButton_14.setIcon(icon2)
        self.toggleButton_14.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_14.setObjectName("toggleButton_14")
        self.horizontalLayout_22.addWidget(self.toggleButton_14)
        self.toggleButton_15 = QtWidgets.QPushButton(self.frame_27)
        self.toggleButton_15.setMinimumSize(QtCore.QSize(200, 50))
        self.toggleButton_15.setMaximumSize(QtCore.QSize(200, 50))
        font = QtGui.QFont()
        font.setBold(True)
        self.toggleButton_15.setFont(font)
        self.toggleButton_15.setStyleSheet("QPushButton {\n"
"    border: none;\n"
"    font: 18pt 'Segoe UI';\n"
"    background-color: rgb(30, 30, 30);\n"
"    border-left: 3px solid rgb(30, 30, 30);\n"
"    border-right: 3px solid rgb(30, 30, 30);\n"
"    color: rgb(255, 85, 0);\n"
"    border-radius: 13px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border-left: 3px solid rgb(255, 85, 0);\n"
"    border-right: 3px solid rgb(255, 85, 0);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.toggleButton_15.setIcon(icon2)
        self.toggleButton_15.setIconSize(QtCore.QSize(25, 25))
        self.toggleButton_15.setObjectName("toggleButton_15")
        self.horizontalLayout_22.addWidget(self.toggleButton_15)
        self.verticalLayout_20.addWidget(self.frame_27)
        '''
        self.verticalLayout_20.setStretch(0, 2)
        self.verticalLayout_20.setStretch(1, 1)
        self.verticalLayout_19.addWidget(self.frame_24)
        self.frame_25 = QtWidgets.QFrame(self.frame_5)
        self.frame_25.setStyleSheet("border:none;")
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.frame_25)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.frame_26 = QtWidgets.QFrame(self.frame_25)
        self.frame_26.setStyleSheet("border:none;\n"
"")
        self.frame_26.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_26.setObjectName("frame_26")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.frame_26)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.tableView = QtWidgets.QTableView(self.frame_26)
        # Set the delegate to center-align text
        delegate = AlignDelegate()
        self.tableView.setItemDelegate(delegate)

        # Set the text color to white using a style sheet
        self.tableView.setStyleSheet("QTableView {\n"
"    color: white;\n"
"    font: 18pt 'Segoe UI';\n"
"    border:1px solid white;\n"
"    border-radius:3px;\n"
"}\n")
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.setObjectName("tableView")
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Date", "Amount"])
        self.tableView.setModel(self.model)
        # Set the horizontal header properties
        header = self.tableView.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStretchLastSection(True)
        # Set custom font for the horizontal header
        font = QFont()
        font.setPointSize(14)  # Set the font size to 14
        header.setFont(font)
        self.horizontalLayout_23.addWidget(self.tableView)
        self.verticalLayout_21.addWidget(self.frame_26)
        self.frame_29 = QtWidgets.QFrame(self.frame_25)
        self.frame_29.setStyleSheet("border:none;")
        self.frame_29.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.frame_29)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_3 = QtWidgets.QLabel(self.frame_29)
        self.label_3.setStyleSheet("QLabel {\n"
"    color: rgb(255,255,255);\n"
"    border-radius: 3px;\n"
"    font: 500 18pt \"Segoe UI\";\n"
"}\n"
"\n"
"\n"
"")
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_24.addWidget(self.label_3)
        self.lineEdit_2 = QtWidgets.QLabel(self.frame_29)
        self.lineEdit_2.setStyleSheet("QLabel {\n"
"    background-color: rgb(45,45,45);\n"
"    border-radius: 5px;\n"
"    font: 18pt \"Segoe UI\";\n"
"    border: 2px solid black;\n"
"color: rgb(200,200,200);\n"
"}\n"
)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_24.addWidget(self.lineEdit_2)
        self.pushButton_removed_6 = QtWidgets.QPushButton(self.frame_29)
        self.pushButton_removed_6.setMinimumSize(QtCore.QSize(200, 45))
        self.pushButton_removed_6.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_removed_6.setFont(font)
        self.pushButton_removed_6.setStyleSheet("QPushButton{border: 2px solid Black;\n"
"background-color: rgb(3, 127, 7);\n"
"font: 15pt \"Segoe UI\";\n"
"border-radius: 5px}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(25, 25, 25);\n"
"}")
        self.pushButton_removed_6.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_removed_6.setObjectName("pushButton_removed_6")
        self.horizontalLayout_24.addWidget(self.pushButton_removed_6)
        self.horizontalLayout_24.setStretch(0, 3)
        self.horizontalLayout_24.setStretch(1, 1)
        self.horizontalLayout_24.setStretch(2, 2)
        self.verticalLayout_21.addWidget(self.frame_29)
        self.verticalLayout_21.setStretch(0, 5)
        self.verticalLayout_21.setStretch(1, 1)
        self.verticalLayout_19.addWidget(self.frame_25)
        self.verticalLayout_19.setStretch(0, 1)
        self.verticalLayout_19.setStretch(1, 3)
        self.verticalLayout_4.addWidget(self.frame_5)
        self.verticalLayout_199.addWidget(self.frame_334)
        self.verticalLayout_198.addWidget(self.frame_333)
        self.verticalLayout_198.setStretch(0, 1)
        self.horizontalLayout_4.addWidget(self.frame_332)
        self.stackedWidget.addWidget(self.page_7)
        self.verticalLayout_18.addWidget(self.stackedWidget)
        self.horizontalLayout.addWidget(self.Container)
        self.verticalLayout.addWidget(self.Body)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet("QStatusBar {\n"
"    background-color: rgb(10, 11, 12);\n"
"}")
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statistics()
        self.insert_current_date()
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.plainTextEdit.setReadOnly(True)
        self.addbtn.clicked.connect(self.add_record)
        self.dashbtn.clicked.connect(self.DashBoard)
        self.removebtn.clicked.connect(self.remove)
        self.depositbtn.clicked.connect(self.deposit)
        self.viewbtn.clicked.connect(self.view)
        self.removedbtn.clicked.connect(self.removed)
        self.accountsbtn.clicked.connect(self.accounts)
        self.label_4.clicked.connect(self.open_image)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_13.clicked.connect(self.addnew)
        self.pushButton_14.clicked.connect(self.call_camera)
        self.pushButton_16.clicked.connect(self.search_remove)
        self.pushButton_17.clicked.connect(self.remove_record)
        self.pushButton_18.clicked.connect(self.search_deposit)
        self.pushButton_19.clicked.connect(self.add_deposit)
        self.pushButton_20.clicked.connect(self.delete_record)
        self.toggleButton_9.clicked.connect(self.generate_report)
        self.toggleButton_11.clicked.connect(self.add_cash)
        self.toggleButton_12.clicked.connect(self.backup_sql)
        self.toggleButton_8.clicked.connect(self.view_text)
        self.toggleButton_10.clicked.connect(self.save_text)
        self.toggleButton_7.clicked.connect(self.remove_cash)
        self.pushButton_removed_3.clicked.connect(self.search_view)
        self.pushButton_removed_4.clicked.connect(self.search_removed)
        self.pushButton_removed_5.clicked.connect(self.generate_report1)
        self.pushButton_removed_6.clicked.connect(self.save_as_pdf)
        self.comboBox.currentIndexChanged.connect(self.populate_chart)
        self.comboBox_3.currentIndexChanged.connect(self.disable_lineEdit_5)
        self.comboBox_4.currentIndexChanged.connect(self.disable_lineEdit_7)
        
        #==========================================================================
        self.tableWidget_exist_5.setStyleSheet("QTableWidget {font-size: 30px;}")
        self.tableWidget_exist_5.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        delegate = AlignDelegate(self.tableWidget_exist_5)
        self.tableWidget_exist_5.setItemDelegate(delegate)
        self.tableWidget_exist_5.horizontalHeader().setDefaultSectionSize(160)
        #============================================================================
        #==========================================================================
        self.tableWidget_5.setStyleSheet("QTableWidget {font-size: 30px;}")
        self.tableWidget_5.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        delegate = AlignDelegate(self.tableWidget_5)
        self.tableWidget_5.setItemDelegate(delegate)
        self.tableWidget_5.horizontalHeader().setDefaultSectionSize(160)
        #============================================================================
        #==========================================================================
        self.tableWidget_removed_9.setStyleSheet("QTableWidget {font-size: 30px;}")
        self.tableWidget_removed_9.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        delegate = AlignDelegate(self.tableWidget_exist_5)
        self.tableWidget_removed_9.setItemDelegate(delegate)
        self.tableWidget_removed_9.horizontalHeader().setDefaultSectionSize(160)
        #============================================================================
        #==========================================================================
        self.tableWidget_removed_10.setStyleSheet("QTableWidget {font-size: 30px;}")
        self.tableWidget_removed_10.verticalHeader().setDefaultAlignment(Qt.AlignCenter)
        delegate = AlignDelegate(self.tableWidget_exist_5)
        self.tableWidget_removed_10.setItemDelegate(delegate)
        self.tableWidget_removed_10.horizontalHeader().setDefaultSectionSize(170)
        #============================================================================

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "LoanMate"))
        self.label.setText(_translate("MainWindow", "Loan Management System"))
        self.toggleButton_7.setText(_translate("MainWindow", "Remove Cash"))
        self.toggleButton_11.setText(_translate("MainWindow", "Add Cash"))
        self.dashbtn.setText(_translate("MainWindow", " Dashboard"))
        self.addbtn.setText(_translate("MainWindow", "Add Record"))
        self.removebtn.setText(_translate("MainWindow", "Remove Rec."))
        self.depositbtn.setText(_translate("MainWindow", "Add Deposit"))
        self.viewbtn.setText(_translate("MainWindow", "View Records"))
        self.removedbtn.setText(_translate("MainWindow", "Removed Rec."))
        self.accountsbtn.setText(_translate("MainWindow", "View Accounts"))
        self.pushButton.setText(_translate("MainWindow", "Close"))
        self.label_11.setText(_translate("MainWindow", "Total Investment"))
        #self.total_investment.setText(_translate("MainWindow", "$125, 300"))
        #self.lineEdit_9.setText(_translate("MainWindow", "+16%"))
        self.label_2.setText(_translate("MainWindow", "Today\'s Investment"))
        #self.todays_investment.setText(_translate("MainWindow", "5, 625"))
        #self.lineEdit_10.setText(_translate("MainWindow", "+7%"))
        self.label_15.setText(_translate("MainWindow", "Today\'s Return"))
        #self.todays_return.setText(_translate("MainWindow", "+9.8%"))
        self.label_7.setText(_translate("MainWindow", "Today\'s Interest"))
        #self.todays_interest.setText(_translate("MainWindow", "2,122"))
        #self.label_22.setText(_translate("MainWindow", "Accounting Stats"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Investments"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Returns"))
        self.label_23.setText(_translate("MainWindow", "Daily Report"))
        self.toggleButton_8.setText(_translate("MainWindow", "View"))
        self.toggleButton_9.setText(_translate("MainWindow", "Generate"))
        self.toggleButton_10.setText(_translate("MainWindow", "Save"))
        self.toggleButton_12.setText(_translate("MainWindow", "Backup"))
        self.label_92.setText(_translate("MainWindow", "Add New Record"))
        self.label_93.setText(_translate("MainWindow", "Name"))
        self.label_94.setText(_translate("MainWindow", "Father\'s Name"))
        self.label_95.setText(_translate("MainWindow", "Location"))
        self.label_96.setText(_translate("MainWindow", "Amount"))
        self.label_97.setText(_translate("MainWindow", "Jewellery"))
        self.label_98.setText(_translate("MainWindow", "Date"))
        self.label_99.setText(_translate("MainWindow", "Weight (in gm)"))
        self.label_100.setText(_translate("MainWindow", "Biometric"))
        self.label_101.setText(_translate("MainWindow", "Identification"))
        self.pushButton_13.setText(_translate("MainWindow", "Add Record"))
        self.pushButton_14.setText(_translate("MainWindow", " Add Fingerprint"))
        self.label_103.setText(_translate("MainWindow", "Remove Record"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "Name"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "Date"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "Location"))
        self.comboBox_3.setItemText(3, _translate("MainWindow", "Fingerprint"))
        self.label_104.setText(_translate("MainWindow", "Interest Till Date "))
        self.pushButton_16.setText(_translate("MainWindow", "Search Record"))
        self.pushButton_17.setText(_translate("MainWindow", "Remove Record"))
        self.pushButton_20.setText(_translate("MainWindow", "Delete"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "User id"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Amt"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "F. Name"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Location"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Weight"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Deposit"))
        item = self.tableWidget_exist_5.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Deposit Date"))
        self.label_105.setText(_translate("MainWindow", "Add Deposit"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "Name"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "Location"))
        self.comboBox_4.setItemText(2, _translate("MainWindow", "Fingerprint"))
        self.label_106.setText(_translate("MainWindow", "Enter Deposit Amount "))
        self.pushButton_18.setText(_translate("MainWindow", "Search Record"))
        self.pushButton_19.setText(_translate("MainWindow", "Add Deposit"))
        item = self.tableWidget_5.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "User id"))
        item = self.tableWidget_5.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Amt"))
        item = self.tableWidget_5.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget_5.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "F. Name"))
        item = self.tableWidget_5.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Location"))
        item = self.tableWidget_5.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget_5.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget_5.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Weight"))
        item = self.tableWidget_5.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Deposit"))
        item = self.tableWidget_5.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "    Deposit Date"))
        self.label_107.setText(_translate("MainWindow", "View Records"))
        self.comboBox_removed_3.setItemText(0, _translate("MainWindow", "By Name"))
        self.comboBox_removed_3.setItemText(1, _translate("MainWindow", "By Date"))
        self.comboBox_removed_3.setItemText(2, _translate("MainWindow", "By Location"))
        self.pushButton_removed_3.setText(_translate("MainWindow", " Search Record"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "User_id"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Amt"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "F.Name"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Location"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Weight"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Deposit"))
        item = self.tableWidget_removed_9.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Deposit Date"))
        self.label_108.setText(_translate("MainWindow", "View Removed Records"))
        self.comboBox_removed_4.setItemText(0, _translate("MainWindow", "By Name"))
        self.comboBox_removed_4.setItemText(1, _translate("MainWindow", "By Date"))
        self.comboBox_removed_4.setItemText(2, _translate("MainWindow", "By Location"))
        self.pushButton_removed_4.setText(_translate("MainWindow", " Search Record"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "User_id"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Amt"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "F.Name"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Location"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Date"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Removed Date"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Type"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Weight"))
        item = self.tableWidget_removed_10.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Interest"))
        self.label_109.setText(_translate("MainWindow", "View Accounts"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Investment"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Returns"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Interest"))
        self.pushButton_removed_5.setText(_translate("MainWindow", "Generate "))
        '''
        self.toggleButton_13.setText(_translate("MainWindow", "1 month"))
        self.toggleButton_14.setText(_translate("MainWindow", "6 month"))
        self.toggleButton_15.setText(_translate("MainWindow", "1 year"))
        '''
        self.label_3.setText(_translate("MainWindow", ""))
        self.pushButton_removed_6.setText(_translate("MainWindow", "Save as Pdf"))
import resources


if __name__ == "__main__":
    import sys 
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
