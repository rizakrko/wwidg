#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from urllib import urlencode
import urllib2
import cookielib
import requests
import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.solid import Solid

from settings import SettingsDialog

class BWCBalancePlasmoid(plasmascript.Applet):

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        """Applet settings"""

        self.setHasConfigurationInterface(True)
        self.resize(300, 300)
        self.setAspectRatioMode(1)

        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)

        self.layout = QGraphicsGridLayout(self.applet)

        # Main label with balance value
        self.nameLabel = Plasma.Label(self.applet)
	self.descLabel = Plasma.Label(self.applet)
	self.tempLabel = Plasma.Label(self.applet)
	self.humLabel = Plasma.Label(self.applet)
	self.layout.addItem(self.descLabel,1,0)
	self.layout.addItem(self.nameLabel,0,0)
	self.layout.addItem(self.tempLabel,2,0)
	self.layout.addItem(self.humLabel,3,0)
        self.applet.setLayout(self.layout)


        # SettingsDialog instance
        # see: settings.py
        self.settings_dialog = None

        # User credentials
	self.City = ''


        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout(bool)"), self.update)

	def postInit(self):

       	 self.timer.start(1000*60*60)
         self.update()

    def update(self):
        """Update label text"""
	pre = 'http://api.openweathermap.org/data/2.5/weather?q=' 
	post = '&appid=653ea39c344cd35c73b76e3766770422'
	if self.City != None:
		tar = str(self.City)
		request = pre + tar + post
		r = requests.get(request)
		data = r.json()
		res = str(data['name']) + str(data['weather'][0]['description']) + str(data['main']['humidity'])
		self.nameLabel.setText(str(data['name']))
		self.descLabel.setText(str(data['weather'][0]['description']))
		self.tempLabel.setText(str(round(data['main']['temp'] - 273.15,1)) + ' C')
		self.humLabel.setText(str(data['main']['humidity']) + '%')
		self.descLabel.setStyleSheet('font: 16pt "Monaco"')
		self.humLabel.setStyleSheet('font: 16pt "Monaco"')
		self.tempLabel.setStyleSheet('font: 16pt "Monaco"')
		self.nameLabel.setStyleSheet('font: 16pt "Monaco";')
    def timerEvent(self, event):
	self.update()

    def showConfigurationInterface(self):
        """Show settings dialog"""

        self.settings_dialog = SettingsDialog(self)

        dialog = KPageDialog()
        dialog.setFaceType(KPageDialog.Plain)
        dialog.setButtons(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel))
        page = dialog.addPage(self.settings_dialog, "Settings")

        self.connect(dialog, SIGNAL("okClicked()"), self.configAccepted)
        self.connect(dialog, SIGNAL("cancelClicked()"), self.configDenied)

        dialog.resize(350, 200)
        dialog.exec_()

    def configAccepted(self):
        self.City = self.settings_dialog.get_settings()
	self.update()

    def configDenied(self):
        """Do nothing"""

        pass

def CreateApplet(parent):
    return BWCBalancePlasmoid(parent)
