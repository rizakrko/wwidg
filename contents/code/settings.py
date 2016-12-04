#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Settings dialog with cellphone number and ISSA password
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kio import *
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

from settings_ui import Ui_SettingsDialog


class SettingsDialog(QWidget, Ui_SettingsDialog):
    """Settings form for BWCBalance-plasmoid"""

    def __init__(self, parent=None):
        QWidget.__init__(self)

        self.parent = parent
        self.setupUi(self)

        # Load settings from KWallet and populate settings form
        self.wallet = KWallet.Wallet.openWallet(KWallet.Wallet.LocalWallet(), 0)
        if self.wallet:
            self.wallet.setFolder("bwc-balance-plasmoid")

            if not self.wallet.entryList().isEmpty():
                phone = str(self.wallet.entryList().first())
                password = QString()
                self.wallet.readPassword(phone, password)
                self.textPhone.setText(phone)
                self.textPassword.setText(str(password))

    def get_city(self):
        """Returns user-inputed credentials"""

        return str(self.City.text())
    def get_weekly(self):
        return self.fiveDays.isChecked()
