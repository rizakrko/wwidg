# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_ui.ui'
#
# Created: Sun Dec  4 04:34:00 2016
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.resize(333, 121)
        self.gridLayoutWidget = QtGui.QWidget(SettingsDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 333, 121))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(12)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fiveDays = QtGui.QRadioButton(self.gridLayoutWidget)
        self.fiveDays.setObjectName(_fromUtf8("fiveDays"))
        self.horizontalLayout.addWidget(self.fiveDays)
        self.City = QtGui.QLineEdit(self.gridLayoutWidget)
        self.City.setInputMask(_fromUtf8(""))
        self.City.setMaxLength(10)
        self.City.setEchoMode(QtGui.QLineEdit.Normal)
        self.City.setObjectName(_fromUtf8("City"))
        self.horizontalLayout.addWidget(self.City)
        self.daily = QtGui.QRadioButton(self.gridLayoutWidget)
        self.daily.setObjectName(_fromUtf8("daily"))
        self.horizontalLayout.addWidget(self.daily)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 2, 1, 1)

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "BWC Balance settings", None))
        self.fiveDays.setText(_translate("SettingsDialog", "5 days", None))
        self.daily.setText(_translate("SettingsDialog", "daily", None))

