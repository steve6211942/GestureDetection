# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'yibajiu.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1334, 1036)
        self.label_camera_up = QtWidgets.QLabel(Form)
        self.label_camera_up.setGeometry(QtCore.QRect(20, 10, 500, 500))
        self.label_camera_up.setText("")
        self.label_camera_up.setObjectName("label_camera_up")
        self.label_camera_down = QtWidgets.QLabel(Form)
        self.label_camera_down.setGeometry(QtCore.QRect(20, 530, 500, 500))
        self.label_camera_down.setText("")
        self.label_camera_down.setObjectName("label_camera_down")
        self.label_roi_u = QtWidgets.QLabel(Form)
        self.label_roi_u.setGeometry(QtCore.QRect(609, 20, 281, 250))
        self.label_roi_u.setText("")
        self.label_roi_u.setObjectName("label_roi_u")
        self.label_cnt_u = QtWidgets.QLabel(Form)
        self.label_cnt_u.setGeometry(QtCore.QRect(979, 20, 281, 250))
        self.label_cnt_u.setText("")
        self.label_cnt_u.setObjectName("label_cnt_u")
        self.label_roi_d = QtWidgets.QLabel(Form)
        self.label_roi_d.setGeometry(QtCore.QRect(609, 290, 281, 250))
        self.label_roi_d.setText("")
        self.label_roi_d.setObjectName("label_roi_d")
        self.label_cnt_d = QtWidgets.QLabel(Form)
        self.label_cnt_d.setGeometry(QtCore.QRect(979, 290, 281, 250))
        self.label_cnt_d.setText("")
        self.label_cnt_d.setObjectName("label_cnt_d")
        self.label_text = QtWidgets.QLabel(Form)
        self.label_text.setGeometry(QtCore.QRect(550, 559, 761, 461))
        self.label_text.setText("")
        self.label_text.setObjectName("label_text")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


