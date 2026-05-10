# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'config_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGroupBox, QLabel, QLineEdit,
    QRadioButton, QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(519, 508)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 20, 111, 21))
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.serverIP_edit = QLineEdit(Dialog)
        self.serverIP_edit.setObjectName(u"serverIP_edit")
        self.serverIP_edit.setGeometry(QRect(30, 50, 161, 31))
        font1 = QFont()
        font1.setPointSize(12)
        self.serverIP_edit.setFont(font1)
        self.serverIP_edit.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.virtual_robot_ip = QLineEdit(Dialog)
        self.virtual_robot_ip.setObjectName(u"virtual_robot_ip")
        self.virtual_robot_ip.setGeometry(QRect(30, 210, 161, 31))
        self.virtual_robot_ip.setFont(font1)
        self.virtual_robot_ip.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(30, 180, 151, 21))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.physical_checkBox = QCheckBox(Dialog)
        self.physical_checkBox.setObjectName(u"physical_checkBox")
        self.physical_checkBox.setGeometry(QRect(250, 50, 131, 21))
        self.physical_checkBox.setFont(font)
        self.physical_checkBox.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 100, 111, 21))
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.serverPort_edit = QLineEdit(Dialog)
        self.serverPort_edit.setObjectName(u"serverPort_edit")
        self.serverPort_edit.setGeometry(QRect(30, 130, 161, 31))
        self.serverPort_edit.setFont(font1)
        self.serverPort_edit.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.emotions_checkBox = QCheckBox(Dialog)
        self.emotions_checkBox.setObjectName(u"emotions_checkBox")
        self.emotions_checkBox.setGeometry(QRect(250, 90, 191, 21))
        self.emotions_checkBox.setFont(font)
        self.emotions_checkBox.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(30, 260, 171, 21))
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.physical_robot_ip = QLineEdit(Dialog)
        self.physical_robot_ip.setObjectName(u"physical_robot_ip")
        self.physical_robot_ip.setGeometry(QRect(30, 290, 161, 31))
        self.physical_robot_ip.setFont(font1)
        self.physical_robot_ip.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.accept_button = QDialogButtonBox(Dialog)
        self.accept_button.setObjectName(u"accept_button")
        self.accept_button.setGeometry(QRect(70, 410, 271, 51))
        self.accept_button.setFont(font)
        self.accept_button.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.accept_button.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.exercise_loop_input = QLineEdit(Dialog)
        self.exercise_loop_input.setObjectName(u"exercise_loop_input")
        self.exercise_loop_input.setGeometry(QRect(250, 170, 161, 31))
        self.exercise_loop_input.setFont(font1)
        self.exercise_loop_input.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_exercise_loop = QLabel(Dialog)
        self.label_exercise_loop.setObjectName(u"label_exercise_loop")
        self.label_exercise_loop.setGeometry(QRect(250, 140, 171, 21))
        self.label_exercise_loop.setFont(font)
        self.label_exercise_loop.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(240, 220, 241, 91))
        self.radioButton_male = QRadioButton(self.groupBox)
        self.radioButton_male.setObjectName(u"radioButton_male")
        self.radioButton_male.setGeometry(QRect(10, 60, 100, 21))
        font2 = QFont()
        font2.setPointSize(14)
        self.radioButton_male.setFont(font2)
        self.radioButton_male.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.radioButton_female = QRadioButton(self.groupBox)
        self.radioButton_female.setObjectName(u"radioButton_female")
        self.radioButton_female.setGeometry(QRect(140, 60, 100, 21))
        self.radioButton_female.setFont(font2)
        self.radioButton_female.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.label_gender = QLabel(self.groupBox)
        self.label_gender.setObjectName(u"label_gender")
        self.label_gender.setGeometry(QRect(10, 10, 191, 21))
        self.label_gender.setFont(font)
        self.label_gender.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Server IP", None))
        self.serverIP_edit.setText(QCoreApplication.translate("Dialog", u"127.0.0.1", None))
        self.virtual_robot_ip.setText(QCoreApplication.translate("Dialog", u"127.0.0.1", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Virtual Robot IP", None))
        self.physical_checkBox.setText(QCoreApplication.translate("Dialog", u"Physical", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"Server port", None))
        self.serverPort_edit.setText(QCoreApplication.translate("Dialog", u"1234", None))
        self.emotions_checkBox.setText(QCoreApplication.translate("Dialog", u"Detect Emotions", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Physical Robot IP", None))
        self.physical_robot_ip.setText(QCoreApplication.translate("Dialog", u"127.0.0.1", None))
        self.exercise_loop_input.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.label_exercise_loop.setText(QCoreApplication.translate("Dialog", u"Exercise duration", None))
        self.groupBox.setTitle("")
        self.radioButton_male.setText(QCoreApplication.translate("Dialog", u"Male", None))
        self.radioButton_female.setText(QCoreApplication.translate("Dialog", u"Female", None))
        self.label_gender.setText(QCoreApplication.translate("Dialog", u"Participant gender", None))
    # retranslateUi

