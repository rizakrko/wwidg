#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from urllib import urlencode
import urllib2
import cookielib
import requests
import json
import datetime

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui
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

        self.step = 0
        self.wasWeekly = 0
        self.wasDaily = 0
        self.layout = QGraphicsGridLayout(self.applet)


        self.createOneDayLayout()

        self.setOneDayLayout()

        # SettingsDialog instance
        # see: settings.py
        self.settings_dialog = None

        # User credentials
        self.City = ''
        self.weekly = 1
        self.path = "/home/draed/wwidg/contents/images/"

        self.timer = QTimer()
        self.connect(self.timer, SIGNAL("timeout(bool)"), self.update)

        def postInit(self):
            self.timer.start(1000 * 60 * 60)
            self.update()

    def update(self):
        """Update label text"""
        pre = 'http://api.openweathermap.org/data/2.5/weather?q='
        if self.weekly:
            pre = 'http://api.openweathermap.org/data/2.5/forecast?q='
        post = '&appid=653ea39c344cd35c73b76e3766770422'
        if self.City != None:
            tar = str(self.City)
            request = pre + tar + post
            r = requests.get(request)
            self.data = r.json()

            if self.weekly:
                if self.wasDaily:
                    self.clear1()
                    self.wasDaily = 0
                self.createFiveDaysLayout()
                self.setWeekLayout()
                self.setFiveDaysData()
            else:
                if self.wasWeekly:
                    self.clear2()
                    self.wasWeekly = 0
                self.createOneDayLayout()
                self.setOneDayLayout()
                self.setOneDayData()

    def createOneDayLayout(self):

        self.layout.setColumnMaximumWidth(0, 300)
        self.wasDaily = 1
        self.clearLayout()
        self.resize(300, 300)

        self.nameLabel = Plasma.Label(self.applet)
        self.descLabel = Plasma.Label(self.applet)
        self.tempLabel = Plasma.Label(self.applet)
        self.humLabel = Plasma.Label(self.applet)
        self.layout.addItem(self.descLabel, 1, 0)
        self.layout.addItem(self.nameLabel, 0, 0)
        self.layout.addItem(self.tempLabel, 2, 0)
        self.layout.addItem(self.humLabel, 3, 0)

    def setOneDayData(self):
        self.nameLabel.setText(str(self.data['name']))
        self.descLabel.setText(str(self.data['weather'][0]['description']))
        self.tempLabel.setText(str(round(self.data['main']['temp'] - 273.15, 1)) + ' C')
        self.humLabel.setText(str(self.data['main']['humidity']) + '%')
        self.descLabel.setStyleSheet('font: 16pt "Monaco"')
        self.humLabel.setStyleSheet('font: 16pt "Monaco"')
        self.tempLabel.setStyleSheet('font: 16pt "Monaco"')
        self.nameLabel.setStyleSheet('font: 16pt "Monaco";')

    def createFiveDaysLayout(self):

        self.layout.setColumnMaximumWidth(0, 90)

        self.clearLayout()
        self.wasWeekly = 1

        self.resize(540, 300)

        """top"""
        self.dayLabels = []
        self.descLabels = []
        self.tempLabels = []
        self.timeBotLabels = []
        self.descBotLabels = []
        self.tempBotLabels = []
        self.humBotLabels = []
        for i in range(4):
            self.dayLabels.append(Plasma.Label(self.applet))
            self.descLabels.append(Plasma.Label(self.applet))
            self.tempLabels.append(Plasma.Label(self.applet))
            self.timeBotLabels.append(Plasma.Label(self.applet))
            self.descBotLabels.append(Plasma.Label(self.applet))
            self.tempBotLabels.append(Plasma.Label(self.applet))
            self.humBotLabels.append(Plasma.Label(self.applet))


        for i in range(4):
            self.layout.addItem(self.dayLabels[i], 0, i + 1)
            self.layout.addItem(self.descLabels[i], 1, i + 1)
            self.layout.addItem(self.tempLabels[i], 2, i + 1)
            self.layout.addItem(self.timeBotLabels[i], 3, i + 1)
            self.layout.addItem(self.descBotLabels[i], 4, i + 1)
            self.layout.addItem(self.tempBotLabels[i], 5, i + 1)
            self.layout.addItem(self.humBotLabels[i], 6, i + 1)

        self.tempLabelBot = Plasma.Label(self.applet)
        self.humLabelBot = Plasma.Label(self.applet)
        self.layout.addItem(self.tempLabelBot, 5, 0)
        self.layout.addItem(self.humLabelBot, 6, 0)
        self.tempLabelBot.setText("Temperature, C:")
        self.humLabelBot.setText("Humidity, %:")

        self.NameLabel = Plasma.Label(self.applet)
        self.DescLabel = Plasma.Label(self.applet)
        self.TempLabel = Plasma.Label(self.applet)
        self.layout.addItem(self.NameLabel, 0,0)
        self.layout.addItem(self.DescLabel, 2,0)
        self.layout.addItem(self.TempLabel, 1,0)



        #btns
        self.rightButtn = Plasma.PushButton(self.applet)
        self.leftButton = Plasma.PushButton(self.applet)
        self.rightButtn.setText("Next")
        self.leftButton.setText("Prev")
        self.connect(self.rightButtn, SIGNAL("clicked()"), self.nextDay)
        self.connect(self.leftButton, SIGNAL("clicked()"), self.prevDay)
        self.layout.addItem(self.rightButtn, 0, 6)
        self.layout.addItem(self.leftButton, 6, 6)


    def setFiveDaysData(self):

        for i in range(4):
            stam = self.data['list'][0 + 8*i]['dt']
            value = datetime.datetime.fromtimestamp(stam).strftime('%a')
            value2 = datetime.datetime.fromtimestamp(stam).strftime('%d %b')
            self.dayLabels[i].setText(value + '\n' + value2)
            self.descLabels[i].setImage(self.path + self.data['list'][0 + 8*i]['weather'][0]['icon'] + ".png")
            min = str(round(self.data['list'][0 + 8*i]['main']['temp_min'] - 273.15, 1))
            max = str(round(self.data['list'][0 + 8*i]['main']['temp_max'] - 273.15, 1))
            self.tempLabels[i].setText("Min. " + "Max.\n"+ min + "  " + max)

        # bot

        self.setBot()

        #left
        #self.NameLabel.setText(self.data['city']['name'])
        stam = self.data['list'][0]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%d')
        self.NameLabel.setText("Weather today,\n  " + value + ':00')
        self.DescLabel.setImage(self.path + self.data['list'][0]['weather'][0]['icon'] + ".png")
        self.TempLabel.setText(str(round(self.data['list'][0]['main']['temp'] - 273.15, 1)) + 'C')

        self.prevDay()


    def setBot(self):
        if self.step > 3:
            self.step -= 1
        if self.step < 0:
            self.step = 0

	for i in range(4):
		self.dayLabels[i].setStyleSheet("")
	self.dayLabels[self.step].setStyleSheet("color: red")

        for i in range(4):
            stam = self.data['list'][i*2 + 8*self.step]['dt']
            value = datetime.datetime.fromtimestamp(stam).strftime('%H' + ':00')
            self.timeBotLabels[i].setText(value)
            self.descBotLabels[i].setImage(self.path + self.data['list'][i*2 + 8*self.step]['weather'][0]['icon'] + ".png")
            temp = str(round(self.data['list'][i*2 + 8*self.step]['main']['temp'] - 273.15, 1))
            self.tempBotLabels[i].setText(temp)
            self.humBotLabels[i].setText(str(self.data['list'][i*2 + 8*self.step]['main']['humidity']) + "%")


    def clearLayout(self):
        while self.layout.count():
            #self.layout.removeAt(0)
            self.layout.removeItem(self.layout.itemAt(0))

    def clearLayoutt(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayoutt(child.layout())

    def clear2(self):

        for i in range(4):
            self.dayLabels[i].setText("")
            self.descLabels[i].setText("")
            self.descLabels[i] = 0
            self.tempLabels[i].setText("")
            self.timeBotLabels[i].setText("")
            self.tempBotLabels[i].setText("")
            self.descBotLabels[i] = 0
            self.humBotLabels[i].setText("")
            self.humLabelBot = 0
            self.tempLabelBot = 0
            self.NameLabel = 0
            self.DescLabel = 0
            self.TempLabel = 0

        self.rightButtn = None
        self.leftButton = None

    def clear1(self):
        self.nameLabel = None
        self.descLabel = None
        self.tempLabel = None
        self.humLabel = None

    def timerEvent(self, event):
        self.update()

    def prevDay(self):

        self.step -= 1
	
        self.setBot()





    def nextDay(self):
        self.step += 1
	

        self.setBot()

    def setWeekLayout(self):
        self.applet.setLayout(self.layout)

    def setOneDayLayout(self):
        self.applet.setLayout(self.layout)

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
        self.City = self.settings_dialog.get_city()
        self.weekly = self.settings_dialog.get_weekly()
        self.update()

    def configDenied(self):
        """Do nothing"""

        pass


def CreateApplet(parent):
    return BWCBalancePlasmoid(parent)
