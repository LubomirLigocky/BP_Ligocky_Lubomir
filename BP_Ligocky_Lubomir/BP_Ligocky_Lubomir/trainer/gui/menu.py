# -*- coding: utf-8 -*-
import json
import socket

################################################################################
## Form generated from reading UI file 'exercisewindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
                               QLayout, QMainWindow, QPushButton, QSizePolicy,
                               QWidget, QComboBox)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, active_socket, base_speach_lang: dict = {}, json_config: dict = {}):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        self.active_socket = active_socket
        self.json_config = json_config
        self.MainWindow = MainWindow
        self.base_speach_lang = base_speach_lang
        MainWindow.resize(1920,  2000)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.video_feed = QLabel(self.centralwidget)
        self.video_feed.setObjectName(u"video_feed")
        self.video_feed.setGeometry(QRect(19, 39, 1050, 600))
        self.video_feed.setMinimumSize(QSize(4, 0))
        self.video_feed.setMaximumSize(QSize(1280, 720))
        self.note_label = QLabel(self.centralwidget)
        self.note_label.setObjectName(u"note_label")
        self.note_label.setGeometry(QRect(100, 700, 1761, 81))
        font = QFont()
        font.setPointSize(40)
        self.note_label.setFont(font)
        self.note_label.setStyleSheet(u"color: rgb(119, 118, 123);\n"
"")
        self.note_label.setAlignment(Qt.AlignJustify|Qt.AlignVCenter)
        self.gridLayoutWidget_2 = QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(40, 600, 1521, 180))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)

        font1 = QFont()
        font1.setPointSize(12)


        self.squat_button = QPushButton(self.gridLayoutWidget_2)
        self.squat_button.setObjectName(u"squat_button")
        self.squat_button.setFont(font1)
        self.squat_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.squat_button, 1, 0, 1, 1)

        self.predpazovanie_button = QPushButton(self.gridLayoutWidget_2)
        self.predpazovanie_button.setObjectName(u"predpazovanie_button")
        self.predpazovanie_button.setFont(font1)
        self.predpazovanie_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.predpazovanie_button, 1, 1, 1, 1)

        self.tpose_button = QPushButton(self.gridLayoutWidget_2)
        self.tpose_button.setObjectName(u"tpose_button")
        self.tpose_button.setFont(font1)
        self.tpose_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.tpose_button, 1, 2, 1, 1)

        self.arm_circling_button = QPushButton(self.gridLayoutWidget_2)
        self.arm_circling_button.setObjectName(u"arm_circling_button")
        self.arm_circling_button.setFont(font1)
        self.arm_circling_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.arm_circling_button, 1, 3, 1, 1)


        self.forefooting_predpazovanie_button = QPushButton(self.gridLayoutWidget_2)
        self.forefooting_predpazovanie_button.setObjectName(u"forefooting_predpazovanie_button")
        self.forefooting_predpazovanie_button.setFont(font1)
        self.forefooting_predpazovanie_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.forefooting_predpazovanie_button, 2, 0, 1, 1)

        self.forefooting_rozpazovanie_button = QPushButton(self.gridLayoutWidget_2)
        self.forefooting_rozpazovanie_button.setObjectName(u"forefooting_rozpazovanie_button")
        self.forefooting_rozpazovanie_button.setFont(font1)
        self.forefooting_rozpazovanie_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.forefooting_rozpazovanie_button, 2, 1, 1, 1)

        self.knee_lifting_predpazovanie_button = QPushButton(self.gridLayoutWidget_2)
        self.knee_lifting_predpazovanie_button.setObjectName(u"knee_lifting_predpazovanie_button")
        self.knee_lifting_predpazovanie_button.setFont(font1)
        self.knee_lifting_predpazovanie_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.knee_lifting_predpazovanie_button, 2, 2, 1, 1)

        self.knee_lifting_rozpazovanie_button = QPushButton(self.gridLayoutWidget_2)
        self.knee_lifting_rozpazovanie_button.setObjectName(u"knee_lifting_rozpazovanie_button")
        self.knee_lifting_rozpazovanie_button.setFont(font1)
        self.knee_lifting_rozpazovanie_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.knee_lifting_rozpazovanie_button, 2, 3, 1, 1)

        self.arm_sit_circling_button = QPushButton(self.gridLayoutWidget_2)
        self.arm_sit_circling_button.setObjectName(u"arm_sit_circling_button")
        self.arm_sit_circling_button.setFont(font1)
        self.arm_sit_circling_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.arm_sit_circling_button, 3, 4, 1, 1)

        self.sit_stand_raise_arms_button = QPushButton(self.gridLayoutWidget_2)
        self.sit_stand_raise_arms_button.setObjectName(u"sit_stand_raise_arms_button")
        self.sit_stand_raise_arms_button.setFont(font1)
        self.sit_stand_raise_arms_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.sit_stand_raise_arms_button, 3, 0, 1, 1)

        self.chair_circling_button = QPushButton(self.gridLayoutWidget_2)
        self.chair_circling_button.setObjectName(u"chair_circling_button")
        self.chair_circling_button.setFont(font1)
        self.chair_circling_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.chair_circling_button, 3, 1, 1, 1)

        self.sadanie_na_stolicku_button = QPushButton(self.gridLayoutWidget_2)
        self.sadanie_na_stolicku_button.setObjectName(u"sadanie_na_stolicku_button")
        self.sadanie_na_stolicku_button.setFont(font1)
        self.sadanie_na_stolicku_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.sadanie_na_stolicku_button, 3, 2, 1, 1)

        self.forefooting_ruky_nad_hlavu_button = QPushButton(self.gridLayoutWidget_2)
        self.forefooting_ruky_nad_hlavu_button.setObjectName(u"forefooting_ruky_nad_hlavu_button")
        self.forefooting_ruky_nad_hlavu_button.setFont(font1)
        self.forefooting_ruky_nad_hlavu_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.forefooting_ruky_nad_hlavu_button, 3, 3, 1, 1)

        self.krizny_forefooting_in_lying_button = QPushButton(self.gridLayoutWidget_2)
        self.krizny_forefooting_in_lying_button.setObjectName(u"krizny_forefooting_in_lying_button")
        self.krizny_forefooting_in_lying_button.setFont(font1)
        self.krizny_forefooting_in_lying_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.krizny_forefooting_in_lying_button, 4, 0, 1, 1)

        self.forefooting_in_lying_button = QPushButton(self.gridLayoutWidget_2)
        self.forefooting_in_lying_button.setObjectName(u"forefooting_in_lying_button")
        self.forefooting_in_lying_button.setFont(font1)
        self.forefooting_in_lying_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.forefooting_in_lying_button, 4, 1, 1, 1)

        self.forefooting_ruky_pri_tele_button = QPushButton(self.gridLayoutWidget_2)
        self.forefooting_ruky_pri_tele_button.setObjectName(u"forefooting_ruky_pri_tele_button")
        self.forefooting_ruky_pri_tele_button.setFont(font1)
        self.forefooting_ruky_pri_tele_button.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_3.addWidget(self.forefooting_ruky_pri_tele_button, 4, 2, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 10)
        self.gridLayout_3.setColumnStretch(1, 10)
        self.gridLayout_3.setColumnStretch(2, 10)
        self.gridLayout_3.setColumnStretch(3, 10)
        self.gridLayout_3.setColumnStretch(4, 10)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(1100, 60, 450, 420))
        self.frame.setStyleSheet(u"border-color: rgb(0, 0, 0);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.config_button = QPushButton(self.frame)
        self.config_button.setObjectName(u"config_button")
        self.config_button.setGeometry(QRect(40, 360, 141, 41))
        font2 = QFont()
        font2.setFamilies([u"Ubuntu"])
        font2.setPointSize(14)
        font2.setBold(False)
        self.config_button.setFont(font2)
        self.config_button.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.config_button.setCheckable(False)
        self.end_button = QPushButton(self.frame)
        self.end_button.setObjectName(u"end_button")
        self.end_button.setGeometry(QRect(250, 360, 141, 41))
        self.end_button.setFont(font2)
        self.end_button.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.end_button.setCheckable(True)
        self.gridLayoutWidget = QWidget(self.frame)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(50, 10, 458, 297))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        font3 = QFont()
        font3.setFamilies([u"Roboto Condensed Light"])
        font3.setPointSize(22)
        font3.setBold(True)
        self.label_2.setFont(font3)
        self.label_2.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        font4 = QFont()
        font4.setFamilies([u"Ubuntu"])
        font4.setPointSize(20)
        font4.setBold(True)

        self.timer_label = QLabel(self.gridLayoutWidget)
        self.timer_label.setObjectName(u"timer_label")
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(40)
        font5.setBold(True)
        self.timer_label.setFont(font5)
        self.timer_label.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.timer_label.setTextFormat(Qt.PlainText)

        self.gridLayout_2.addWidget(self.timer_label, 1, 1, 1, 1)

        self.score_label = QLabel(self.gridLayoutWidget)
        self.score_label.setObjectName(u"score_label")
        font6 = QFont()
        font6.setFamilies([u"Ubuntu"])
        font6.setPointSize(50)
        font6.setBold(True)
        self.score_label.setFont(font6)
        self.score_label.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.score_label.setTextFormat(Qt.PlainText)

        self.gridLayout_2.addWidget(self.score_label, 0, 1, 1, 1)

        self.distance_label_score = QLabel(self.gridLayoutWidget)
        self.distance_label_score.setObjectName(u"distance_label_score")
        self.distance_label_score.setFont(font)
        self.distance_label_score.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_2.addWidget(self.distance_label_score, 3, 1, 1, 1)

        self.distance_label = QLabel(self.gridLayoutWidget)
        self.distance_label.setObjectName(u"distance_label")
        font7 = QFont()
        font7.setPointSize(22)
        font7.setBold(False)
        self.distance_label.setFont(font7)
        self.distance_label.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_2.addWidget(self.distance_label, 3, 0, 1, 1)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        font8 = QFont()
        font8.setFamilies([u"Roboto Condensed Light"])
        font8.setPointSize(21)
        font8.setBold(True)
        self.label.setFont(font8)
        self.label.setStyleSheet(u"color: rgb(0, 0, 0);")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_2.raise_()
        self.timer_label.raise_()
        self.score_label.raise_()
        self.distance_label_score.raise_()
        self.distance_label.raise_()
        self.label.raise_()
        self.kamera_1 = QPushButton(self.centralwidget)
        self.kamera_1.setObjectName(u"kamera_1")
        self.kamera_1.setGeometry(QRect(0, 0, 91, 31))


        font9 = QFont()
        font9.setPointSize(14)
        self.kamera_1.setFont(font9)
        self.kamera_1.setStyleSheet(u"color: rgb(0, 0, 0);")
        self.kamera_2 = QPushButton(self.centralwidget)
        self.kamera_2.setObjectName(u"kamera_2")
        self.kamera_2.setGeometry(QRect(110, 0, 91, 31))
        self.kamera_2.setFont(font9)
        self.kamera_2.setStyleSheet(u"color: rgb(0, 0, 0);")
        MainWindow.setCentralWidget(self.centralwidget)

        self.lang_select = QComboBox(self.centralwidget)
        self.lang_select.addItems(["SK", "EN"])
        self.lang_select.currentTextChanged.connect(self.lang_changed)
        font10 = QFont()
        font10.setPointSize(14)
        font10.setBold(True)
        self.lang_select.setFont(font10)
        #self.gridLayout_2.addWidget(self.lang_select, 0, 0, 1, 1)

        self.retranslateUi(MainWindow, base_speach_lang)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi
    def lang_changed(self, lang):
        print("Language changed to: " + str(lang))
        self.__load_base_config(lang)
        self.retranslateUi(self.MainWindow, self.base_speach_lang)
        self.__update_language(lang)

    def __update_language(self, lang: str):
        try:
            if self.active_socket == None:

                ip_adress = (self.json_config["server_ip"], int(self.json_config["server_port"]))

                self.active_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.active_socket.connect(ip_adress)
                self.active_socket.setblocking(False) # Necessary, dont change or program will freeze
            config_message = "lang;" + str(lang)

            print("Updating language...", config_message)
            self.active_socket.sendall(config_message.encode())
        except:
            print("Cannot update language...", config_message)

    def __load_base_config(self, lang):
        path_to_base_file = "lang/" + str(lang.lower()) + ".json"

        with open(path_to_base_file, "r", encoding="utf-8") as file:
            self.base_speach_lang = json.loads(file.read())

    def retranslateUi(self, MainWindow, base_speach_lang: dict = {}):
        main_title_text = base_speach_lang.get("ui_buttons", {}).get("main_title",
                                                                      "MainWindow")
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", main_title_text, None))
        self.video_feed.setText("")
        self.note_label.setText("")
        leg_lifting_text = base_speach_lang.get("ui_buttons", {}).get("leg_lifting", "Zdv\u00edhanie n\u00f4h + ruky pri tele")
        predpazovanie_text = base_speach_lang.get("ui_buttons", {}).get("predpazovanie", "Predpažovanie")
        upazovanie_text = base_speach_lang.get("ui_buttons", {}).get("upazovanie", "Upa\u017eovanie")
        squats_text = base_speach_lang.get("ui_buttons", {}).get("squats", "Drepy")
        configuration_text = base_speach_lang.get("ui_buttons", {}).get("configuration", "Konfigur\u00e1cia")
        weaving_arms_in_sitting_text = base_speach_lang.get("ui_buttons", {}).get("weaving_arms_in_sitting", "V sede kruzenie rukami")
        weaving_arms_in_standing_text = base_speach_lang.get("ui_buttons", {}).get("weaving_arms_in_standing",
                                                                                  "V stoji kruzenie rukami")
        raising_feets_rozpazovanie_text = base_speach_lang.get("ui_buttons", {}).get("raising_feets_rozpazovanie",
                                                                                  "Zdv\u00edhanie n\u00f4h + rozpa\u017eenie")
        raising_feets_hands_up_text = base_speach_lang.get("ui_buttons", {}).get("raising_feets_hands_up", "Zdv\u00edhanie n\u00f4h + ruky nad hlavu")
        sitting_raising_hands_text = base_speach_lang.get("ui_buttons", {}).get("sitting_raising_hands", "Sadanie a zdv\u00edhanie r\u00fak")
        sitting_raising_hands_predpazovanie_text = base_speach_lang.get("ui_buttons", {}).get("sitting_raising_hands_predpazovanie",
                                                                                "Zdv\u00edhanie n\u00f4h + predpa\u017eovanie")
        knee_lifting_rozpazovanie_text = base_speach_lang.get("ui_buttons", {}).get("knee_lifting_rozpazovanie",
                                                                                "Zdv\u00edhanie kolien + upa\u017eovanie")
        knee_lifting_predpazovanie_text = base_speach_lang.get("ui_buttons", {}).get("knee_lifting_predpazovanie",
                                                                                "Zdv\u00edhanie kolien + predpa\u017eovanie")

        self.forefooting_ruky_pri_tele_button.setText(QCoreApplication.translate("MainWindow", leg_lifting_text, None))
        self.forefooting_rozpazovanie_button.setText(QCoreApplication.translate("MainWindow", raising_feets_rozpazovanie_text, None))
        self.tpose_button.setText(QCoreApplication.translate("MainWindow", upazovanie_text, None))
        self.squat_button.setText(QCoreApplication.translate("MainWindow", squats_text, None))
        self.predpazovanie_button.setText(QCoreApplication.translate("MainWindow", predpazovanie_text, None))
        self.sadanie_na_stolicku_button.setText(QCoreApplication.translate("MainWindow", u"Sadanie na stoli\u010dku", None))
        self.forefooting_ruky_nad_hlavu_button.setText(QCoreApplication.translate("MainWindow", raising_feets_hands_up_text, None))
        self.arm_circling_button.setText(QCoreApplication.translate("MainWindow", weaving_arms_in_standing_text, None))
        self.sit_stand_raise_arms_button.setText(QCoreApplication.translate("MainWindow", sitting_raising_hands_text, None))
        self.forefooting_predpazovanie_button.setText(QCoreApplication.translate("MainWindow", sitting_raising_hands_predpazovanie_text, None))
        self.arm_sit_circling_button.setText(QCoreApplication.translate("MainWindow", weaving_arms_in_sitting_text, None))
        self.knee_lifting_rozpazovanie_button.setText(QCoreApplication.translate("MainWindow", knee_lifting_rozpazovanie_text, None))
        self.knee_lifting_predpazovanie_button.setText(
            QCoreApplication.translate("MainWindow", knee_lifting_predpazovanie_text, None))

        self.forefooting_in_lying_button.setText(QCoreApplication.translate("MainWindow", u"Predno\u017eovanie v \u013eahu", None))
        self.krizny_forefooting_in_lying_button.setText(QCoreApplication.translate("MainWindow", u"Predno\u017eovanie do kr\u00ed\u017ea v \u013eahu", None))
        self.chair_circling_button.setText(QCoreApplication.translate("MainWindow", u"Obch\u00e1dzanie okolo  stoli\u010dky", None))
        self.config_button.setText(QCoreApplication.translate("MainWindow", configuration_text, None))

        finish_text = base_speach_lang.get("ui_buttons", {}).get("finish", "Koniec")
        time_text = base_speach_lang.get("ui_buttons", {}).get("time", "Time")
        distance_text = base_speach_lang.get("ui_buttons", {}).get("distance", "Time")
        number_repetition_text = base_speach_lang.get("ui_buttons", {}).get("number_repetitions", "Počet opakovaní:")
        camera_text = base_speach_lang.get("ui_buttons", {}).get("camera", "Kamera")
        self.end_button.setText(QCoreApplication.translate("MainWindow", finish_text, None))
        self.label_2.setText(QCoreApplication.translate("MainWindow",  time_text, None))
        self.timer_label.setText("")
        self.score_label.setText("")
        self.distance_label_score.setText("")
        self.distance_label.setText(QCoreApplication.translate("MainWindow", distance_text, None))
        self.label.setText(QCoreApplication.translate("MainWindow", number_repetition_text, None))
        self.kamera_1.setText(QCoreApplication.translate("MainWindow", camera_text, None))
        self.kamera_2.setText(QCoreApplication.translate("MainWindow", u"Kamera 2", None))
    # retranslateUi

