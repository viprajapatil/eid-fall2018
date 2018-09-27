# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project1.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(389, 396)
        self.temp_label = QtWidgets.QLabel(Dialog)
        self.temp_label.setGeometry(QtCore.QRect(40, 10, 131, 21))
        self.temp_label.setObjectName("temp_label")
        self.hum_label = QtWidgets.QLabel(Dialog)
        self.hum_label.setGeometry(QtCore.QRect(250, 10, 111, 21))
        self.hum_label.setObjectName("hum_label")
        self.refresh_temp = QtWidgets.QPushButton(Dialog)
        self.refresh_temp.setGeometry(QtCore.QRect(30, 110, 101, 31))
        self.refresh_temp.setObjectName("refresh_temp")
        self.refresh_hum = QtWidgets.QPushButton(Dialog)
        self.refresh_hum.setGeometry(QtCore.QRect(240, 110, 101, 31))
        self.refresh_hum.setObjectName("refresh_hum")
        self.list_temp = QtWidgets.QListWidget(Dialog)
        self.list_temp.setGeometry(QtCore.QRect(20, 170, 141, 111))
        self.list_temp.setObjectName("list_temp")
        self.list_hum = QtWidgets.QListWidget(Dialog)
        self.list_hum.setGeometry(QtCore.QRect(220, 170, 151, 111))
        self.list_hum.setObjectName("list_hum")
        self.graph_temp = QtWidgets.QGraphicsView(Dialog)
        self.graph_temp.setGeometry(QtCore.QRect(10, 310, 161, 71))
        self.graph_temp.setObjectName("graph_temp")
        self.graph_hum = QtWidgets.QGraphicsView(Dialog)
        self.graph_hum.setGeometry(QtCore.QRect(210, 310, 161, 71))
        self.graph_hum.setObjectName("graph_hum")
        self.graph_temp_label = QtWidgets.QLabel(Dialog)
        self.graph_temp_label.setGeometry(QtCore.QRect(60, 290, 67, 21))
        self.graph_temp_label.setObjectName("graph_temp_label")
        self.graph_hum_label = QtWidgets.QLabel(Dialog)
        self.graph_hum_label.setGeometry(QtCore.QRect(260, 290, 67, 21))
        self.graph_hum_label.setObjectName("graph_hum_label")
        self.temp_value = QtWidgets.QLabel(Dialog)
        self.temp_value.setGeometry(QtCore.QRect(40, 40, 141, 20))
        self.temp_value.setObjectName("temp_value")
        self.hum_value = QtWidgets.QLabel(Dialog)
        self.hum_value.setGeometry(QtCore.QRect(250, 40, 151, 21))
        self.hum_value.setObjectName("hum_value")
        self.temp_time = QtWidgets.QLabel(Dialog)
        self.temp_time.setGeometry(QtCore.QRect(40, 70, 81, 21))
        self.temp_time.setObjectName("temp_time")
        self.hum_time = QtWidgets.QLabel(Dialog)
        self.hum_time.setGeometry(QtCore.QRect(250, 70, 81, 21))
        self.hum_time.setObjectName("hum_time")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.temp_label.setText(_translate("Dialog", "Temperature"))
        self.hum_label.setText(_translate("Dialog", "Humidity"))
        self.refresh_temp.setText(_translate("Dialog", "Refresh"))
        self.refresh_hum.setText(_translate("Dialog", "Refresh"))
        self.graph_temp_label.setText(_translate("Dialog", "Graph"))
        self.graph_hum_label.setText(_translate("Dialog", "Graph"))
        self.temp_value.setText(_translate("Dialog", "Current temperature"))
        self.hum_value.setText(_translate("Dialog", "Current Humidity"))
        self.temp_time.setText(_translate("Dialog", "Time"))
        self.hum_time.setText(_translate("Dialog", "Time"))

