import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKitWidgets import *
import datetime
import time
import threading
import ast
#from PyQt5.QtWebEngineWidgets import *
#from PyQt5 import QtWebEngineWidgets

class SmartMirrorGUI(QWidget):
    def __init__(self, width, height):
        super().__init__()
        self.startX = ""
        self.startY = ""
        self.endX = ""
        self.endY = ""
        self.webView = None
        self.showFullScreen()
        self.setFixedSize(width, height)
        self.setWindowTitle('鏡:Rorrim')
        self.playlist = []
        self.initUI()

    def closeEvent(self, event):
        self.deleteLater()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        vlayout = QVBoxLayout()
        self.setLayout(vlayout)
        self.initDatetime()
        self.initSchedule()
        self.initNews()
        self.initMusic()
        self.initWeather()
        self.initPath()
        self.dt_th = threading.Thread(target=self.updateDatetime)
        self.dt_th.daemon = True
        self.dt_th.start()

    def initPath(self):
        self.webView = QWebView(self)
        self.webView.setUrl(QUrl("http://sd100.iptime.org:5000/getPath"))
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        self.webView.setFixedSize(self.width()/100*29, self.width()/100*29)
        self.webView.setZoomFactor(self.webView.width()/500)
        self.webView.move(self.width()-self.webView.width(), self.height()-self.webView.height())
        self.layout().addChildWidget(self.webView)
        self.webView.setVisible(True)
        self.sld = QSlider()
        self.sldvalue = 1
        self.sld.setValue(self.sldvalue)
        self.sld.valueChanged.connect(self.getPath)

    def setStartPoint(self, point):
        self.startX = point['longitude']
        self.startY = point['latitude']

    def initSchedule(self):
        # get schedules from server or google calendar
        self.scheWidget = QWidget()
        vlayout = QVBoxLayout()
        self.scheWidget.setLayout(vlayout)

        self.scheLB = [QLabel("1"), QLabel("2"), QLabel("3")]
        
        for i in range(3):
            #self.scheLB[i] = QLabel("hihi")
            self.scheLB[i].setStyleSheet('color: white')
            self.scheLB[i].setFont(QFont("", 20, QFont.Bold))
            self.scheLB[i].setFixedSize(self.width()/100*40, self.height()/100*6)
            self.scheLB[i].move(self.width()/100, self.height()/100*(76+i*6))
            self.scheLB[i].setAutoFillBackground(True)
            p = self.scheLB[i].palette()
            p.setColor(self.scheLB[i].backgroundRole(), Qt.black)
            self.scheLB[i].setPalette(p)
            self.scheLB[i].setAlignment(Qt.AlignVCenter)
            self.scheWidget.layout().addChildWidget(self.scheLB[i])
            self.scheLB[i].setVisible(False)

        #self.scheWidget.setVisible(True)
        self.layout().addChildWidget(self.scheWidget)
        self.layout().addChildWidget(self.scheLB[0])
        self.layout().addChildWidget(self.scheLB[1])
        self.layout().addChildWidget(self.scheLB[2])
        

    def controlView(self, alarm_dict):
        activity = list(alarm_dict.keys())[0]
        flag = self.str_to_bool(alarm_dict[activity])
        # We have to do => set label enable, disable
        if activity == 'NewsActivity':
            self.newsLB.setVisible(flag)
        elif activity == 'CalendarActivity':
            self.scheLB[0].setVisible(flag)
            self.scheLB[1].setVisible(flag)
            self.scheLB[2].setVisible(flag)
        elif activity == 'PathActivity':
            if self.webView is not None:
                self.webView.setVisible(flag)
        elif activity == 'MusicActivity':
            self.musicLB[0].setVisible(flag)
            self.musicLB[1].setVisible(flag)
        elif activity == 'WeatherActivity':
            self.weatherWidget.setVisible(flag)
        else:
            pass

    def str_to_bool(self, str):
        if str == 'true':
            return True
        elif str == 'false' or 'False':
            return False
        else:
            return True

    def initNews(self):
        # get news from server

        LB = QLabel("")
        LB.setStyleSheet('color: white')
        LB.setFont(QFont("", 20, QFont.Bold))
        LB.setFixedSize(self.width(), self.height()/100*5)
        LB.move(self.width()/100, self.height()/100*94)
        LB.setAutoFillBackground(True)
        p = LB.palette()
        p.setColor(LB.backgroundRole(), Qt.black)
        LB.setPalette(p)
        LB.setAlignment(Qt.AlignVCenter)
        self.newsLB = LB
        self.layout().addChildWidget(self.newsLB)

    def initWeather(self):
        # get weather information from server or by using api

        #if weather_info is None:
        #    return None

        dt = datetime.datetime.now()

        self.weatherWidget = QWidget()
        vlayout = QVBoxLayout()
        self.weatherWidget.setLayout(vlayout)

        self.imgLB = QLabel()
        img = QPixmap("weather_img/sunny-day.png")
        img.scaledToWidth(5, Qt.FastTransformation)
        img = img.scaledToWidth(self.width()/100*5)
        self.imgLB.setPixmap(img)
        self.imgLB.setFixedSize(img.width(), img.height())
        self.imgLB.move(self.width()/100*2, self.height()/100*1)
        self.imgLB.setAutoFillBackground(True)
        p = self.imgLB.palette()
        p.setColor(self.imgLB.backgroundRole(), Qt.black)
        self.imgLB.setPalette(p)
        self.imgLB.setAlignment(Qt.AlignCenter)

        self.tempLB = QLabel("")
        self.tempLB.setStyleSheet('color: white')
        self.tempLB.setFont(QFont("", 30, QFont.Bold))
        self.tempLB.setFixedSize(self.width()/100*8, img.height())
        self.tempLB.move(self.width()/100*2+img.width(), self.height()/100*1)
        self.tempLB.setAutoFillBackground(True)
        p = self.tempLB.palette()
        p.setColor(self.tempLB.backgroundRole(), Qt.black)
        self.tempLB.setPalette(p)
        self.tempLB.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        #loc = self.wc.get_location()
        #locLB = QLabel(loc)
        self.locLB = QLabel("")
        self.locLB.setStyleSheet('color: white')
        self.locLB.setFont(QFont("", 20, QFont.Bold))
        self.locLB.setFixedSize(self.width()/100*20, self.height()/100*5)
        self.locLB.move(self.width()/100, self.height()/100*1+img.height())
        self.locLB.setAutoFillBackground(True)
        p = self.locLB.palette()
        p.setColor(self.locLB.backgroundRole(), Qt.black)
        self.locLB.setPalette(p)
        self.locLB.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        #mmLB = QLabel("▲"+str(weather_info["max_tem"])[:-2]+"˚C ▼"+str(weather_info["min_tem"])[:-2]+"˚C")
        self.mmLB = QLabel("")
        self.mmLB.setStyleSheet('color: white')
        self.mmLB.setFont(QFont("", 20, QFont.Bold))
        self.mmLB.setFixedSize(self.width()/100*20, self.height()/100*5)
        self.mmLB.move(self.width()/100, self.height()/100*7 + img.height())
        self.mmLB.setAutoFillBackground(True)
        p = self.mmLB.palette()
        p.setColor(self.mmLB.backgroundRole(), Qt.black)
        self.mmLB.setPalette(p)
        self.mmLB.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        self.weatherWidget.layout().addChildWidget(self.imgLB)
        self.weatherWidget.layout().addChildWidget(self.tempLB)
        self.weatherWidget.layout().addChildWidget(self.locLB)
        self.weatherWidget.layout().addChildWidget(self.mmLB)
        self.layout().addChildWidget(self.weatherWidget)

    def initMusic(self):
        # get music file or information

        #self.playlist = self.wc.get_playlist()
        self.playlist = []

        musicLB = []
        titleLB = QLabel("")
        if self.playlist is not None and len(self.playlist) > 0:
            titleLB.setText("♬ " + self.playlist[0][0])
        titleLB.setStyleSheet('color: white')
        titleLB.setFont(QFont("", 25, QFont.Bold))
        titleLB.setFixedSize(self.width()/100*30, self.height()/100*6)
        titleLB.move(self.width()/100*35, self.height()/100*3)
        titleLB.setAutoFillBackground(True)
        p = titleLB.palette()
        p.setColor(titleLB.backgroundRole(), Qt.black)
        titleLB.setPalette(p)
        titleLB.setAlignment(Qt.AlignHCenter)
        musicLB.append(titleLB)

        artistLB = QLabel("")
        if self.playlist is not None and len(self.playlist) > 0:
            artistLB.setText(self.playlist[0][1])
        artistLB.setStyleSheet('color: white')
        artistLB.setFont(QFont("", 22, QFont.Bold))
        artistLB.setFixedSize(self.width()/100*30, self.height()/100*6)
        artistLB.move(self.width()/100*35, self.height()/100*9)
        artistLB.setAutoFillBackground(True)
        p = artistLB.palette()
        p.setColor(artistLB.backgroundRole(), Qt.black)
        artistLB.setPalette(p)
        artistLB.setAlignment(Qt.AlignHCenter)
        musicLB.append(artistLB)

        self.musicLB = musicLB
        self.layout().addChildWidget(self.musicLB[0])
        self.layout().addChildWidget(self.musicLB[1])
        self.musicLB[0].setVisible(False)
        self.musicLB[1].setVisible(False)

    def initDatetime(self):
        dt = datetime.datetime.now()

        weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
        month = ["December", "January", "February", "March", "April", "May", "June", "July", "August", "September",
                 "October", "November", "December"]
        d = weekday[dt.weekday()] + ", " + month[dt.month] + " " + str(dt.day) + " " + str(dt.year)

        dateLB = QLabel(d)
        dateLB.setStyleSheet('color: white')
        dateLB.setFont(QFont("", 21, QFont.Bold))
        dateLB.setFixedSize(self.width()/100*33, self.height()/100*6)
        dateLB.move(self.width()/100*65, self.height()/100*3)
        dateLB.setAutoFillBackground(True)
        p = dateLB.palette()
        p.setColor(dateLB.backgroundRole(), Qt.black)
        dateLB.setPalette(p)
        dateLB.setAlignment(Qt.AlignRight)

        t = str(dt)[11:16]
        if dt.hour > 12:
            t = t + " PM"
        else:
            t = t + " AM"
        timeLB = QLabel(t)
        timeLB.setStyleSheet('color: white')
        timeLB.setFont(QFont("", 30, QFont.Bold))
        timeLB.setFixedSize(self.width()/100*33, self.height()/100*8)
        timeLB.move(self.width()/100*65, self.height()/100*9)
        timeLB.setAutoFillBackground(True)
        p = timeLB.palette()
        p.setColor(timeLB.backgroundRole(), Qt.black)
        timeLB.setPalette(p)
        timeLB.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.timeLB = timeLB
        self.dateLB = dateLB
        self.layout().addChildWidget(self.dateLB)
        self.layout().addChildWidget(self.timeLB)

    def setWeather(self, weather_info):
        if weather_info is None:
            return None

        dt = datetime.datetime.now()

        img = QPixmap("weather_img/sunny-day.png")

        if weather_info['cur_sky'] == "Sunny":
            if dt.hour >= 6 and dt.hour <= 20:
                img = QPixmap("weather_img/sunny-day.png")
            else:
                img = QPixmap("weather_img/sunny-night.png")
        elif weather_info['cur_sky'] == "Cloudy":
            if dt.hour >= 6 and dt.hour <= 20:
                img = QPixmap("weather_img/cloudy-day.png")
            else:
                img = QPixmap("weather_img/cloudy-night.png")
        elif weather_info['cur_sky'] == "Very Cloudy":
            img = QPixmap("weather_img/cloudy-many.png")
        elif weather_info['cur_sky'] == "Foggy":
            img = QPixmap("weather_img/cloudy-so-much.png")
        elif weather_info['cur_sky'] == "Rainy":
            img = QPixmap("weather_img/rainy.png")
        elif weather_info['cur_sky'] == "rain with snow":
            img = QPixmap("weather_img/rainy-snow.png")
        elif weather_info['cur_sky'] == "Snowy":
            img = QPixmap("weather_img/snow.png")

        img.scaledToWidth(10, Qt.FastTransformation)
        img = img.scaledToWidth(self.width() / 100 * 5)
        self.imgLB.setPixmap(img)

        self.tempLB.setText(str(weather_info['cur_tem']) + "˚C")
        self.mmLB.setText("▲" + str(weather_info["max_tem"])[:-2] + "˚C ▼" + str(weather_info["min_tem"])[:-2] + "˚C")

    def setLocation(self, loc):
        self.locLB.setText(loc)

    def setNews(self, text):
        self.newsLB.setText(text)

    def updateDatetime(self):
        while(True):
            try:
                dt = datetime.datetime.now()

                weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
                month = ["December", "January", "February", "March", "April", "May", "June", "July", "August", "September",
                         "October", "November", "December"]
                d = weekday[dt.weekday()] + ", " + month[dt.month] + " " + str(dt.day) + " " + str(dt.year)
                t = str(dt)[11:16]
                if dt.hour > 12:
                    t = t + " PM"
                else:
                    t = t + " AM"
                self.dateLB.setText(d)
                self.timeLB.setText(t)
                time.sleep(1)
            except:
                break

    def setPath(self, point):
        self.endY = point['lat']
        self.endX = point['lng']
        self.sldvalue += 1
        if self.sldvalue == 100:
            sldvalue = 1
        self.sld.setValue(self.sldvalue)

    def getPath(self):
        self.webView.setUrl(QUrl("http://sd100.iptime.org:5000/getPath?startX="+str(self.startX)+"&startY="+str(self.startY)+"&endX="+str(self.endX)+"&endY="+str(self.endY)))
        self.webView.setVisible(True)

