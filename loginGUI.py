from PyQt5 import QtCore, QtGui, QtWidgets
from mainGUItest import Ui_Form1
import login2_rc
import subprocess
import hashlib
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1400, 850)
        Form.setStyleSheet("background-image: url(:/login/Screenshot 2023-07-09 163610.png);")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, -10, 821, 211))
        self.label.setStyleSheet("\n"
                                  "font: 28pt \"Stencil\";\n"
                                  "color:rgb(15, 29, 70);")
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(170, 190, 511, 601))
        self.widget.setStyleSheet("\n"
                                   "\n"
                                   "background: url(:/finger/abstract-grunge-decorative-relief-navy-blue-stucco-wall-texture-wide-angle-rough-colored-background.jpg);")
        self.widget.setObjectName("widget")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(190, 60, 181, 81))
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 35pt \"MS Shell Dlg 2\";\n"
                                    "no-backgrond;\n"
                                    "")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(20, 200, 141, 71))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 20pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(20, 340, 171, 31))
        self.label_4.setStyleSheet("font: 75 20pt \"MS Shell Dlg 2\";\n"
                                    "color:rgb(255, 255, 255);")
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(190, 500, 131, 31))
        self.pushButton.setStyleSheet("background: rgb(255, 255, 255);\n"
                                        "font: 12pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 270, 461, 31))
        self.lineEdit.setStyleSheet("background: rgb(255, 255, 255);\n"
                                    "color: rgb(0, 0, 0);\n"
                                    "font: 75 12pt \"MS Shell Dlg 2\";")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)  # Hide password input
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 400, 461, 31))
        self.lineEdit_2.setStyleSheet("background: rgb(255, 255, 255);\n"
                                        "color: rgb(0, 0, 0);\n"
                                        "font: 75 12pt \"MS Shell Dlg 2\";")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)  # Hide password input

        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(160, 560, 141, 21))
        self.label_5.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
                                     "color: rgb(255, 255, 255);")  
        self.label_5.setObjectName("label_5")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 560, 81, 25))
        self.pushButton_2.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";\n"
                                     "color: rgb(255, 255, 255);\n""")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.pushButton.clicked.connect(self.show_new_gui)
        self.lineEdit_2.returnPressed.connect(self.show_new_gui)
        self.lineEdit.returnPressed.connect(self.show_new_gui)  # Handle returnPressed signal
        self.pushButton_2.clicked.connect(self.execute_open)
        

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Criminal Face Detection System"))
        self.label_2.setText(_translate("Form", "Login"))
        self.label_3.setText(_translate("Form", "UserID"))
        self.label_4.setText(_translate("Form", "Password"))
        self.pushButton.setText(_translate("Form", "Login"))
        self.label_5.setText(_translate("Form", "New user? "))
        self.pushButton_2.setText(_translate("Form", "signup"))
        

    def show_new_gui(self):
        userID = self.lineEdit.text()
        entered_password = self.lineEdit_2.text()

        entered_hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()

        with open("Employee_Passwords.txt", "r") as file:
            for line in file:
                stored_username, stored_hashed_password = line.strip().split(" ")
                if userID == stored_username and entered_hashed_password == stored_hashed_password:
                    Form.close()
                    upload_process = subprocess.Popen([sys.executable, "mainGUItest.py"])
                    upload_process.wait()

        QtWidgets.QMessageBox.warning(Form, "Login Failed", "Invalid username or password.")
    

    #def validate_credentials(self):
        #self.show_new_gui()
        
        
    def execute_open(self):
       # self.show_waiting_message()
        Form.close()
        upload_process = subprocess.Popen([sys.executable, "Signup.py"])
        upload_process.wait()
        QMessageBox().close()
   




    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())