import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import  QtWidgets
import resources
from tkinter import messagebox
import mysql.connector
import datetime


class LoginDialog1(QDialog):
    def call(self):
        self.con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="akshat",
        database="loan_management",
        auth_plugin="caching_sha2_password" 
        )

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Remove cash")
        self.setGeometry(0, 0, 300, 200)
        self.setFixedSize(300, 200)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Set the window icon (change 'icon.png' to the path of your desired icon file).
        self.setWindowIcon(QIcon("://icons/resources/icons/download.ico"))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.password_label = QLineEdit()
        self.password_label.setPlaceholderText("Enter Amount")
        #self.password_label.setEchoMode(QLineEdit.Password)
        self.password_label.setStyleSheet("QLineEdit { border:1px solid black }")
        self.password_label.setStyleSheet("padding: 10px; font-size: 20px; background-color: white; border: 1px solid #ccc; border-color:black;")

        self.login_button = QPushButton("Remove Cash")
        self.login_button.setStyleSheet("padding: 10px; background-color: rgb(255, 114, 43); color: white; font-weight: bold; font-size: 30px;")
        layout.addWidget(self.password_label)
        layout.addWidget(self.login_button)
        self.login_button.clicked.connect(self.removed_cash)
        self.incorrect_attempts = int(0)

    def removed_cash(self):
        self.call()
        amount = int(self.password_label.text())
        current_date = datetime.date.today()
        mycursor = self.con.cursor()
        try:
            query = '''UPDATE daily_assessment
                    SET removed_cash = COALESCE(removed_cash, 0) + %s
                    WHERE date = %s;'''
            values = (amount, current_date)
            mycursor.execute(query, values)
            self.con.commit()
            messagebox.showinfo("Success!","Cash Removed Successfully!!")
            self.close()
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_dialog = LoginDialog1()

    # Center the login dialog on the screen.
    center_point = app.desktop().availableGeometry().center()
    login_dialog.move(center_point - login_dialog.rect().center())

    login_dialog.show()
    sys.exit(app.exec_())
