from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QCheckBox, QHBoxLayout
from PyQt5.QtCore import *
from main import *
import sys


class CreateAccountWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = connectdb()
        self.top = 100
        self.left = 100
        self.setFixedSize(680, 500)
        self.setWindowTitle("Create Account")
        layout = QHBoxLayout()

        self.firstname = QLabel("First Name:", self)
        self.lastname = QLabel("Last Name:", self)
        self.email = QLabel("Email:", self)
        self.username = QLabel("Username:", self)
        self.password = QLabel("Password:", self)
        self.firstname_edit = QLineEdit(self)
        self.lastname_edit = QLineEdit(self)
        self.email_edit = QLineEdit(self)
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.location = QLabel("Collect Location Information?", self)
        self.location.adjustSize()
        self.locationYes = QCheckBox("Yes", self)
        self.locationNo = QCheckBox("No", self)
        self.locationNo.stateChanged.connect(self.onStateChange)
        self.locationYes.stateChanged.connect(self.onStateChange)
        self.locationNo.setChecked(True)

        self.btn_create_account = QPushButton("Create Account", self)

        self.firstname.move(30, 50)
        self.firstname_edit.move(100, 50)
        self.lastname.move(30, 100)
        self.lastname_edit.move(100, 100)
        self.email.move(30, 150)
        self.email_edit.move(100, 150)
        self.username.move(30, 200)
        self.username_edit.move(100, 200)
        self.password.move(30, 250)
        self.password_edit.move(100, 250)
        self.location.move(30, 300)
        self.locationYes.move(100, 350)
        self.locationNo.move(150, 350)
        self.btn_create_account.move(30, 400)

        self.btn_create_account.clicked.connect(lambda: self.createAccount())

    def createAccount(self):
        print("Name: ", self.firstname_edit.text(), " ", self.lastname_edit.text(), "\n")
        print("Email Address: ", self.email_edit.text(), "\n")
        print("Username selected: ", self.username_edit.text(), "\n")
        print("Password entered: ", self.password_edit.text(), "\n")
        if self.locationYes.isChecked():
            print("Location gathering allowed\n")
            p_addaccount(self.db, self.email_edit.text(), self.username_edit.text(), self.password_edit.text(), "yes")
        elif self.locationNo.isChecked():
            print("Location gathering not allowed\n")
            p_addaccount(self.db, self.email_edit.text(), self.username_edit.text(), self.password_edit.text(), "no")

        self.w = SignInWindow()
        self.w.show()
        self.hide()

    def onStateChange(self, state):
        if state == Qt.Checked:
            if self.sender() == self.locationNo:
                self.locationYes.setChecked(False)
            elif self.sender() == self.locationYes:
                self.locationNo.setChecked(False)



class SignInWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.db = connectdb()
        self.username = QLabel('Username:', self)
        self.password = QLabel('Password:', self)
        self.username_edit = QLineEdit(self)
        self.password_edit = QLineEdit(self)
        self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_sign_in = QPushButton('Sign In', self)
        self.btn_create_account = QPushButton('Create Account', self)

        self.username.move(30, 50)
        self.username_edit.move(100, 50)
        self.password.move(30, 100)
        self.password_edit.move(100, 100)
        self.btn_sign_in.move(30, 150)
        self.btn_create_account.move(100, 150)

        self.btn_sign_in.clicked.connect(lambda: self.signIn())
        self.btn_create_account.clicked.connect(lambda: self.create_account_window())
        self.sign_in_window()

    def sign_in_window(self):
        self.setWindowTitle("Sign In")
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def create_account_window(self):
        self.w = CreateAccountWindow()
        self.w.show()
        self.hide()

    def signIn(self):
        p_signin(self.db, self.username_edit.text(), self.password_edit.text())


def main():
    app = QApplication(sys.argv)
    ex = SignInWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    print("Before turning off hash randomization")
    os.environ["PYTHONHASHSEED"] = "0"
    print("After turning off hash randomization")
    main()