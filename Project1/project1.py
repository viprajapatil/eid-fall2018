"""
@author Vipraja Patil
references:
login --- https://stackoverflow.com/questions/11812000/login-dialog-pyqt
https://ralsina.me/posts/BB974.html
"""
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import Adafruit_DHT as sensor

temp_list = []
hum_list = []

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        loadUi('login.ui',self)
        self.setWindowTitle('Login')
        self.user.text()
        self.password.text()
        self.login_button.clicked.connect(self.login_func)

    def login_func(self):
        if (self.user.text() == "vipraja" and self.password.text() == "vipraja"):
           self.accept()
        else:
           self.login_result.setText('Login unsucessful')

class project1(QDialog):
    def __init__(self, parent=None):
        super(project1,self).__init__()
        loadUi('project1.ui',self)
        self.setWindowTitle('EID project 1')
        self.temp_button = 0
        self.hum_button = 0
        self.conversion_flag = 0      # 0- Celsius, 1- Fahrenheit
        time = QTime.currentTime()
        self.refresh_temp.clicked.connect(self.temp_refresh_clicked)
        self.refresh_hum.clicked.connect(self.humidity_refresh_clicked)
        self.conversion_button.clicked.connect(self.conversion_clicked)

    @pyqtSlot()
    def get_temp(self):
         try:
            time = QTime.currentTime()
            humidity,temp = sensor.read(sensor.DHT22, 4)
            if temp is None and humidity is None:
               self.temp_value.setText('ERROR')
            else:
               if self.temp_button == 1:
                  if self.conversion_flag == 1:
                     temp = temp * 1.8
                     temp = temp + 32
                     if temp > 78.8:
                        self.alarm_temp.setText('ALERT HIGH TEMP')
                     else:
                        self.alarm_temp.setText('')
                     self.temp_value.setText('{} F'.format(round(temp,4)))
                  else:
                     if temp > 26:
                        self.alarm_temp.setText('ALERT HIGH TEMP')
                     else:
                        self.alarm_temp.setText('')
                     self.temp_value.setText('{} C'.format(round(temp,4)))
                  self.temp_time.setText(time.toString(Qt.DefaultLocaleLongDate))
                  self.temp_button = 0
               else:
                  if self.conversion_flag == 1:
                     self.list_temp.addItem('{} F'.format(round(temp,4)))
                  else:
                     self.list_temp.addItem('{} C'.format(round(temp,4)))
               temp_avg = 0
               temp_list_count = 0;
               temp_list.append(round(temp,4))
               for i in temp_list:
                  temp_avg = i + temp_avg
                  temp_list_count = temp_list_count + 1
               temp_avg = temp_avg/temp_list_count
               if self.conversion_flag == 1:
                  temp_avg_f = temp_avg
                  temp_avg_f = temp_avg_f * 1.8
                  temp_avg_f = temp_avg_f + 32
                  self.avg_temp.setText('Avg: {} F'.format(round(temp_avg_f,2)))
               else:
                  self.avg_temp.setText('Avg: {} C'.format(round(temp_avg,2)))
         finally:
            self.temp_button = 0
            QTimer.singleShot(2000, self.get_temp)

    def get_hum(self):
        try:
            time = QTime.currentTime()
            humidity,temp = sensor.read(sensor.DHT22, 4)
            if temp is None and humidity is None:
               self.hum_value.setText('ERROR')
            else:
               if self.hum_button == 1:
                  self.hum_value.setText('{} %'.format(round(humidity,4)))
                  self.hum_time.setText(time.toString(Qt.DefaultLocaleLongDate))
                  self.hum_button = 0
               if humidity > 34:
                  self.alarm_hum.setText('ALERT HIGH HUM')
               else:
                  self.alarm_hum.setText('')
               hum_avg = 0
               hum_list_count = 0
               hum_list.append(round(humidity,4))
               for i in hum_list:
                  hum_avg = i + hum_avg
                  hum_list_count = hum_list_count + 1
               hum_avg = hum_avg/hum_list_count
               self.list_hum.addItem('{} %'.format(round(humidity,4)))
               self.avg_hum.setText('Avg: {}%'.format(round(hum_avg,2)))
        finally:
            self.hum_button = 0
            QTimer.singleShot(2000, self.get_hum)

    def temp_refresh_clicked(self):
        self.temp_button = 1
        time = QTime.currentTime()
        self.get_temp()

    def humidity_refresh_clicked(self):
        self.hum_button = 1
        time = QTime.currentTime()
        self.get_hum()

    def conversion_clicked(self):
        self.conversion_flag = 1 - self.conversion_flag

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
       widget = project1()
       widget.show()
       sys.exit(app.exec_())
