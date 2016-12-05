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

        self.clearLayout()
        self.wasWeekly = 1

        self.resize(700, 300)

        """top"""

        self.dayLabel0 = Plasma.Label(self.applet)
        self.dayLabel1 = Plasma.Label(self.applet)
        self.dayLabel2 = Plasma.Label(self.applet)
        self.dayLabel3 = Plasma.Label(self.applet)
        self.dayLabel4 = Plasma.Label(self.applet)

        self.layout.addItem(self.dayLabel0, 0, 1)
        self.layout.addItem(self.dayLabel1, 0, 2)
        self.layout.addItem(self.dayLabel2, 0, 3)
        self.layout.addItem(self.dayLabel3, 0, 4)
        self.layout.addItem(self.dayLabel4, 0, 5)

        self.descLabel0 = Plasma.Label(self.applet)
        self.descLabel1 = Plasma.Label(self.applet)
        self.descLabel2 = Plasma.Label(self.applet)
        self.descLabel3 = Plasma.Label(self.applet)
        self.descLabel4 = Plasma.Label(self.applet)

        self.layout.addItem(self.descLabel0, 1, 1)
        self.layout.addItem(self.descLabel1, 1, 2)
        self.layout.addItem(self.descLabel2, 1, 3)
        self.layout.addItem(self.descLabel3, 1, 4)
        self.layout.addItem(self.descLabel4, 1, 5)

        self.tempLabel0 = Plasma.Label(self.applet)
        self.tempLabel1 = Plasma.Label(self.applet)
        self.tempLabel2 = Plasma.Label(self.applet)
        self.tempLabel3 = Plasma.Label(self.applet)
        self.tempLabel4 = Plasma.Label(self.applet)

        self.layout.addItem(self.tempLabel0, 2, 1)
        self.layout.addItem(self.tempLabel1, 2, 2)
        self.layout.addItem(self.tempLabel2, 2, 3)
        self.layout.addItem(self.tempLabel3, 2, 4)
        self.layout.addItem(self.tempLabel4, 2, 5)

        """bot"""

        self.timeBot0 = Plasma.Label(self.applet)
        self.timeBot1 = Plasma.Label(self.applet)
        self.timeBot2 = Plasma.Label(self.applet)
        self.timeBot3 = Plasma.Label(self.applet)
        self.timeBot4 = Plasma.Label(self.applet)

        self.layout.addItem(self.timeBot0, 3, 1)
        self.layout.addItem(self.timeBot1, 3, 2)
        self.layout.addItem(self.timeBot2, 3, 3)
        self.layout.addItem(self.timeBot3, 3, 4)
        self.layout.addItem(self.timeBot4, 3, 5)

        self.descBot0 = Plasma.Label(self.applet)
        self.descBot1 = Plasma.Label(self.applet)
        self.descBot2 = Plasma.Label(self.applet)
        self.descBot3 = Plasma.Label(self.applet)
        self.descBot4 = Plasma.Label(self.applet)

        self.layout.addItem(self.descBot0, 4, 1)
        self.layout.addItem(self.descBot1, 4, 2)
        self.layout.addItem(self.descBot2, 4, 3)
        self.layout.addItem(self.descBot3, 4, 4)
        self.layout.addItem(self.descBot4, 4, 5)

        self.tempBot0 = Plasma.Label(self.applet)
        self.tempBot1 = Plasma.Label(self.applet)
        self.tempBot2 = Plasma.Label(self.applet)
        self.tempBot3 = Plasma.Label(self.applet)
        self.tempBot4 = Plasma.Label(self.applet)

        self.layout.addItem(self.tempBot0, 5, 1)
        self.layout.addItem(self.tempBot1, 5, 2)
        self.layout.addItem(self.tempBot2, 5, 3)
        self.layout.addItem(self.tempBot3, 5, 4)
        self.layout.addItem(self.tempBot4, 5, 5)

        self.humBot0 = Plasma.Label(self.applet)
        self.humBot1 = Plasma.Label(self.applet)
        self.humBot2 = Plasma.Label(self.applet)
        self.humBot3 = Plasma.Label(self.applet)
        self.humBot4 = Plasma.Label(self.applet)

        self.layout.addItem(self.humBot0, 6, 1)
        self.layout.addItem(self.humBot1, 6, 2)
        self.layout.addItem(self.humBot2, 6, 3)
        self.layout.addItem(self.humBot3, 6, 4)
        self.layout.addItem(self.humBot4, 6, 5)

        """btns"""
        self.rightButtn = Plasma.PushButton(self.applet)
        self.leftButton = Plasma.PushButton(self.applet)
        self.rightButtn.setText("Next")
        self.leftButton.setText("Prev")
        self.connect(self.rightButtn, SIGNAL("clicked()"), self.nextDay)
        self.connect(self.leftButton, SIGNAL("clicked()"), self.prevDay)
        self.layout.addItem(self.rightButtn, 0, 6)
        self.layout.addItem(self.leftButton, 0, 0)


    def setFiveDaysData(self):

        # top
        stam = self.data['list'][0]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%a')
        self.dayLabel0.setText(value)
        self.dayLabel0.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        self.dayLabel0.setStyleSheet('')
        self.descLabel0.setText(self.data['list'][0]['weather'][0]['description'].replace (" ", "\n"))
        min = str(round(self.data['list'][0]['main']['temp_min'] - 273.15, 1))
        max = str(round(self.data['list'][0]['main']['temp_max'] - 273.15, 1))
        self.tempLabel0.setText("Min: " + min + "\nMax: " + max)

        stam = self.data['list'][8]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%a')
        self.dayLabel1.setText(value)
        self.descLabel1.setText(self.data['list'][8]['weather'][0]['description'].replace (" ", "\n"))
        min = str(round(self.data['list'][8]['main']['temp_min'] - 273.15, 1))
        max = str(round(self.data['list'][8]['main']['temp_max'] - 273.15, 1))
        self.tempLabel1.setText("Min: " + min + "\nMax: " + max)

        stam = self.data['list'][16]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%a')
        self.dayLabel2.setText(value)
        self.descLabel2.setText(self.data['list'][16]['weather'][0]['description'].replace (" ", "\n"))
        min = str(round(self.data['list'][16]['main']['temp_min'] - 273.15, 1))
        max = str(round(self.data['list'][16]['main']['temp_max'] - 273.15, 1))
        self.tempLabel2.setText("Min: " + min + "\nMax: " + max)

        stam = self.data['list'][24]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%a')
        self.dayLabel3.setText(value)
        self.descLabel3.setText(self.data['list'][24]['weather'][0]['description'].replace (" ", "\n"))
        min = str(round(self.data['list'][24]['main']['temp_min'] - 273.15, 1))
        max = str(round(self.data['list'][24]['main']['temp_max'] - 273.15, 1))
        self.tempLabel3.setText("Min: " + min + "\nMax: " + max)

        stam = self.data['list'][-1]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%a')
        self.dayLabel4.setText(value)
        self.descLabel4.setText(self.data['list'][-1]['weather'][0]['description'].replace (" ", "\n"))
        min = str(round(self.data['list'][-1]['main']['temp_min'] - 273.15, 1))
        max = str(round(self.data['list'][-1]['main']['temp_max'] - 273.15, 1))
        self.tempLabel4.setText("Min: " + min + "\nMax: " + max)

        # bot

        self.setBot()

        self.prevDay()
        """
        svg = Plasma.Svg(self.applet)
        icon_path = "contents/icons/10d.svg"
        svg.setImagePath(icon_path)
        self.icon = Plasma.SvgWidget(svg)
        self.layout.addItem(self.icon, 1, 0)
        """
        """
        self.humBot0.setText(str(self.data['name']))
        self.humBot1.setText(str(self.data['name']))
        self.humBot2.setText(str(self.data['name']))
        self.humBot3.setText(str(self.data['name']))
        self.humBot4.setText(str(self.data['name']))

        self.descLabel0.setText("AA")
        self.descLabel1.setText("AB")
        self.descLabel2.setText("AC")
        self.descLabel3.setText("AD")
        self.descLabel4.setText("AE")
        """
        """
        for i in range(5):
            self.nameLabels[i].setText(str(self.data['name']))
            self.nameLabels[i].setStyleSheet('font: 10pt "Monaco"')
        for i in range(5):
            self.descLabels[i].setText(str(self.data['weather'][0]['description']))
            self.descLabels[i].setStyleSheet('font: 10pt "Monaco"')
        for i in range(5):
            self.tempLabels[i].setText(str(round(self.data['main']['temp'] - 273.15, 1)) + ' C')
            self.tempLabels[i].setStyleSheet('font: 10pt "Monaco"')
        for i in range(5):
            self.humLabels[i].setText(str(self.data['main']['humidity']) + '%')
            self.humLabels[i].setStyleSheet('font: 10pt "Monaco"')
        """

    def setBot(self):
        if self.step + 4 >= len(self.data['list']):
            self.step -= 1
        if self.step < 0:
            self.step = 0
        stam = self.data['list'][0 + self.step]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%H')
        self.timeBot0.setText(value)
        self.descBot0.setText(self.data['list'][0 + self.step]['weather'][0]['description'].replace (" ", "\n"))
        temp = str(round(self.data['list'][0 + self.step]['main']['temp'] - 273.15, 1))
        self.tempBot0.setText("Temp: " + temp + " C")

        stam = self.data['list'][1 + self.step]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%H')
        self.timeBot1.setText(value)
        self.descBot1.setText(self.data['list'][1 + self.step]['weather'][0]['description'].replace (" ", "\n"))
        temp = str(round(self.data['list'][1 + self.step]['main']['temp'] - 273.15, 1))
        self.tempBot1.setText("Temp: " + temp + " C")

        stam = self.data['list'][2 + self.step]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%H')
        self.timeBot2.setText(value)
        self.descBot2.setText(self.data['list'][2 + self.step]['weather'][0]['description'].replace (" ", "\n"))
        temp = str(round(self.data['list'][2 + self.step]['main']['temp'] - 273.15, 1))
        self.tempBot2.setText("Temp: " + temp + " C")

        stam = self.data['list'][3 + self.step]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%H')
        self.timeBot3.setText(value)
        self.descBot3.setText(self.data['list'][3 + self.step]['weather'][0]['description'].replace (" ", "\n"))
        temp = str(round(self.data['list'][3 + self.step]['main']['temp'] - 273.15, 1))
        self.tempBot3.setText("Temp: " + temp + " C")

        stam = self.data['list'][4 + self.step]['dt']
        value = datetime.datetime.fromtimestamp(stam).strftime('%H')
        self.timeBot4.setText(value)
        self.descBot4.setText(self.data['list'][4 + self.step]['weather'][0]['description'].replace (" ", "\n"))
        temp = str(round(self.data['list'][4 + self.step]['main']['temp'] - 273.15, 1))
        self.tempBot4.setText("Temp: " + temp + " C")
        self.timeBot0.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        self.timeBot1.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        self.timeBot2.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        self.timeBot3.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        self.timeBot4.setStyleSheet('font-style: italic; font-size: 20px; color: red')


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
        self.dayLabel0.setText("")
        self.dayLabel1.setText("")
        self.dayLabel2.setText("")
        self.dayLabel3.setText("")
        self.dayLabel4.setText("")

        self.descLabel0.setText("")
        self.descLabel1.setText("")
        self.descLabel2.setText("")
        self.descLabel3.setText("")
        self.descLabel4.setText("")

        self.tempLabel0.setText("")
        self.tempLabel1.setText("")
        self.tempLabel2.setText("")
        self.tempLabel3.setText("")
        self.tempLabel4.setText("")

        self.timeBot0.setText("")
        self.timeBot1.setText("")
        self.timeBot2.setText("")
        self.timeBot3.setText("")
        self.timeBot4.setText("")

        self.descBot0.setText("")
        self.descBot1.setText("")
        self.descBot2.setText("")
        self.descBot3.setText("")
        self.descBot4.setText("")

        self.tempBot0.setText("")
        self.tempBot1.setText("")
        self.tempBot2.setText("")
        self.tempBot3.setText("")
        self.tempBot4.setText("")


        self.humBot0.setText("")
        self.humBot1.setText("")
        self.humBot2.setText("")
        self.humBot3.setText("")
        self.humBot4.setText("")

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
        self.dayLabel0.setStyleSheet('')
        self.dayLabel1.setStyleSheet('')
        self.dayLabel2.setStyleSheet('')
        self.dayLabel3.setStyleSheet('')
        self.dayLabel4.setStyleSheet('')
        if self.step < 8:
            self.dayLabel0.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        elif self.step < 16:
            self.dayLabel1.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        elif self.step < 24:
            self.dayLabel2.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        elif self.step < 32:
            self.dayLabel3.setStyleSheet('font-style: italic; font-size: 20px; color: red')



    def nextDay(self):
        self.step += 1
        self.setBot()
        self.dayLabel0.setStyleSheet('')
        self.dayLabel1.setStyleSheet('')
        self.dayLabel2.setStyleSheet('')
        self.dayLabel3.setStyleSheet('')
        self.dayLabel4.setStyleSheet('')
        if self.step < 8:
            self.dayLabel0.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        elif self.step < 16:
            self.dayLabel1.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        elif self.step < 24:
            self.dayLabel2.setStyleSheet('font-style: italic; font-size: 20px; color: red')
        elif self.step < 32:
            self.dayLabel3.setStyleSheet('font-style: italic; font-size: 20px; color: red')

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
